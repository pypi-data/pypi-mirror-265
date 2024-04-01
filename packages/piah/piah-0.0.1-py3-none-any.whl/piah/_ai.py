import json
from typing import Optional

from litellm import completion

Response = dict[str, str | int]


class Ai:
    # TODO: write docstring
    system = {
        "role": "system",
        "content": "You are a senior developer who extracts the needed values from text. "
        "Please supplement the provided JSON object with an "
        "exact value from the given text and only from it. "
        "You must always extract only the value. "
        "Your output must be a valid JSON object",
    }

    def __init__(
        self, ai_model: str, system_content: Optional[str] = None
    ) -> None:
        self.ai_model = ai_model
        if system_content:
            self.system["content"] = system_content

    def _setup_message(self, schema: str, text: str):
        # TODO: write docstring
        message = [
            self.system,
            {
                "role": "user",
                "content": f"JSON object should look like this and it should supplement the empty "
                f"JSON: {schema}",
            },
            {
                "role": "user",
                "content": f"Here is the text you need to parse: {text}",
            },
        ]
        return message

    def _get_ai_response(self, schema: str, text: str) -> Response:
        # TODO: write docstring
        response = completion(
            model=self.ai_model,  # like gpt-3.5-turbo
            messages=self._setup_message(schema, text),
        )
        content = response.model_dump()["choices"][0]["message"]["content"]
        return json.loads(content)
