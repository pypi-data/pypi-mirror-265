from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class Section:
    name: str
    content: str
    has_variable: bool

    def __str__(self):
        return self.content

    def __repr__(self):
        return self.content


@dataclass
class ChatTemplate:
    sections: list[Section] = field(default_factory=list)
    input_variables: list[str] = field(default_factory=list)

    #     def __post_init__(self):
    #         attr_err = AttributeError(
    #             """The template you passed does not have `format_speaker` method.
    # The easy way to implement this is to use spchat.template.HistoryMixin"""
    #         )
    #         if hasattr(self, "format_speaker"):
    #             raise attr_err
    #         if hasattr(self, "format_user"):
    #             raise attr_err
    #         if hasattr(self, "format_assistant"):
    #             raise attr_err

    def __str__(self):
        return "".join([str(section) for section in self.sections])

    def __repr__(self):
        return f"ChatTemplate(sections={self.sections}, input_variavles={self.input_variables})"

    def add(self, section: Section):
        self.sections.append(section)
        if section.has_variable:
            self.input_variables.append(section.name)

    def remove(self, section: Section):
        self.sections.remove(section)
        if section.has_variable:
            self.input_variables.remove(section.name)

    def remove_by_name(self, name: str):
        for section in self.sections:
            if section.name == name:
                self.sections.remove(section)
                if section.has_variable:
                    self.input_variables.remove(section.name)

    def reorder(self, order: list[str]):
        self.sections = []
        self.input_variables = []
        for s in order:
            self.sections.append(getattr(self, s))
            if getattr(self, s).has_variable:
                self.input_variables.append(s)

    @property
    def order(self):
        return [section.name for section in self.sections]

    @property
    def template(self):
        return self.__str__()

    def format(self, *args, **kwargs):
        return self.template.format(*args, **kwargs)


def get_template(
    template: ChatTemplate | str,
    template_registry: dict[str, ChatTemplate] | None = None,
    **kwargs,
) -> ChatTemplate:
    if isinstance(template, str):
        if template_registry is None:
            raise ValueError(
                "template_registry must be provided when template is a string"
            )
        elif template not in template_registry:
            raise ValueError(
                f"Template {template} not found in 'template_registry'. 'template_registry' contains {list(template_registry.keys())}"
            )
        return template_registry[template](**kwargs)

    else:
        return template


class HistoryMixin(ABC):
    @abstractmethod
    def format_user(self, content: str) -> str:
        pass

    @abstractmethod
    def format_assistant(self, content: str) -> str:
        pass

    def format_speaker(self, content: str, speaker: str = "anonymous") -> str:
        return f"{speaker}: {content}\n"


class HumanAIHistoryMixin(HistoryMixin):
    def format_user(self, content: str) -> str:
        return f"Human: {content}\n"

    def format_assistant(self, content: str) -> str:
        return f"AI: {content}\n"


class HumanAIHistoryWithEOSMixin(HistoryMixin):
    def __init__(self, tokenizer):
        self.eos_token = tokenizer.eos_token

    def format_user(self, content: str) -> str:
        return f"Human: {content}{self.eos_token}\n"

    def format_assistant(self, content: str) -> str:
        return f"AI: {content}{self.eos_token}\n"


class UserAssistantMixin(HistoryMixin):
    user_prefix = "USER: "
    user_suffix = "\n"
    assistant_prefix = "ASSISTANT: "
    assistant_suffix = "<|endoftext|>\n"
    speaker_suffix = "\n"

    def format_user(self, content: str) -> str:
        return self.user_prefix + content + self.user_suffix

    def format_assistant(self, content: str) -> str:
        return self.assistant_prefix + content + self.assistant_suffix

    def format_speaker(self, content: str, speaker: str = "anonymous") -> str:
        return self.speaker_prefix(speaker) + content + self.speaker_suffix

    def speaker_prefix(self, speaker: str):
        return f"{speaker}: "


class CalmHistoryMixin(HistoryMixin):
    user_prefix = "USER: "
    user_suffix = "\n"
    assistant_prefix = "ASSISTANT: "
    assistant_suffix = "<|endoftext|>\n"
    speaker_suffix = "\n"

    def format_user(self, content: str) -> str:
        return self.user_prefix + content + self.user_suffix

    def format_assistant(self, content: str) -> str:
        return self.assistant_prefix + content + self.assistant_suffix

    def format_speaker(self, content: str, speaker: str = "anonymous") -> str:
        return self.speaker_prefix(speaker) + content + self.speaker_suffix

    def speaker_prefix(self, speaker: str):
        return f"{speaker}: "


class QwenHistoryMixin(HistoryMixin):
    user_prefix = "<|im_start|>user\n"
    user_suffix = "<|im_end|>\n"
    assistant_prefix = "<|im_start|>assistant\n"
    assistant_suffix = "<|im_end|>\n"
    speaker_suffix = "<|im_end|>\n"

    def format_user(self, content: str) -> str:
        return self.user_prefix + content + self.user_suffix

    def format_assistant(self, content: str) -> str:
        return self.assistant_prefix + content + self.assistant_suffix

    def format_speaker(self, content: str, speaker: str = "anonymous") -> str:
        return self.speaker_prefix(speaker) + content + self.speaker_suffix

    def speaker_prefix(self, speaker: str):
        return f"<|im_start|>{speaker}\n"


class ZephyrHistoryMixin(HistoryMixin):
    def format_user(self, content: str) -> str:
        return f"<|user|>\n{content}</s>\n"

    def format_assistant(self, content: str) -> str:
        return f"<|assistant|>\n{content}</s>\n"

    def format_speaker(self, content: str, speaker: str = "anonymous") -> str:
        return f"<|{speaker}|>\n{content}</s>\n"


class DialogHandlerMixin(ABC):
    @abstractmethod
    def format_from_dialog_data(self, data) -> tuple[str, str]:
        pass


class DialogWithLastUserResponseMixin(DialogHandlerMixin):
    def format_from_dialog_data(self, data) -> tuple[str, str]:
        dialog = data.messages
        history, _, response, last_uttr = dialog.split_dialog(use_last_uttr=True)
        data = data.to_dict()
        kwargs = {"history": history.text, "user_utterance": last_uttr}
        for k, v in data.items():
            if k in self.input_variables:
                kwargs[k] = v
        prompt = self.format(**kwargs)
        return prompt, response


class SimpleDialogMixin(DialogHandlerMixin):
    def format_from_dialog_data(self, data) -> tuple[str, str]:
        dialog = data.messages
        history, _, response = dialog.split_dialog(use_last_uttr=False)
        data = data.to_dict()
        kwargs = {"history": history.text}
        for k, v in data.items():
            if k in self.input_variables:
                kwargs[k] = v
        prompt = self.format(**kwargs)
        return prompt, response
