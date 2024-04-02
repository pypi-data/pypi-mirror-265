from ..prompts import ChatTemplate, Section, SimpleDialogMixin, UserAssistantMixin


class Calm2Template(ChatTemplate, UserAssistantMixin, SimpleDialogMixin):
    history = Section(
        name="history",
        content="{history}",
        has_variable=True,
    )
    response = Section(name="response", content="", has_variable=False)

    def __init__(self):
        ChatTemplate.__init__(self)
        self.add(self.history)
        self.add(self.response)
