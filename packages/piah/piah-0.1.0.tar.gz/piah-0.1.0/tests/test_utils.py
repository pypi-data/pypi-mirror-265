from pathlib import Path

import pytest

from piah._utils import _extract_text, _is_pdf

@pytest.mark.parametrize("input,expected", [
    ("tests/test2.pdf", "An\nexample\nPDF\njust\na\nsimple\npdf"),
    (Path("tests/test2.pdf"), "An\nexample\nPDF\njust\na\nsimple\npdf")
])
def test_it_correctly_extract_text_from_pdf(input, expected):
    assert _extract_text(input) == expected

@pytest.mark.parametrize("input,expected", [
    ("just string", False),
    ("string", False),
    ("A long string that is not a pdf."
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
        "Vestibulum faucibus imperdiet purus eget rutrum"
        "Suspendisse ac augue sed mi dignissim dignissim",
     False),
    ("tests/test1.pdf", True),
    (Path("tests/test2.pdf"), True)
])
def test_it_is_pdf(input, expected):
    assert _is_pdf(input) == expected

