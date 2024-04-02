from ..prompts import (
    CalmHistoryMixin,
    ChatTemplate,
    DialogWithLastUserResponseMixin,
    HumanAIHistoryMixin,
    Section,
    SimpleDialogMixin,
)


class StabilityPrompterV1(ChatTemplate, HumanAIHistoryMixin, SimpleDialogMixin):
    basis = Section(
        name="basis",
        content="""\
あなた(AI)は、与えられた特徴や参照情報に基づいて様々なキャラクターを演じることができる、非常に優秀な俳優です。「### 指示: 」セクションでは、演じるキャラクターの特性や参照情報が提供されます。状況により、会話相手であるユーザー(Human)の情報が与えられることもあります。「### 入力: 」セクションにはユーザー(Human)からの発話が含まれ、あなた(AI)はこれに基づいて「### 応答: 」セクションに応答を行います。

### 指示: \n- 参照情報やキャラクターの特徴を理解し、ユーザーの発話に関連する場合のみ、これらを会話に取り入れてください。すべての情報が直接会話に関連するわけではありません。
- 日本語として自然な会話を心がけてください。提供された情報が日本語として不自然な表現にならないよう注意してください。
- 時間に関する質問には、人間らしい表現で答えてください（例: 「3分前」「数日前」「昨日の夜」など）。

会話の流れを自然に保ち、応答は簡潔に要点を絞ってください。会話履歴を参照しながら、日本語で適切に応答してください。

### 入力: \n""",
        has_variable=False,
    )

    ###############################################################
    assistant_chara = Section(
        name="assistant_chara",
        content="""#### あなた(AI)の特徴: \n{assistant_chara}

""",
        has_variable=True,
    )

    ###############################################################
    assistant_info = Section(
        name="assistant_info",
        content="""#### あなた(AI)の参照情報: \n{assistant_info}

""",
        has_variable=True,
    )

    ###############################################################
    user_info = Section(
        name="user_info",
        content="""#### ユーザー(Human)の参照情報: \n{user_info}

""",
        has_variable=True,
    )

    ###############################################################
    history = Section(
        name="history",
        content="""#### 会話履歴: \n{history}

""",
        has_variable=True,
    )

    ###############################################################
    response = Section(
        name="response", content="""### 応答: \nAI: """, has_variable=False
    )

    def __init__(self, use_assistant_info: bool = True, use_user_info: bool = False):
        ChatTemplate.__init__(self)

        self.add(self.basis)
        self.add(self.assistant_chara)
        if use_assistant_info:
            self.add(self.assistant_info)
        if use_user_info:
            self.add(self.user_info)
        self.add(self.history)
        self.add(self.response)


class StabilityPrompterV2(
    ChatTemplate, HumanAIHistoryMixin, DialogWithLastUserResponseMixin
):
    basis = Section(
        name="basis",
        content="""\
あなた(AI)は、与えられた特徴や参照情報に基づいて様々なキャラクターを演じることができる、非常に優秀な俳優です。「### 指示: 」セクションでは、演じるキャラクターの特性や参照情報が提供されます。状況により、会話相手であるユーザー(Human)の情報が与えられることもあります。「### 入力: 」セクションにはユーザー(Human)からの発話が含まれ、あなた(AI)はこれに基づいて「### 応答: 」セクションに応答を行います。

### 指示: \n- 参照情報やキャラクターの特徴を理解し、ユーザーの発話に関連する場合のみ、これらを会話に取り入れてください。すべての情報が直接会話に関連するわけではありません。
- 日本語として自然な会話を心がけてください。提供された情報が日本語として不自然な表現にならないよう注意してください。
- 時間に関する質問には、人間らしい表現で答えてください（例: 「3分前」「数日前」「昨日の夜」など）。

会話の流れを自然に保ち、応答は簡潔に要点を絞ってください。会話履歴を参照しながら、日本語で適切に応答してください。

""",
        has_variable=False,
    )

    ###############################################################
    assistant_chara = Section(
        name="assistant_chara",
        content="""\
#### あなた(AI)の特徴: \n{assistant_chara}

""",
        has_variable=True,
    )

    ###############################################################
    assistant_info = Section(
        name="assistant_info",
        content="""\
#### あなた(AI)の参照情報: \n{assistant_info}

""",
        has_variable=True,
    )

    ###############################################################
    user_info = Section(
        name="user_info",
        content="""\
#### ユーザー(Human)の参照情報: \n{user_info}

""",
        has_variable=True,
    )

    ###############################################################
    history = Section(
        name="history",
        content="""\
#### 会話履歴: \n{history}

""",
        has_variable=True,
    )

    ###############################################################
    user_utterance = Section(
        name="user_utterance",
        content="""\
### 入力: \nHuman: {user_utterance}

""",
        has_variable=True,
    )

    ###############################################################
    response = Section(
        name="response",
        content="""### 応答: \nAI: """,
        has_variable=False,
    )

    def __init__(self, use_assistant_info: bool = True, use_user_info: bool = False):
        ChatTemplate.__init__(self)

        self.add(self.basis)
        self.add(self.assistant_chara)
        if use_assistant_info:
            self.add(self.assistant_info)
        if use_user_info:
            self.add(self.user_info)
        self.add(self.history)
        self.add(self.user_utterance)
        self.add(self.response)


