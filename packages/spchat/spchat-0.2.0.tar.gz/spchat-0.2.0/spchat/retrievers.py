import argparse
import json
import os
from pathlib import Path

import chromadb
import tqdm
from datasets import load_dataset
from loguru import logger
from spllm.utils import get_single_openai_api_key


class FactRetriever:
    VIOLATED_NAMING_CONVENTION = "violated_chromadb_naming_convention"

    def __init__(
        self,
        db_dir: str | Path,
        embd_style: str = "openai",
        embd_kwargs: dict = {},
    ):
        db_dir = str(db_dir)
        self.client = chromadb.PersistentClient(db_dir)

        with open(os.path.join(db_dir, "embedding.json"), "w") as f:
            f.write(json.dumps({"embd_style": embd_style, "embd_kwargs": embd_kwargs}))

        match embd_style:
            case "openai":
                from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

                self.embeddings = OpenAIEmbeddingFunction(
                    api_key=get_single_openai_api_key(), **embd_kwargs
                )

            case "hf":
                from chromadb.utils.embedding_functions import (
                    HuggingFaceEmbeddingFunction,
                )

                self.embeddings = HuggingFaceEmbeddingFunction(**embd_kwargs)

    def set_user(self, user):
        if user.endswith("_") or user.endswith("-"):
            user += self.VIOLATED_NAMING_CONVENTION
        if user.startswith("_") or user.startswith("-"):
            user = self.VIOLATED_NAMING_CONVENTION + user
        self.db = self.client.get_or_create_collection(
            user, embedding_function=self.embeddings
        )

    def retrieve(self, query: str | list, top_k: int) -> str:
        try:
            facts = self.db.query(query_texts=query, n_results=top_k)
        except AttributeError:
            logger.error(
                "You need to set the user first. Please use `set_user` method to set the user."
            )
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            logger.error(f"Query: {query}")
            logger.error(f"Top k: {top_k}")
            raise e

        f = "".join([x for x in facts["documents"][0]])
        if f.endswith("\n"):
            f = f[:-1]
        return f

    def add(self, src_file):
        if os.path.exists(src_file):
            if len(self.db.get()["documents"]) > 0:
                logger.warning(
                    f"Vectorstore for {user} already exists. If you want to update it, please use `update` method. Skipping."
                )
                return
            with open(src_file) as f:
                docs = f.readlines()
            self.db.add(
                documents=docs,
                metadatas=[{"user": user} for _ in range(len(docs))],
                ids=[f"{user}_{i:08d}" for i in range(len(docs))],
            )
        else:
            logger.warning(f"File {src_file} has not been generated yet. Skipping.")
            return

    def update(self, src_file):
        if os.path.exists(src_file):
            with open(src_file) as f:
                docs = f.readlines()
            self.db.update(
                documents=docs,
                metadatas=[{"user": user} for _ in range(len(docs))],
                ids=[f"{user}_{i:08d}" for i in range(len(docs))],
            )
        else:
            logger.warning(f"File {src_file} has not been generated yet. Skipping.")
            return

    def add_users(self, users, src_dir):
        for user in tqdm.tqdm(users):
            self.set_user(user)
            src_file = os.path.join(src_dir, user, "all_facts.txt")
            self.add(src_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--users", type=str, nargs="+")
    parser.add_argument(
        "-src", "--src_dir", type=str, default="/home/ubuntu/workspace/data"
    )
    args = parser.parse_args()

    if args.users:
        users = args.users
    else:
        dataset = load_dataset("Spiral-AI/CharacterChat", split="x")
        df = dataset.to_pandas()
        users = df.user_id.unique()

    retriever = FactRetriever(
        db_dir=os.path.join(args.src_dir, "vectorstore"),
        embd_style="openai",
    )

    retriever.add_users(users, args.src_dir)

    logger.success("Retrieved all facts!")
