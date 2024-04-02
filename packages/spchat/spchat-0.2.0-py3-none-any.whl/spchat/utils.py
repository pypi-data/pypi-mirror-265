import re

import pandas as pd
from datasets import Dataset, load_dataset
from loguru import logger
from tqdm import tqdm

from .chat import DialogDataFormat, MultiTurnDialogDataFormat
from .prompts import ChatTemplate


def get_hereafter(prompt, query, include_query=False):
    index = prompt.find(query)

    if index != -1:
        result_text = prompt[index:]
        if not include_query:
            result_text = result_text[len(query) :]
        return result_text
    else:
        logger.warning(f"Could not find the specified string: {query} in the prompt.")
        return None


def get_speaker_lines(data, assistant_prefix, user_prefix, criteria):
    prompt = data["prompt"]
    response = data["response"]
    prompt = prompt.replace("\n", "")

    prompt = prompt.replace(assistant_prefix, f"\n{assistant_prefix}")
    prompt = prompt.replace(user_prefix, f"\n{user_prefix}")
    for c in criteria:
        prompt = prompt.replace(c, f"\n{c}")

    assistant_lines = re.findall(rf"{assistant_prefix}(.+)", prompt)
    user_lines = re.findall(rf"{user_prefix}(.+)", prompt)

    assistant_lines.append(response)

    return assistant_lines, user_lines


def filter_turn(cls, target, dataset, assistant_prefix, user_prefix, criteria):
    results = []
    for d in tqdm(dataset):
        assistant_lines, user_lines = cls.get_speaker_lines(
            d, assistant_prefix, user_prefix, criteria
        )
        match target:
            case "single":
                if len(user_lines) == 0:
                    results.append(d)
            case "multi":
                if len(user_lines) >= 1 and len(assistant_lines) >= 1:
                    results.append(d)
            case _:
                raise ValueError("Turn target must be 'single' or 'multi'")

    return Dataset.from_list(results)


def filter_length(
    self,
    dataset,
    target="both",
    min_length=None,
    max_length=None,
    assistant_prefix=None,
    user_prefix=None,
    criteria=None,
):

    def len_lines(lines):
        return [len(line) for line in lines]

    results = []
    for d in tqdm(dataset):
        assistant_lines, user_lines = self.get_speaker_lines(
            d, assistant_prefix, user_prefix, criteria
        )
        try:
            user_min = min(len_lines(user_lines))
            user_max = max(len_lines(user_lines))

        except ValueError:
            user_min = 0
            user_max = 0

        assistant_min = min(len_lines(assistant_lines))
        assistant_max = max(len_lines(assistant_lines))

        match target:
            case "both":
                if min_length:
                    if user_min < min_length or assistant_min < min_length:
                        continue
                if max_length:
                    if user_max > max_length or assistant_max > max_length:
                        continue
            case "assistant":
                if min_length:
                    if assistant_min < min_length:
                        continue
                if max_length:
                    if assistant_max > max_length:
                        continue

            case "user":
                if min_length:
                    if user_min < min_length:
                        continue
                if max_length:
                    if user_max > max_length:
                        continue

        results.append(d)

    return Dataset.from_list(results)


def get_mt_ds(dataset, min_length, max_length=130):
    results = []
    for d in tqdm(dataset):
        ai_lines, human_lines = get_speaker_lines(
            d, "AI: ", "Human: ", ["### 応答:", "### 入力:"]
        )

        num_ai = len(ai_lines)
        num_human = len(human_lines)

        # min length of ai_lines
        ai_min = min([len(line) for line in ai_lines])
        ai_max = max([len(line) for line in ai_lines])
        # min length of human_lines
        try:
            human_min = min([len(line) for line in human_lines])
            human_max = max([len(line) for line in human_lines])
        except ValueError:
            human_min = 0
            human_max = 0

        if num_ai > 0 and num_human > 0:  # multi-turn conversation
            pass

        else:
            continue

        if (
            ai_min > min_length
            and ai_max < max_length
            and human_min > min_length
            and human_max < max_length
        ):
            results.append(d)

    df = pd.DataFrame(results)
    df.to_json(
        "tmp.jsonl",
        orient="records",
        lines=True,
        force_ascii=False,
    )
    ds = load_dataset("json", data_files="tmp.jsonl")
    return ds


def to_prompt(data, template: str, **kwargs):
    data = DialogDataFormat.from_dict(data, template=template)
    prompter = template(**kwargs)
    prompt, response = prompter.format_from_dialog_data(data)
    return {"prompt": prompt + response.content}


def to_mt_prompt(
    data,
    template: ChatTemplate | str,
    template_registry: dict[str, ChatTemplate] = {},
    target_speaker: str | list[str] | None = None,
    do_split: bool = False,
    **kwargs,
):
    data = MultiTurnDialogDataFormat.from_dict(
        data,
        template=template,
        template_registry=template_registry,
        target_speaker=target_speaker,
        template_kwargs=kwargs,
        do_split=do_split,
    )  # FIXME: implement format_from_mt_dialog_data
    if do_split:
        prompt, response = data.to_prompt_and_response()
        return {"prompt": prompt + response}
    else:
        return {"prompt": data.text}


def add_eos_token(tokenizer, prompt_column="prompt", **kwargs):
    def func(example):
        prompts = []
        for i in range(len(example[prompt_column])):
            prompt = example[prompt_column][i]
            text = f"{prompt}{tokenizer.eos_token}"
            prompts.append(text)
        return prompts

    return func


def do_nothing(prompt_column="prompt", **kwargs):
    def func(example):
        prompts = []
        for i in range(len(example[prompt_column])):
            prompt = example[prompt_column][i]
            prompts.append(prompt)
        return prompts

    return func
