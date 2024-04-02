import os

import torch
from anthropic import Anthropic, AnthropicBedrock
from gstop import STOP_TOKENS_REGISTRY, GenerationStopper
from loguru import logger
from openai import OpenAI
from spllm.model.utils import load_model_from_tree
from spllm.utils import get_single_openai_api_key
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    PreTrainedModel,
    TextGenerationPipeline,
    TextStreamer,
)

from .chat import Dialog, Utterance
from .prompts import ChatTemplate
from .retrievers import FactRetriever
from .templates import TEMPLATE_REGISTRY


class ChatEngine:
    def __init__(
        self,
        template: ChatTemplate | str,
        model: str | PreTrainedModel | None = None,
        template_registry: dict[str, ChatTemplate] | None = None,
        memory_size: int = 40,
        tokenizer: str | AutoTokenizer = None,
        model_kwargs: dict = {"device_map": "auto"},
        template_kwargs: dict = {},
        stopper: str | None = "mistral",
        revision: str | None = None,
        do_merge: bool = True,
    ):
        self.model_name = model

        if isinstance(model, str):
            self.model, self.tokenizer = load_model_from_tree(
                model_name=model,
                revision=revision,
                return_self=True,
                return_tokenizer=True,
                do_merge=do_merge,
                **model_kwargs,
            )
        elif isinstance(model, PreTrainedModel):
            self.model = model
            self.tokenizer = AutoTokenizer.from_pretrained(
                tokenizer if tokenizer else model.config.name_or_path
            )
        else:
            raise ValueError(f"Invalid model: {model}")

        self.tokenizer.pad_token_id = self.tokenizer.eos_token_id
        self.pipeline = TextGenerationPipeline(self.model, self.tokenizer)
        self.streamer = TextStreamer(self.tokenizer)

        if template_registry is None:
            template_registry = TEMPLATE_REGISTRY

        self.dialog = Dialog(
            template=template, template_registry=template_registry, **template_kwargs
        )
        self.input_prompt = ""

        self._memory_size = memory_size

        if stopper:
            self.set_stopper(stopper)
        else:
            self.stopper = None

        logger.info(f"Model: {model}")
        if self.model.device.type == "cpu":
            logger.warning(
                "Model is on CPU. Consider using a GPU for faster generation."
            )
        else:
            logger.info(f"Model is on {self.model.device}")

    def __del__(self):
        self.sleep()

    def __repr__(self):
        return f"{self.__class__.__name__}(model={self.model_name}, template={self.dialog.template}, memory_size={self._memory_size})"

    def hear(self, utterance: Utterance | str):
        if isinstance(utterance, str):
            utterance = Utterance(content=utterance, speaker="user")
        self.memorize(utterance)

    def say(
        self,
        system_message: str = "",
        prompt_kwargs: dict | None = None,
        gen_kwargs: dict = {"max_new_tokens": 128},
        stream: bool = True,
    ):
        if prompt_kwargs is None:
            prompt_kwargs = {}

        prompt = (
            self.dialog.format(**prompt_kwargs)
            + self.dialog.template.user_suffix
            + self.dialog.template.assistant_prefix
        )
        self.input_prompt = prompt
        # logger.debug(f"\nPrompt: {prompt}")
        return self.generate(
            prompt=prompt, stream=stream, system_message=system_message, **gen_kwargs
        )

    def generate(
        self, prompt: str, stream: bool = True, system_message: str = "", **kwargs
    ):
        generated_text = self.pipeline(
            system_message + prompt,
            num_return_sequences=1,
            return_full_text=False,
            use_cache=True,
            streamer=self.streamer if stream else None,
            stopping_criteria=None if self.stopper is None else self.stopper.criteria,
            **kwargs,
        )[0]["generated_text"]

        if self.stopper:
            generated_text = self.stopper.format(generated_text)

        self.memorize(
            Utterance(
                speaker="assistant",
                content=generated_text,
            )
        )
        return generated_text

    def respond(
        self,
        utterance: str,
        system_message: str = "",
        stream=True,
        gen_kwargs={"max_new_tokens": 128, "temperature": 0.7, "do_sample": True},
        prompt_kwargs={},
    ):
        if self._memory_size == 0:
            self.clear()
        self.hear(
            Utterance(
                content=utterance,
                speaker="user",
            )
        )
        return self.say(
            system_message=system_message,
            stream=stream,
            gen_kwargs=gen_kwargs,
            prompt_kwargs=prompt_kwargs,
        )

    def chat(self, stream=False, **kwargs):
        print("=" * 100)
        print("Let's start chatting! Press enter to exit.")
        print("=" * 100)
        while True:
            user_utterance = input("You: ")
            print("-" * 100)
            if user_utterance == "exit":
                break
            elif user_utterance == "clear":
                self.clear()
                continue
            avatar_utterance = self.respond(
                user_utterance,
                gen_kwargs=kwargs,
                stream=stream,
            )
            print(f"{self.__class__.__name__}: {avatar_utterance}")
            print("-" * 100)

    def memorize(self, utterance: Utterance):
        if self._memory_size == 0:
            pass
        elif len(self.dialog) >= self._memory_size:
            self.dialog.memory.forget(idx_exp=f"-({self._memory_size} - 1):")
        self.dialog.add(utterance)

    def clear(self):
        self.dialog.clear()
        logger.success("Memory cleared")

    def sleep(self):
        if hasattr(self, "model"):
            del self.model
        torch.cuda.empty_cache()
        logger.success("Avatar is sleeping")

    def wake_up(self, model_name, **kwargs):
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name, device_map="auto", **kwargs
        )
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.tokenizer.pad_token_id = self.tokenizer.eos_token_id
        self.pipeline = TextGenerationPipeline(self.model, self.tokenizer)
        self.streamer = TextStreamer(self.tokenizer)
        logger.success(f"{model_name} is ready")

    def refresh(self, model_name, **kwargs):
        self.sleep()
        self.wake_up(model_name, **kwargs)

    @property
    def memory(self):
        return self.dialog

    @property
    def memory_size(self):
        return self._memory_size

    @memory_size.setter
    def memory_size(self, value):
        self._memory_size = value
        if value == 0:
            self.clear()

    def set_stopper(self, stopper: str):
        logger.info(f"Setting stopper: {stopper}")
        self.stopper = GenerationStopper(stop_tokens=STOP_TOKENS_REGISTRY[stopper])


