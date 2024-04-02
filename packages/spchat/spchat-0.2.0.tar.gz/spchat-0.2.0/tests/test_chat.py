from datetime import datetime

import pytest

from spchat.chat import Utterance


def test_utterance_post_init():
    utterance = Utterance(content="Hello", speaker="user")
    assert isinstance(utterance.id, str)
    assert len(utterance.id) > 0  # UUIDが生成されていることを確認
    assert utterance.timestamp == datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def test_utterance_add():
    utterance1 = Utterance(content="Hello", speaker="user")
    utterance2 = Utterance(content=" World", speaker="user")
    utterance1.add(utterance2)
    assert utterance1.content == "Hello World"


def test_utterance_add_with_different_speakers():
    utterance1 = Utterance(content="Hello", speaker="user")
    utterance2 = Utterance(content=" World", speaker="assistant")
    with pytest.raises(AssertionError):
        utterance1.add(utterance2)


def test_utterance_remove_line_breaks():
    utterance = Utterance(content="Hello\nWorld", speaker="user")
    utterance.remove_line_breaks()
    assert utterance.content == "Hello World"


def test_utterance_from_dict():
    message = {"role": "user", "content": "Hello World"}
    utterance = Utterance.from_dict(message)
    assert utterance.speaker == "user"
    assert utterance.content == "Hello World"


def test_utterance_to_dict():
    utterance = Utterance(content="Hello", speaker="user")
    utterance_dict = utterance.to_dict()
    assert utterance_dict["content"] == "Hello"
    assert utterance_dict["speaker"] == "user"
