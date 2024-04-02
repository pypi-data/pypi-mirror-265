import datetime
import os
from collections import deque

from peft import PeftModel
from transformers import AutoModelForCausalLM

from spchat import APIChatEngine, ChatEngine


class Session:
    judge_instruction = """\
あなたはプロのラジオパーソナリティーです。
二人の人物による会話を聞いて、会話内容として以下のいずれかの終了条件を満たしているかを判断しください。

====終了条件====
1. 両者が相槌や、肯定だけなど、お互いがそれ以上の会話をする意欲がない場合。（片方が話を展開しようとしている場合は続行してください）
2. 会話の脈絡がない。AとBの発言が食い違っている場合。
3. 会話の内容が３回以上連続して繰り返しになっている場合。

最後の発話のあとに、質問や話を展開する余地がある場合は続行してください。
会話の終了条件を満たしている場合、Terminationと応答してください。
会話の終了条件を満たしていない場合、Continueと応答してください。
返答は返答のテンプレートに従い、それ以外の返答はしないでください。

====返答のテンプレート====
終了判定: (Termination or Continue)
終了条件: (1, 2, 3)

====例====
<<終了条件を満たしている例1（終了条件: 1）>>
A: おはようございます
B: どうも、、、
A: 今日はいい天気ですね
B: そうですね
A: 何か予定はありますか？
B: 特にないです
A: そうですか
B: 特にありません。

<<終了条件を満たしている例2（終了条件: 1）>>
A: 来週どこに行こうか？
B: どこでもいいよ
A: 海とかはどう？
B: いいね！
A: じゃあ、それで決まりだね！あとで連絡するね
B: そうだね！ありがと〜
A: どういたしまして
B: はい！

<<終了条件を満たしていない例1（Continue）>>
B: 醤油ラーメンですか、いいですね！チャーシューって、特に魅力ですよね。
A: そうそう、それに、麺は細麺で、スープとの相性が抜群なんだ。
B: 細麺は、私も大好きです！それに、スープの味も気になりますね。
A: うん、醤油ベースなんだけど、なんか、ほんのり甘さがあって。
B: 甘味ですか、それは意外ですね！ラーメンって意外とそういう味もあるんですね。
A: そうなんだ。でも、それがまたいいんだよね。
B: なるほど、ラーメンの奥深さを感じますね。私も食べに行ってみようかな。
A: ぜひぜひ！一緒に行こうよ。
B: 本当ですか！ありがとうございます！行ってみましょう！
A: あっ、でも、その前にお店の情報を教えてよ！
"""

    def __init__(
        self,
        engine_a: str | ChatEngine | APIChatEngine,
        engine_b: str | ChatEngine | APIChatEngine,
        criteria="repeat",
        log_dir="logs",
    ):
        self.engine_a = engine_a
        self.engine_b = engine_b
        self.log_dir = log_dir

        if criteria == "repeat":
            self.criteria = criteria
        elif isinstance(criteria, str):
            self.criteria = APIChatEngine(
                criteria, system_message=self.judge_instruction
            )
            self.judge = deque([False, False], maxlen=2)
        else:
            self.criteria = criteria

    def start(
        self,
        gen_kwargs={"temperature": 0.7, "do_sample": True, "max_new_tokens": 256},
    ):
        log_file = f"chat-{datetime.datetime.now().strftime('%m%d-%H%M%S')}.log"
        log_file = os.path.join(self.log_dir, log_file)
        self.engine_a.clear()
        self.engine_b.clear()

        with open(log_file, "w") as f:
            topic = input("Topic: ")
            print("=" * 60)
            f.write(f"Topic: {topic}\n{'='*30}\n")

        response_a = self.engine_a.respond(
            f"{topic}について話そうよ", gen_kwargs=gen_kwargs, stream=False
        )
        print(f"A: {response_a}")
        with open(log_file, "a") as f:
            f.write(f"A: {response_a}\n")

        if self.criteria == "repeat":
            previous_a = ""
            previous_b = ""
        else:
            history = response_a

        continue_ = True
        num_uttrs = 0

        while continue_:
            response_b = self.engine_b.respond(
                response_a, gen_kwargs=gen_kwargs, stream=False
            )
            print(f"B: {response_b}")
            with open(log_file, "a") as f:
                f.write(f"B: {response_b}\n")

            response_a = self.engine_a.respond(
                response_b, gen_kwargs=gen_kwargs, stream=False
            )
            print(f"A: {response_a}")
            with open(log_file, "a") as f:
                f.write(f"A: {response_a}\n")

            if self.criteria == "repeat":
                if response_a == previous_a or response_a == previous_b:
                    continue_ = False
            else:
                history += f"B: {response_b}\nA: {response_a}\n"
                response_judge = self.criteria.respond(history)

                if "Termination" in response_judge:
                    self.judge.append(True)
                    with open(log_file, "a") as f:
                        f.write(f"{response_judge}\n")
                        print(response_judge)
                    continue_ = self.judge.count(True) < 2
                elif "Continue" in response_judge:
                    self.judge.append(False)
                    continue_ = self.judge.count(True) < 2

            previous_a = response_a
            previous_b = response_b

            num_uttrs += 2

        return num_uttrs

    def start_sessions(
        self,
        gen_kwargs={"temperature": 0.7, "do_sample": True, "max_new_tokens": 256},
    ):
        while True:
            num_uttrs = self.start(gen_kwargs=gen_kwargs)

            print(f"{'-' * 30}Number of utterances: {num_uttrs}{'-' * 30}")

            if input("Continue? [y/N]: ") in ["n", "N", ""]:
                break


if __name__ == "__main__":
    # a = ChatEngine(
    #     template="calm2",
    #     model="Spiral-AI/Anonymous",
    #     revision="v1.5",
    #     memory_size=40,
    #     stopper="calm2",
    # )

    # b = ChatEngine(
    #     template="calm2",
    #     model="Spiral-AI/Anonymous",
    #     revision="v1.5",
    #     memory_size=40,
    #     stopper="calm2",
    # )

    model = AutoModelForCausalLM.from_pretrained(
        "Spiral-AI/ItaCo-7b-v1", device_map="auto"
    )
    model = PeftModel.from_pretrained(model, "Spiral-AI/ItaCo-7b-v1-mt-r100-adapter")
    model = model.merge_and_unload()

    a = ChatEngine(
        template="calm2",
        model=model,
        memory_size=40,
        stopper="calm2",
    )

    b = ChatEngine(
        template="calm2",
        model=model,
        memory_size=40,
        stopper="calm2",
    )

    session = Session(a, b, criteria="gpt-3.5", log_dir="/nas/k_ishikawa/results/logs")
    session.start_sessions()