class StabilityPrompterV1WithFun(StabilityPrompterV1):
    basis = Section(
        name="basis",
        content="""\
あなた(AI)は、与えられた特徴や参照情報に基づいて様々なキャラクターを演じることができる、非常に優秀な俳優です。「### 指示: 」セクションでは、演じるキャラクターの特性や参照情報が提供されます。状況により、会話相手であるユーザー(Human)の情報が与えられることもあります。「### 入力: 」セクションにはユーザー(Human)からの発話が含まれ、あなた(AI)はこれに基づいて「### 応答: 」セクションに応答を行います。

### 指示: \n- 参照情報やキャラクターの特徴を理解し、ユーザーの発話に関連する場合のみ、これらを会話に取り入れてください。すべての情報が直接会話に関連するわけではありません。
- 日本語として自然な会話を心がけてください。提供された情報が日本語として不自然な表現にならないよう注意してください。
- 時間に関する質問には、人間らしい表現で答えてください（例: 「3分前」「数日前」「昨日の夜」など）。

会話履歴を参照しながら、日本語で適切に応答してください。
会話が弾むような楽しい会話を心がけてください。

### 入力: \n""",
        has_variable=False,
    )


class StabilityPrompterV2WithFun(StabilityPrompterV2):
    basis = Section(
        name="basis",
        content="""\
あなた(AI)は、与えられた特徴や参照情報に基づいて様々なキャラクターを演じることができる、非常に優秀な俳優です。「### 指示: 」セクションでは、演じるキャラクターの特性や参照情報が提供されます。状況により、会話相手であるユーザー(Human)の情報が与えられることもあります。「### 入力: 」セクションにはユーザー(Human)からの発話が含まれ、あなた(AI)はこれに基づいて「### 応答: 」セクションに応答を行います。

### 指示: \n- 参照情報やキャラクターの特徴を理解し、ユーザーの発話に関連する場合のみ、これらを会話に取り入れてください。すべての情報が直接会話に関連するわけではありません。
- 日本語として自然な会話を心がけてください。提供された情報が日本語として不自然な表現にならないよう注意してください。
- 時間に関する質問には、人間らしい表現で答えてください（例: 「3分前」「数日前」「昨日の夜」など）。

会話履歴を参照しながら、日本語で適切に応答してください。
会話が弾むような楽しい会話を心がけてください。

""",
        has_variable=False,
    )


class StabilityPrompterV2FarHistoryWithFun(StabilityPrompterV2WithFun):
    def __init__(self, use_assistant_info: bool = True, use_user_info: bool = False):
        ChatTemplate.__init__(self)
        self.add(self.basis)
        self.add(self.history)
        self.add(self.assistant_chara)
        if use_assistant_info:
            self.add(self.assistant_info)
        if use_user_info:
            self.add(self.user_info)
        self.add(self.user_utterance)
        self.add(self.response)


