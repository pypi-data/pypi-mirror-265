from ..prompts import (
    ChatTemplate,
    DialogWithLastUserResponseMixin,
    HumanAIHistoryMixin,
    Section,
    SimpleDialogMixin,
)


class SpiralPrompterV1(ChatTemplate, HumanAIHistoryMixin, SimpleDialogMixin):
    basis = Section(
        name="basis",
        content="""\
あなた(AI)は、与えられた特徴や参照情報に基づいて様々なキャラクターを演じることができる、非常に優秀な俳優です。会話履歴に基づいて会話してください。

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
