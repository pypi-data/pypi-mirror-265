import json
import uuid
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Literal

import pandas as pd
from loguru import logger

from spchat.prompts import ChatTemplate, get_template

SPEAKERS = ["assistant", "user"]


@dataclass
class Speaker:
    name: str
    id: str

    def __eq__(self, other):
        return self.id == other.id


@dataclass
class Utterance:
    speaker: str
    content: str

    def __post_init__(self):
        self._timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._id = uuid.uuid4()
        # self._speaker_id  # TODO: implement speaker id (use x user id?)

    @property
    def id(self):
        return str(self._id)

    @property
    def timestamp(self):
        return self._timestamp

    def __repr__(self):
        return f"Utterance({self.speaker}: {self.content})"

    def add(
        self,
        utterance: "Utterance",
        linebreak_op=Literal[None, "add", "remove"],
        whitespace_op=Literal[None, "add", "remove"],
    ):
        assert self.speaker == utterance.speaker, "Speakers must be the same"
        if linebreak_op == "remove" and whitespace_op is None:
            logger.warning(
                "'remove_line_breaks=True' and 'add_whitespace=False' can only work on the languages that don't use whitespace to separate words such as Chinese, Japanese, and Korean."
            )
        if whitespace_op == "add":
            self.content += " " + utterance.content
        elif whitespace_op == "remove":
            if self.content.endswith(" "):
                self.content = self.content[:-1]
            self.content += utterance.content
        else:
            self.content += utterance.content

        if linebreak_op == "remove":
            self.remove_line_breaks(no_whitespace=True)
        elif linebreak_op == "add":
            raise NotImplementedError(
                "linebreak_op='add' is not implemented yet. Please use linebreak_op='none' or linebreak_op='remove' instead."
            )

    def format(self, template):
        if self.speaker == "assistant":
            return template.format_assistant(self.content)
        elif self.speaker == "user":
            return template.format_user(self.content)
        else:
            return template.format_speaker(speaker=self.speaker, content=self.content)

    def rename(self, new_speaker):
        self.speaker = new_speaker

    def remove_line_breaks(self, no_whitespace=False):
        if no_whitespace:
            self.content = self.content.replace("\n", "")
        else:
            self.content = self.content.replace("\n", " ")

    @staticmethod
    def from_dict(
        message: dict,
        speaker_column: str = "role",
        content_column: str = "content",
        target_speaker: str | list[str] | None = None,
    ):
        if isinstance(target_speaker, list):
            if message[speaker_column] in target_speaker:
                return Utterance(content=message[content_column], speaker="assistant")
            else:
                return Utterance(content=message[content_column], speaker="user")
        elif isinstance(target_speaker, str):
            if message[speaker_column] == target_speaker:
                return Utterance(content=message[content_column], speaker="assistant")
            else:
                return Utterance(content=message[content_column], speaker="user")
        else:
            return Utterance(
                content=message[content_column], speaker=message[speaker_column]
            )

    def to_dict(self, speaker_column="speaker", content_column="content"):
        return {speaker_column: self.speaker, content_column: self.content}

    def to_dialog_data_format(self):
        return {"content": self.content, "role": self.speaker}

    def to_mt_dialog_data_format(self):
        return {"content": self.content, "speaker": self.speaker}


