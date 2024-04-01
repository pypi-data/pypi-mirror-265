from dataclasses import Field, fields, is_dataclass
from typing import Iterator, Optional, TypeVar, Type

from piah._ai import Response, Ai
from piah._utils import Pdf, _is_pdf, _extract_text


T = TypeVar("T")


class Piah:
    # TODO: write docstring
    def __init__(
        self, ai_model: str, system_content: Optional[str] = None
    ) -> None:
        self.ai = Ai(ai_model, system_content)

    @staticmethod
    def _iterate_dataclass(dataclass: Type[T]) -> Iterator[Field]:
        # TODO: write docstring
        if is_dataclass(dataclass):
            for field in fields(dataclass):
                match field.type():
                    # TODO: improve allowed types
                    case int() | str() | list():
                        yield field
                    case _:
                        raise Exception("Field type currently not allowed")

    @staticmethod
    def _dataclass_to_text(dataclass: Type[T]) -> str:
        # TODO: write docstring
        fields: list[str] = []
        for field in Piah._iterate_dataclass(dataclass):
            fields.append(field.name)
        return "{%s:}" % ":, ".join(fields)

    @staticmethod
    def _response_to_dataclass(response: Response, dataclass: Type[T]) -> T:
        # TODO: write docstring
        parsed_values = {}
        for field in Piah._iterate_dataclass(dataclass):
            value = response.get(field.name, False)
            if value:
                if not isinstance(value, field.type):
                    parsed_values[field.name] = field.type(value)
                else:
                    parsed_values[field.name] = value

        return dataclass(**parsed_values)

    @staticmethod
    def _is_valid_content_source(content_source: str | Pdf) -> str:
        # TODO: write docstring
        if isinstance(content_source, str) and not _is_pdf(content_source):
            return content_source
        return _extract_text(content_source)

    def parse(self, content_source: str | Pdf, dataclass: Type[T]) -> T:
        # TODO: write docstring
        text = Piah._is_valid_content_source(content_source)
        schema = Piah._dataclass_to_text(dataclass)
        response = self.ai._get_ai_response(schema, text)
        return Piah._response_to_dataclass(response, dataclass)
