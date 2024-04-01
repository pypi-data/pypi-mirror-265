import os
from pathlib import Path
from dataclasses import dataclass

import pytest

from piah import Piah

AI_KEY = os.getenv("OPENAI_API_KEY") is None


@dataclass
class Person1:
    name: str
    age: int


@dataclass
class Person2:
    name: str
    age: int
    adress: str
    color: str
    born_year: int


@pytest.mark.skipif(AI_KEY, reason="Key not configured in enrivonment")
def test_parser_when_receive_custom_system_context():
    to_compare = Person1("python", 33)
    parser = Piah(
        "gpt-3.5-turbo",
        "You are a principal software developer who extracts the needed values from text. "
        "Please supplement the provided JSON object with an "
        "exact value from the given text. "
        "You must always extract only the value. "
        "Your output must be a valid JSON object",
    )
    result = parser.parse("Hello I am python and I am 33 years old", Person1)
    assert result == to_compare


@pytest.mark.skipif(AI_KEY, reason="Key not configured in enrivonment")
def test_parser_when_receive_text():
    to_compare = Person1("python", 33)
    parser = Piah("gpt-3.5-turbo")
    result = parser.parse("Hello I am python and I am 33 years old", Person1)
    assert result == to_compare


@pytest.mark.skipif(AI_KEY, reason="Key not configured in enrivonment")
@pytest.mark.xfail
def test_parser_when_receive_string_pdf():
    to_compare = Person2(
        "python", 33, "221B Baker Street, London", "green", 1991
    )
    parser = Piah("gpt-3.5-turbo")
    result = parser.parse("test1.pdf", Person2)
    print(result)
    assert result == to_compare


@pytest.mark.skipif(AI_KEY, reason="Key not configured in enrivonment")
@pytest.mark.xfail
def test_parser_when_receive_path_pdf():
    to_compare = Person2(
        "python", 33, "221B Baker Street, London", "green", 1991
    )
    parser = Piah("gpt-3.5-turbo")
    result = parser.parse(Path("tests/test1.pdf"), Person2)
    print(result)
    assert result == to_compare