class Memory:
    def __init__(self, history: list[Utterance] | None = None, id: str | None = None):
        if history is None:
            self._history = []
        elif isinstance(history, list):
            self._history = history

        if id is None:
            self._id = str(uuid.uuid4())
        else:
            self._id = id

    def __getitem__(self, idx):
        return self._history[idx]

    def __len__(self):
        return len(self._history)

    def __repr__(self):
        return f"Memory(history={self._history}, id={self._id})"

    def __iter__(self):
        return iter(self._history)

    def add(
        self, utterance: Utterance | str, speaker: str | None, index: int | None = None
    ):
        if isinstance(utterance, str):
            if speaker is None:
                raise ValueError("speaker must be provided when utterance is a string")
            utterance = Utterance(content=utterance, speaker=speaker)
        elif not isinstance(utterance, Utterance):
            raise ValueError(
                "utterance must be a string or an Utterance instance, not "
                + str(type(utterance))
            )
        else:
            if not utterance.speaker or not utterance.content:
                logger.warning(
                    "Utterance must have both speaker and content. Skipping adding utterance."
                )
                return

        if index is not None:
            self._history.insert(index, utterance)
        else:
            self._history.append(utterance)

    def pop(self, idx, inplace=True) -> Utterance | list[Utterance] | None:
        if inplace:
            return self._history.pop(idx)
        else:
            return self._history[:idx] + self._history[idx + 1 :]

    def forget(self, idx_exp: int | str):
        self._history = eval(f"self._history[{idx_exp}]")

    def clear(self):
        self._history = []

    def show(self):
        for u in self._history:
            print(f"{u.speaker}: {u.content}")

    def save(self, path: str = "memory.json"):
        with open(path, "w") as f:
            json.dump(self.to_dict(), f, indent=4, ensure_ascii=False)

    def consolidate(
        self,
        inplace=True,
        whitespace_op=Literal[None, "add", "remove"],
        linebreak_op=Literal[None, "add", "remove"],
    ) -> "Memory":
        uttrs: list[Utterance] = []
        for u in self._history:
            if len(uttrs) == 0:
                uttrs.append(u)
            elif u.speaker == uttrs[-1].speaker:
                uttrs[-1].add(
                    u,
                    whitespace_op=whitespace_op,
                    linebreak_op=linebreak_op,
                )
            else:
                uttrs.append(u)
        if inplace:
            self._history = uttrs
            return self
        else:
            return self.__class__(history=uttrs, id=self._id)

    def to_hqr(
        self, use_last_uttr: bool = False
    ) -> tuple[list[Utterance] | None, Utterance | None, Utterance | None]:
        """Get the history, query, and response

        Args:
            use_last_uttr (bool, optional): Whether to use last user utterance. Defaults to False.

        Returns:
            tuple[list[Utterance] | None, Utterance | None, Utterance | None]: The history, query, and response
        """

        # Messages must have assistant message at the end
        while self._history[-1].speaker != "assistant":
            if self._history[-1].speaker != "assistant" and len(self._history) == 1:
                logger.warning("No assistant message found.")
                return (None, None, None)
            self.pop(-1, inplace=True)

        gathered_dialog = self.gather()

        if len(gathered_dialog.history) > 1:
            query = gathered_dialog.history[-2]
            assert query.speaker == "user"
            response = gathered_dialog.pop(-1)
            history = gathered_dialog
        else:
            query = gathered_dialog.history[-1]
            assert query.speaker == "assistant"
            response = gathered_dialog.pop(-1)
            history = gathered_dialog

        if use_last_uttr:
            last_uttr, history = self.get_last_user_utterance_and_history()
            return history, query, response, last_uttr

        return history, query, response

    def get_last_user_utterance_and_history(
        self,
    ) -> tuple[Utterance | None, list[Utterance]]:
        if "user" in [u.speaker for u in self._history]:
            for u in reversed(self._history):
                if u.speaker == "user":
                    # last_uttr = u
                    # history = self.history[: self.history.index(u)]
                    last_uttr = self.pop(self._history.index(u))
                    return (last_uttr, self)
            raise ValueError("No user utterance found in history")

        else:
            return (None, self)

    def to_dict(self, include_id=False, history_column="messages"):
        d = {}
        if include_id:
            d["id"] = self.id
        d[history_column] = [u.to_dict() for u in self._history]
        d["speakers"] = self.unique_speakers

        return d

    def to_gr_history(self):
        self.consolidate()
        gr_history = []
        for u in self.history:
            if u.speaker == "assistant":
                gr_history.append([None, u.content])
            elif u.speaker == "user":
                gr_history.append([u.content, None])
            else:
                raise NotImplementedError(
                    "Speaker type not supported in gather_response history"
                )
        return gr_history

    @property
    def id(self):
        return str(self._id)

    @property
    def history(self) -> list[Utterance]:
        return self._history

    @property
    def history_content(self) -> list[str]:
        return [u.content for u in self._history]

    @property
    def query(self) -> Utterance | None:
        """The last not assistant utterance"""

        if self._history:
            for u in reversed(self._history):
                if u.speaker != "assistant":
                    return u
                elif u.speaker == "assistant":
                    continue
        else:
            return None

    @property
    def size(self) -> int:
        return len(self._history)

    @property
    def unique_speakers(self) -> list[str]:
        return sorted(list(set([u.speaker for u in self._history])))


