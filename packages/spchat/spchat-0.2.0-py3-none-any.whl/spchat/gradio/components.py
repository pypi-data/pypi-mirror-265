import glob
import uuid
from dataclasses import dataclass
from pathlib import Path

import gradio as gr
from loguru import logger

from ..avatars import Avatar
from ..chat import Utterance
from ..prompts import ChatTemplate


def get_latest_checkpoint(model_dir):
    checkpoints = glob.glob(f"{model_dir}/checkpoint-*")
    if len(checkpoints) == 0:
        return None
    for checkpoint in checkpoints:
        if "best" in checkpoint:
            return checkpoint
        elif "latest" in checkpoint:
            return checkpoint
    return max(checkpoints, key=lambda x: int(x.split("-")[-1]))


model_registry = {
    "v1.1_rank8": {
        "name": "/nas/share/results/Ditto/2024-02-15/v1-8gpu-rank8-2",
        "template": "stability_v1",
        "description": "v1.1 rank 8",
    },
    "v1.1_rank100": {
        "name": "/nas/share/results/Ditto/2024-02-14/v1-8gpu-rank8",
        "template": "stability_v1",
        "description": "v1.1 rank 100",
    },
    "v1.1_ensemble_rank100": {
        "name": "/nas/k_ishikawa/results/Ditto/2024-02-28/rank100_v2_ensemble_ep1",
        "template": "stability_v1",
    },
    "v1.1_rank8-ep3": {
        "name": "/nas/k_ishikawa/results/Ditto/2024-02-16/v1-rank8-epoch3",
        "template": "stability_v1",
        "description": "v1.1 rank 8 epoch 3",
    },
    "v1.1_rank100-ep3": {
        "name": "/nas/k_ishikawa/results/Ditto/2024-02-16/v1-rank100-epoch3",
        "template": "stability_v1",
    },
    "v1.1_rank8_fun": {
        "name": "/nas/k_ishikawa/results/Ditto/2024-02-20/v2-rank8-fun",
        "template": "stability_v1_fun",
    },
    "v1.1_rank100_fun": {
        "name": "/nas/k_ishikawa/results/Ditto/2024-02-20/v1-rank100-fun",
        "template": "stability_v1_fun",
    },
    "v1.1_rank100_fun-mt50-ep5": {
        "name": "/nas/k_ishikawa/results/Ditto/2024-02-20/v1-rank100-mt50-ep5",
        "template": "stability_v1_fun",
    },
    "v2.2_rank8_fun": {
        "name": "/nas/k_ishikawa/results/Ditto/2024-02-20/v1-rank8-fun",
        "template": "stability_v2_fun",
    },
    "v2.2_rank100_fun": {
        "name": "/nas/k_ishikawa/results/Ditto/2024-02-20/v2-rank100-fun",
        "template": "stability_v2_fun",
    },
    "v2.2_rank100_fun-mt50-ep5": {
        "name": "/nas/k_ishikawa/results/Ditto/2024-02-20/v2-rank100-mt50-ep5",
        "template": "stability_v2_fun",
    },
    "v2.2_rank100_fun-mt50-far-ep5": {
        "name": "/nas/k_ishikawa/results/Ditto/2024-02-20/v2-rank100-mt50-ep5-far",
        "template": "stability_v2_fun_far_history",
    },
    "v2.2_rank100_fun-ai50-shi3z": {
        "name": "/nas/k_ishikawa/results/Ditto/2024-02-21/v2-rank100-ai50-shi3z",
        "template": "stability_v2_fun",
    },
    "v2.2_rank100_fun-ai50-shi3z-alpaca_ja": {
        "name": "/nas/k_ishikawa/results/Ditto/2024-02-21/v2-rank100-ai50-shi3z-alpaca_ja",
        "template": "stability_v2_fun",
    },
    "v3.0_rank100_mt50-ep1": {
        "name": "/nas/k_ishikawa/results/Ditto/2024-02-22/rank100_v3.0-mt-50_ep1",
        "template": "stability_v3",
    },
    "v3.0_rank100_ensemble-ep5": {
        "name": "/nas/k_ishikawa/results/Ditto/2024-02-29/rank100_v3_ensemble_ep1_xx2sample",
        "template": "stability_v3",
    },
    "v4.0_rank100_ensemble-ep5": {
        "name": "/nas/k_ishikawa/results/Ditto/2024-03-05/rank100_v4_ensemble_ep5_mt",
        "template": "stability_v4",
    },
    "ca_rank100_ensemble-ep10": {
        "name": "/nas/k_ishikawa/results/Ditto/2024-03-05/rank100_ca_ensemble_ep10_mt",
        "template": "calm2",
    },
    "ca_rank100_no-x_ep5": {
        "name": "/nas/k_ishikawa/results/Ditto/2024-03-05/rank100_ca_jakucho-gpt_ep5_mt",
        "template": "calm2",
    },
}


