from pathlib import Path
from typing import Union, Any, IO

from pypdf import PdfReader

StreamType = IO[Any]
StrByteType = Union[str, StreamType]
Pdf = StrByteType | Path


def _extract_text(stream: StrByteType | Path) -> str:
    # TODO: write docstring
    reader = PdfReader(stream)
    page = reader.pages[0]
    return page.extract_text()


def _is_pdf(value: Pdf) -> bool:
    # TODO: write docstring
    try:
        _extract_text(value)
        return True
    except FileNotFoundError:
        return False
    except OSError:
        return False