class Dialog:
    def __init__(
        self,
        template: ChatTemplate | str,
        template_registry: dict[str, ChatTemplate] | None = None,
        memory: Memory | list[Utterance] | None = None,
        **kwargs,
    ):
        self.set_template(template, template_registry, **kwargs)

        if isinstance(memory, list):
            self._memory = Memory(history=memory)
        elif isinstance(memory, Memory):
            self._memory = memory
        elif memory is None:
            self._memory = Memory()
        else:
            raise ValueError(
                f"memory must be a list of Utterance instances or a Memory instance, not {type(memory)}"
            )

        assert isinstance(self._memory, Memory), "memory must be a Memory instance"

    def __repr__(self):
        return f"Dialog(template={self.template}, memory={self.memory})"

    def __str__(self):
        return self.text

    def __len__(self):
        return len(self.history)

    def __getitem__(self, idx):
        return self.history[idx]

    def __iter__(self):
        return iter(self.history)

    def add(
        self, utterance: Utterance | str, speaker=str | None, index: int | None = None
    ):
        self._memory.add(utterance=utterance, speaker=speaker, index=index)

    def pop(self, idx):
        return self._memory.pop(idx)

    def clear(self):
        self._memory.clear()

    def show(self):
        self._memory.show()

    def rename_speaker(self, speaker: str, new_speaker: str):
        for u in self._memory:
            if u.speaker == speaker:
                u.speaker = new_speaker

    def get_query_and_history(self):
        return self._memory.query, self.history_text_without_query

    def format(self, **kwargs):
        """Format the chat history to be used in a prompt template"""

        if "user_utterance" in self.template.input_variables:
            if self._memory[-1].speaker == "user":
                kwargs["user_utterance"] = self._memory[-1].content
                if len(self._memory) == 1:
                    history = ""
                else:
                    history = self.format_history(
                        memory=self._memory[:-1], template=self.template
                    )
            else:
                kwargs["user_utterance"] = ""

        else:
            history = self.format_history(memory=self._memory, template=self.template)

        prompt = self.template.format(history=history, **kwargs)

        return prompt

    @staticmethod
    def format_history(memory: Memory | list[Utterance], template: ChatTemplate):
        history = ""
        for u in memory:
            history += u.format(template)
        if history.endswith("\n"):
            history = history[:-1]
        return history

    @classmethod
    def format_with_template(
        cls,
        memory: Memory | list[Utterance],
        template: ChatTemplate | str,
        template_registry: dict[str, ChatTemplate] | None = None,
        template_kwargs: dict = {},
        format_kwargs: dict = {},
    ) -> str:
        instance = cls(
            template=template,
            template_registry=template_registry,
            memory=memory,
            **template_kwargs,
        )
        prompt = instance.format(**format_kwargs)
        return prompt

    def consolidate(self, **kwargs):
        self.memory.consolidate(inplace=True, **kwargs)

    def set_template(
        self,
        template: ChatTemplate | str,
        template_registry: dict[str, ChatTemplate] | None = None,
        **kwargs,
    ):
        self.template = get_template(template, template_registry, **kwargs)

    def from_list(
        self,
        messages: dict | list[list[str]],
        speaker_column: str = "role",
        target_speaker: str | list[str] | int | None = None,
    ):
        for message in messages:
            if isinstance(message, dict):
                if not isinstance(target_speaker, int):
                    self.add(
                        Utterance.from_dict(
                            message,
                            speaker_column=speaker_column,
                            target_speaker=target_speaker,
                        )
                    )
                # else:
                #     self.add(
                #         Utterance.from_dict(
                #             message,
                #         )
                #     )
            elif isinstance(message, list):
                self.add(
                    Utterance(
                        content=message[1],
                        speaker=(
                            "assistant" if message[0] in ["AI", "assistant"] else "user"
                        ),
                    )
                )

        return self

    def to_dict(self):
        return self._memory.to_dict()

    def to_dialog_data_format(self):
        return [u.to_dialog_data_format() for u in self.history]

    def to_mt_dialog_data_format(self):
        return [u.to_mt_dialog_data_format() for u in self.history]

    @property
    def history(self) -> list[Utterance]:
        return self._memory.history

    @property
    def history_content(self) -> list[str]:
        return self._memory.history_content

    @property
    def history_text(self) -> str:
        return self.format_history(memory=self._memory, template=self.template)

    @property
    def query(self) -> Utterance | None:
        return self._memory.query

    @property
    def history_text_without_query(self) -> str | None:
        """The history without the last not assistant utterance"""

        if self.query:
            return self.history_text.replace(self.query.format(self.template), "")
        else:
            return self.history_text

    @property
    def id(self):
        return self._memory.id

    @property
    def memory(self):
        return self._memory

    @property
    def unique_speakers(self) -> list[str]:
        return self._memory.unique_speakers