@dataclass
class AppState:
    profile_dir: Path = Path("/nas/k_ishikawa/datasets/chat/ditto/avatars")
    db_dir: Path = Path("/nas/k_ishikawa/datasets/chat/ditto/vectorstore")
    log_dir: Path = Path("/nas/k_ishikawa/tmp/logs")
    avatar_name: str = "unknown"
    model_name: str = "unknown"
    memory_size: int = 1
    use_user_info: bool = False

    def __post_init__(self):
        self.log_file_path = self.log_dir / f"chat-{uuid.uuid4()}.log"

    def set_avatar(
        self,
        avatar_name: str,
        model_key: str,
        memory_size: int,
        template: str,
        use_user_info: bool,
        use_assistant_info: bool,
        template_registry: dict[str, ChatTemplate] | None = None,
        stopper: str | None = None,
    ) -> tuple[str, list]:
        """Initializes the avatar with the given parameters

        This process is a heavy operation and should be carefully handled.

        Args:
            avatar_name (str): The name of the avatar
            model_key (str): The key of the model
            template_style (str): The style of the template
            memory_size (int): The size of the memory
            use_user_info (bool): Whether to use user info
            use_assistant_info (bool): Whether to use assistant info

        Returns:
            tuple[str, list]: The response and the chat history
        """
        model_name = get_latest_checkpoint(model_registry[model_key]["name"])
        # template_style = model_registry[model_key]["template"]
        if template != model_registry[model_key]["template"]:
            gr.Warning(
                f"The template style you selected is not the same as the template style the model was trained with. The model was trained with {model_registry[model_key]['template']}."
            )

        if self.model_name == model_name:
            gr.Info(f"{avatar_name} is already in the room😙")
            return gr.update(interactive=True, placeholder="Type your message here"), []
        else:
            gr.Info(f"{avatar_name} is entering the room...")

            if hasattr(self, "avatar"):
                logger.info("Clearing cache...")
                self.avatar.sleep()
                logger.success("Cache cleared")

            else:
                logger.info("No model to clear cache")
            logger.info(f"Loading {avatar_name}...")

            template_kwargs = {}
            template_cls = template_registry[template]
            if hasattr(template_cls, "user_info"):
                template_kwargs["use_user_info"] = use_user_info
            if hasattr(template_cls, "assistant_info"):
                template_kwargs["use_assistant_info"] = use_assistant_info

            self.avatar = Avatar(
                name=avatar_name,
                model_name=model_name,
                memory_size=memory_size,
                template=template,
                template_registry=template_registry,
                template_kwargs=template_kwargs,
                data_dir=str(self.profile_dir),
                db_dir=str(self.db_dir),
                stopper=stopper,
            )

            self.avatar_name = avatar_name
            self.memory_size = memory_size
            self.use_user_info = use_user_info
            self.use_assistant_info = use_assistant_info
            self.model_name = model_name

            self.avatar.clear()

            gr.Info(f"{avatar_name} entered the room💕")

            return gr.update(interactive=True, placeholder="Type your message here"), []

    def update_avatar_name(self, avatar_name) -> None:
        if hasattr(self, "avatar"):
            self.avatar.set(name=avatar_name)
            self.avatar_name = avatar_name
            gr.Info(f"{avatar_name} is now in the room💕")

        else:
            logger.warning("You need to set the avatar first")

    def update_model_name(self):
        gr.Info("Please click 'invite' to load the new model")
        return gr.update(
            interactive=False, placeholder="Please click 'invite' to load the new model"
        )

    def update_memory_size(self, memory_size):
        self.avatar.memory_size = memory_size
        self.memory_size = memory_size

    def update_use_user_info(self, use_user_info):
        self.use_user_info = use_user_info
        if use_user_info:
            order = self.avatar.dialog.template.order
            order.insert(order.index("assistant_info") + 1, "user_info")
            self.avatar.dialog.template.reorder(order)
        else:
            self.avatar.dialog.template.remove_by_name("user_info")
        return gr.update(interactive=True, placeholder="Type your info here")

    def update_stopper(self, stopper: str):
        if hasattr(self, "avatar"):
            self.avatar.set_stopper(stopper)

    def clear_history(self):
        if hasattr(self, "avatar"):
            self.avatar.clear()
            return "", []
        else:
            logger.warning("You need to set the avatar first")
            gr.Warning("You need to set the avatar first")

    def avatar_say(
        self,
        max_new_tokens,
        temperature,
        length_penalty,
        repetition_penalty,
        top_p,
        top_k,
        chat_history,
        use_user_info,
        user_info,
        use_assistant_info,
        rag_k,
    ) -> tuple[str, list, str]:
        if hasattr(self, "avatar"):
            if self.avatar is None:
                gr.Warning("Please invite an avatar first😝")
                return "", chat_history, ""
        else:
            gr.Warning("Please invite an avatar first😝")
            return "", chat_history, ""

        prompt_kwargs = {}
        if use_user_info:
            prompt_kwargs["user_info"] = user_info
        if use_assistant_info:
            prompt_kwargs["rag_k"] = rag_k

        bot_message = self.avatar.say(
            gen_kwargs={
                "max_new_tokens": max_new_tokens,
                "temperature": temperature,
                "length_penalty": length_penalty,
                "repetition_penalty": repetition_penalty,
                "top_p": top_p,
                "top_k": top_k,
            },
            prompt_kwargs=prompt_kwargs,
            stream=True,
        )
        chat_history.append([None, bot_message])

        # self._write(self.avatar.dialog.text)
        self._log(chat_history)

        return "", chat_history, self.avatar.input_prompt

    def avatar_generate(
        self,
        message: str,
        max_new_tokens: int,
        temperature: float,
        length_penalty: float,
        repetition_penalty: float,
        top_p: float,
        top_k: int,
        chat_history,
    ) -> tuple[str, str, list]:
        if hasattr(self, "avatar"):
            if self.avatar is None:
                gr.Warning("Please invite an avatar first😝")
                return "", "", ([None, None])
        else:
            gr.Warning("Please invite an avatar first😝")
            return "", "", ([None, None])

        bot_message = self.avatar.generate(
            message,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            length_penalty=length_penalty,
            repetition_penalty=repetition_penalty,
            top_p=top_p,
            top_k=top_k,
            stream=True,
        )

        history = message + bot_message
        chat_history.clear()
        chat_history.append([None, None])

        self._write(history)

        return (bot_message, message, chat_history)

    def user_respond(
        self,
        message: str,
        chat_history: list,
    ):
        if hasattr(self, "avatar"):
            self.avatar.hear(Utterance(content=message, speaker="user"))
            chat_history.append([message, None])
            return "", chat_history
        else:
            return "", ([None, None])

    def _write(self, history_text: str):
        text = "\n"
        text += "=" * 100 + "\n"
        text += f"Logging to {self.log_file_path}\n"
        text += "=" * 100 + "\n"
        text += f"Avatar: {self.avatar_name}\n"
        text += "=" * 100 + "\n"
        text += f"Model: {self.model_name}\n"
        text += "=" * 100 + "\n"
        text += "History: \n"
        text += "-" * 100 + "\n"
        text += f"{history_text}\n"
        text += "-" * 100 + "\n"

        with open(self.log_file_path, "w") as f:
            f.write(text)

    def _log(self, chat_history):
        history = "\n"
        history += "=" * 100 + "\n"
        history += f"Logging to {self.log_file_path}\n"
        history += "=" * 100 + "\n"
        history += f"Avatar: {self.avatar_name}\n"
        history += "=" * 100 + "\n"
        history += f"Model: {self.model_name}\n"
        history += "=" * 100 + "\n"
        for chat in chat_history:
            if chat[0] is not None:
                history += f"Human: {chat[0]}\n"
                history += "-" * 100 + "\n"
            if chat[1] is not None:
                history += f"AI: {chat[1]}\n"
                history += "-" * 100 + "\n"

        with open(self.log_file_path, "w") as f:
            f.write(history)

    def export(self, chat_history: list):
        gr.Info(f"Successfully exported chat history to {self.log_file_path}📜")
        return chat_history

    def apply_settings(self, profile_dir, db_dir, log_dir):
        self.profile_dir = profile_dir
        self.db_dir = db_dir
        self.log_dir = log_dir
        self.log_file_path = self.log_dir / f"chat-{uuid.uuid4()}.log"
        return self.profile_dir, self.db_dir, self.log_dir
