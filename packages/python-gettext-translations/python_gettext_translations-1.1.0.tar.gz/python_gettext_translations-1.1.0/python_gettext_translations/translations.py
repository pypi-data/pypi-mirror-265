from typing import Optional
from python_gettext_translations.storage import Storage

def init_translations(translations_dir: str):
    Storage.load(translations_dir)

def translate(language: str, original: str, placeholders: Optional[dict[str, str]] = None) -> str:
    translation = Storage.get_translation_string(language, original)
    if placeholders:
        for placeholder in placeholders:
            translation = translation.replace("%" + placeholder + "%", placeholders[placeholder])

    return translation