class APIChatEngine:
    available_models = [
        "gpt-4",
        "gpt-3.5",
        "haiku",
        "sonnet",
        "opus",
    ]

    def __init__(
        self,
        model: str,
        on_bedrock: bool = False,
        system_message: str | None = None,
        memory_size: int = 10,
    ):
        if memory_size < 1:
            raise ValueError("Memory size must be greater than 0")

        self.model_alias = model
        self.sys_msg = system_message
        self.memory_size = memory_size

        if model in ["gpt-4", "gpt-3.5"]:
            self.client = OpenAI(api_key=get_single_openai_api_key())

            match model:
                case "gpt-4":
                    self.model = "gpt-4-turbo-preview"
                case "gpt-3.5":
                    self.model = "gpt-3.5-turbo"

        elif model in ["haiku", "sonnet", "opus"]:
            if on_bedrock:
                self.client = AnthropicBedrock()

                match model:
                    case "haiku":
                        self.model = "anthropic.claude-3-haiku-20240307-v1:0"
                    case "sonnet":
                        self.model = "anthropic.claude-3-sonnet-20240229-v1:0"
                    case "opus":
                        raise ValueError(
                            f"Invalid model: {model} is not supported on Bedrock"
                        )

            else:
                self.client = Anthropic()

                match model:
                    case "haiku":
                        self.model = "claude-3-haiku-20240307"
                    case "sonnet":
                        self.model = "claude-3-sonnet-20240229"
                    case "opus":
                        self.model = "claude-3-opus-20240229"

        else:
            raise ValueError(f"Invalid model: {model}")

        self.memory: list[dict[str, str]] = []

    def respond(
        self,
        user_message: str,
        system_message: str | None = None,
        json_mode: bool = False,
    ):
        if system_message is None:
            system_message = self.sys_msg

        if isinstance(self.client, OpenAI):
            messages = (
                [{"role": "system", "content": system_message}]
                if system_message
                else []
            )
            for uttr in self.memory:
                if uttr["role"] == "user":
                    messages.append({"role": "user", "content": uttr["content"]})
                elif uttr["role"] == "assistant":
                    messages.append({"role": "assistant", "content": uttr["content"]})
            messages.append({"role": "user", "content": user_message})
            self.memory.append({"role": "user", "content": user_message})

            client_inputs = {"model": self.model, "messages": messages}
            if json_mode:
                client_inputs["response_format"] = {"type": "json_object"}

            response = self.client.chat.completions.create(**client_inputs)
            response = response.choices[0].message.content

        elif isinstance(self.client, Anthropic) or isinstance(
            self.client, AnthropicBedrock
        ):
            if system_message is None:
                system_message = ""

            messages = []
            for uttr in self.memory:
                if uttr["role"] == "user":
                    messages.append({"role": "user", "content": uttr["content"]})
                elif uttr["role"] == "assistant":
                    messages.append({"role": "assistant", "content": uttr["content"]})
            messages.append({"role": "user", "content": user_message})
            self.memory.append({"role": "user", "content": user_message})

            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=system_message,
                messages=messages,
            )
            response = response.content[0].text

        self.memory.append({"role": "assistant", "content": response})

        if len(self.memory) > self.memory_size:
            self.memory = self.memory[-self.memory_size :]
            if self.memory[0]["role"] == "assistant":
                self.memory.pop(0)

        return response

    def clear(self):
        self.memory = []
        logger.success("Memory cleared")