@dataclass
class DialogDataFormat:
    assistant_id: str
    messages: list[dict] | Dialog
    num_assistant_utters: int
    num_user_utters: int
    assistant_min: int
    assistant_max: int
    user_min: int | None
    user_max: int | None
    assistant_chara: str | None
    assistant_info: str | None
    query: dict | Utterance | None
    template: ChatTemplate | str
    template_registry: dict[str, ChatTemplate] = field(default_factory=dict)
    template_kwargs: dict = field(default_factory=dict)
    note: str | None = None

    def __repr__(self):
        return f"DialogDataFormat(assistant_id={self.assistant_id}, messages={self.messages}, num_assistant_utters={self.num_assistant_utters}, num_user_utters={self.num_user_utters}, assistant_min={self.assistant_min}, assistant_max={self.assistant_max}, user_min={self.user_min}, user_max={self.user_max}, assistant_chara={self.assistant_chara}, assistant_info={self.assistant_info}, query={self.query}, template={self.template}, note={self.note})"

    def __post_init__(self):
        if isinstance(self.messages, list):
            self.messages = Dialog(
                template=self.template,
                template_registry=self.template_registry,
                **self.template_kwargs,
            ).from_list(self.messages)
        if isinstance(self.query, Utterance):
            self.query = self.query.to_dialog_data_format()

    def to_dict(self):
        if isinstance(self.messages, Dialog):
            self.messages = self.messages.to_dialog_data_format()
        if isinstance(self.query, Utterance):
            self.query = self.query.to_dialog_data_format()
        return asdict(self)

    @classmethod
    def from_dict(cls, data, template_style: str, **kwargs):
        kwargs = {}
        for k, v in data.items():
            if k == "messages" and isinstance(v, list):
                kwargs[k] = Dialog(template_style=template_style, **kwargs).from_list(v)
            elif k == "query" and v:
                kwargs[k] = Utterance.from_dict(v)

            elif k in DialogDataFormat.__annotations__:
                kwargs[k] = v
            else:
                logger.warning(f"Key {k} not found in DialogDataFormat annotations")
        return cls(**kwargs)

    @property
    def text(self) -> str:
        return self.messages.text