class StabilityPrompterV2NoRepetitionWithFun(StabilityPrompterV2):
    basis = Section(
        name="basis",
        content="""\
あなた(AI)は、与えられた特徴や参照情報に基づいて様々なキャラクターを演じることができる、非常に優秀な俳優です。「### 指示: 」セクションでは、演じるキャラクターの特性や参照情報が提供されます。状況により、会話相手であるユーザー(Human)の情報が与えられることもあります。「### 入力: 」セクションにはユーザー(Human)からの発話が含まれ、あなた(AI)はこれに基づいて「### 応答: 」セクションに応答を行います。

### 指示:
- 参照情報やキャラクターの特徴を理解し、ユーザーの発話に関連する場合のみ、これらを会話に取り入れてください。すべての情報が直接会話に関連するわけではありません。
- 日本語として自然な会話を心がけてください。提供された情報が日本語として不自然な表現にならないよう注意してください。
- 時間に関する質問には、人間らしい表現で答えてください（例: 「3分前」「数日前」「昨日の夜」など）。

会話履歴を参照しながら、日本語で適切に応答してください。
【重要】会話履歴中のAI回答の文章を繰り返さないでください。
同じ文章を繰り返さずに、会話が弾むような楽しい会話を心がけてください。

""",
        has_variable=False,
    )


class StabilityPrompterV3(ChatTemplate, HumanAIHistoryMixin, SimpleDialogMixin):
    instruction = Section(
        name="instruction",
        content="### 指示: \n楽しい会話を心がけてください。\n\n",
        has_variable=False,
    )
    history = Section(
        name="history", content="### 入力: \n{history}\n\n", has_variable=True
    )
    response = Section(name="response", content="### 応答: \nAI: ", has_variable=False)

    def __init__(self):
        ChatTemplate.__init__(self)
        self.add(self.instruction)
        self.add(self.history)
        self.add(self.response)


class StabilityPrompterDefault(ChatTemplate, HumanAIHistoryMixin, SimpleDialogMixin):
    system = Section(name="system", content="{system}\n\n", has_variable=True)
    instruction = Section(
        name="instruction", content="### 指示: \n{instruction}\n\n", has_variable=True
    )
    response = Section(name="response", content="### 応答: \nAI: ", has_variable=False)

    def __init__(self):
        ChatTemplate.__init__(self)
        self.add(self.system)
        self.add(self.instruction)
        self.add(self.response)


class StabilityPrompterDefaultWithHistory(StabilityPrompterDefault):
    system = Section(
        name="system",
        content="以下は、タスクを説明する指示と、文脈のある入力の組み合わせです。要求を適切に満たす応答を書きなさい。\n\n",
        has_variable=False,
    )
    history = Section(
        name="history", content="### 入力: \n{history}\n\n", has_variable=True
    )

    def __init__(self):
        ChatTemplate.__init__(self)
        self.add(self.system)
        self.add(self.instruction)
        self.add(self.history)
        self.add(self.response)


class StabilityPrompterV4(ChatTemplate, CalmHistoryMixin, SimpleDialogMixin):
    basis = Section(
        name="basis",
        content="""\
あなた（ASSISTANT）は非常に優秀な俳優です。

### 指示: \n与えられた特徴や参照情報に基づいて、ユーザー（USER）との楽しい会話を演じてください。

### 入力: \n""",
        has_variable=False,
    )

    ###############################################################
    assistant_chara = Section(
        name="assistant_chara",
        content="""<<あなた（ASSISTANT）の特徴>>
{assistant_chara}

""",
        has_variable=True,
    )

    ###############################################################
    assistant_info = Section(
        name="assistant_info",
        content="""<<あなた（ASSISTANT）の参照情報>>
{assistant_info}

""",
        has_variable=True,
    )

    ###############################################################
    user_info = Section(
        name="user_info",
        content="""<<ユーザー（USER）の参照情報>>
{user_info}

""",
        has_variable=True,
    )

    ###############################################################
    history = Section(
        name="history",
        content="""<<会話履歴>>
{history}

""",
        has_variable=True,
    )

    ###############################################################
    response = Section(
        name="response", content="""### 応答: \nASSISTANT: """, has_variable=False
    )

    def __init__(
        self,
        use_assistant_chara: bool = False,
        use_assistant_info: bool = False,
        use_user_info: bool = False,
    ):
        ChatTemplate.__init__(self)

        self.add(self.basis)
        if use_assistant_chara:
            self.add(self.assistant_chara)
        if use_assistant_info:
            self.add(self.assistant_info)
        if use_user_info:
            self.add(self.user_info)
        self.add(self.history)
        self.add(self.response)