class Avatar(ChatEngine):
    """Handles the memory, prompt-formatting, and conversation generation."""

    def __init__(
        self,
        name: str,
        model_name: str,
        template: ChatTemplate | str,
        data_dir: str,
        db_dir: str,
        template_registry: dict[str, ChatTemplate] | None = None,
        memory_size: int = 0,
        tokenizer_name: str | None = None,
        model_kwargs: dict = {},
        template_kwargs: dict = {},
        stopper: str | None = "mistral",
    ):
        self.data_dir = data_dir
        self.db_dir = db_dir

        # Prepare ai characteristics and fact retriever
        self.set(name)

        super().__init__(
            model=model_name,
            template=template,
            template_registry=template_registry,
            memory_size=memory_size,
            tokenizer=tokenizer_name,
            model_kwargs=model_kwargs,
            template_kwargs=template_kwargs,
            stopper=stopper,
        )

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name})"

    def say(
        self,
        prompt_kwargs: dict = {},
        gen_kwargs: dict = {"max_new_tokens": 100},
        stream: bool = True,
    ):
        if "assistant_info" in self.dialog.template.input_variables:
            prompt_kwargs["assistant_info"] = self.search(
                self.dialog.query.content, top_k=prompt_kwargs["rag_k"]
            )

        prompt = self.dialog.format(
            assistant_chara=self.assistant_chara, **prompt_kwargs
        )
        self.input_prompt = prompt
        logger.debug(f"Prompt: {prompt}")
        return self.generate(prompt=prompt, stream=stream, **gen_kwargs)

    def search(self, query: str, top_k: int = 5) -> str:
        return self.retriever.retrieve(query, top_k)

    def set(self, name):
        try:
            with open(
                os.path.join(self.data_dir, name, "summary_speech_habits.txt")
            ) as f:
                self.assistant_chara = f.read()
        except FileNotFoundError:
            logger.warning(f"{name}'s speech habits not found at {self.data_dir}")
            return
        self.name = name
        self.retriever = FactRetriever(db_dir=self.db_dir, embd_style="openai")
        self.retriever.set_user(name)

        logger.success(f"{name} is ready")