@dataclass
class MultiTurnDialogDataFormat:
    messages: list[dict] | Dialog
    speakers: list[str]
    num_messages: int
    min: int
    max: int
    note: str | None = None
    target_speaker: str | list[str] | None = None
    template: ChatTemplate | str | None = None
    template_registry: dict[str, ChatTemplate] | None = None
    template_kwargs: dict = field(default_factory=dict)
    do_split: bool = False

    def __repr__(self):
        return f"MultiTurnDialogDataFormat(messages={self.messages}, speakers={self.speakers}, num_messages={self.num_messages}, min={self.min}, max={self.max}, note={self.note})"

    def __post_init__(self):
        if isinstance(self.messages, list):
            if self.do_split:
                self.response = self.messages.pop(-1)
            self.messages = [
                Dialog(
                    template=self.template,
                    template_registry=self.template_registry,
                    **self.template_kwargs,
                ).from_list(
                    m, speaker_column="speaker", target_speaker=self.target_speaker
                )
                for m in self.messages
            ]
        else:
            if self.do_split:
                self.response = self.messages.pop(-1)

    def to_dict(self):
        if isinstance(self.messages, list):
            self.messages = [m.to_dict() for m in self.messages]
        return asdict(self)

    @classmethod
    def from_dict(
        cls,
        data,
        template: ChatTemplate | str,
        template_registry: dict[str, ChatTemplate] | None = None,
        template_kwargs: dict = {},
        target_speaker: str | list[str] | None = None,
        do_split: bool = False,
    ):
        kwargs = {}
        for k, v in data.items():

            if k == "messages" and isinstance(v, list):
                kwargs[k] = Dialog(
                    template=template,
                    template_registry=template_registry,
                    **template_kwargs,
                ).from_list(
                    v,
                    speaker_column="speaker",
                    target_speaker=target_speaker,
                )

            elif k in MultiTurnDialogDataFormat.__annotations__:
                kwargs[k] = v
            else:
                logger.warning(
                    f"Key {k} not found in MultiTurnDialogDataFormat annotations"
                )
        kwargs["do_split"] = do_split
        return cls(**kwargs)

    @property
    def history(self) -> str:
        return self.messages.text

    @property
    def text(self, **kwargs) -> str:
        return self.messages.format(**kwargs)

    def to_prompt_and_response(self, **kwargs) -> tuple[str, str]:
        return self.messages.format(**kwargs), self.response.content


class DialogData(ABC):
    @staticmethod
    def get_prompts_by_user(
        df: pd.DataFrame,
        user_name: str,
        user_column: str = "user",
        query_column: str = "prompt",
    ):
        filtered_df = df[df[user_column] == user_name]
        return filtered_df[query_column].tolist()

    def check_file_exist(self, src_file):
        src_file = Path(src_file)
        if src_file.exists():
            if src_file.suffix == ".json":
                try:
                    with open(src_file, "r") as f:
                        json.load(f)
                        return True
                except json.JSONDecodeError:
                    logger.error(f"File {src_file} exists but is not a valid JSON file")
                    return False

            elif src_file.suffix == ".jsonl":
                try:
                    pd.read_json(src_file, lines=True)
                    return True
                except json.JSONDecodeError:
                    logger.error(
                        f"File {src_file} exists but is not a valid JSONL file"
                    )
                    return False

            elif src_file.suffix == ".csv":
                try:
                    pd.read_csv(src_file)
                    return True
                except pd.errors.ParserError:
                    logger.error(f"File {src_file} exists but is not a valid CSV file")
                    return False

            elif src_file.suffix == ".txt":
                return True

        else:
            logger.warning(f"File {src_file} not found.")
            return False

    @abstractmethod
    def generate_dataset(self):
        pass

    @staticmethod
    def get_min_max_lengths(dialog: Dialog) -> tuple[int, int, int, int]:
        assistant_min = 1e5
        assistant_max = 0
        user_min = 1e5
        user_max = 0

        for u in dialog.history:
            if u.speaker == "assistant":
                assistant_min = min(int(assistant_min), len(u.content))
                assistant_max = max(assistant_max, len(u.content))
            elif u.speaker == "user":
                user_min = min(int(user_min), len(u.content))
                user_max = max(user_max, len(u.content))

        assert assistant_min != 1e5, "No assistant messages found"
        assert user_min != 1e5, "No user messages found"

        return assistant_min, assistant_max, user_min, user_max
