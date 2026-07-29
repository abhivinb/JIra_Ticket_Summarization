import json
from pathlib import Path


def ensure_directory(path):

    Path(path).mkdir(
        parents=True,
        exist_ok=True
    )


def save_json(data, path):

    with open(path, "w", encoding="utf-8") as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )


def load_json(path):

    with open(path, encoding="utf-8") as file:

        return json.load(file)

def clean_json(text: str) -> str:

    text = text.strip()

    if text.startswith("```json"):
        text = text.replace("```json", "", 1)

    if text.startswith("```"):
        text = text.replace("```", "", 1)

    if text.endswith("```"):
        text = text[:-3]

    return text.strip()