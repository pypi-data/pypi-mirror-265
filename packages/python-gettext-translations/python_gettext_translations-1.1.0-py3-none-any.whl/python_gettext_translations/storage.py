import os
import polib


class Storage(object):
    """
    Top level key is the language code, and the value is the map where keys represent the original strings
    and values represent the translations
    """
    storage: dict[str, dict[str, str]] = {}

    @staticmethod
    def load(path):
        for (dirpath, dirnames, filenames) in os.walk(path):
            for language_code in dirnames:
                if not os.path.isdir(path + "/" + language_code):
                    continue

                translation_file_name = path + "/" + language_code + "/messages.po"
                if not os.path.isfile(translation_file_name):
                    continue

                po = polib.pofile(translation_file_name)
                Storage.storage[language_code] = {}
                for entry in po:
                    Storage.storage[language_code][entry.msgid] = entry.msgstr


    @staticmethod
    def get_translation_string(language_code: str, original_string: str) -> str:
        if not language_code in Storage.storage:
            return original_string

        if not original_string in Storage.storage.get(language_code):
            return original_string

        translation_candidate = Storage.storage[language_code][original_string]
        if translation_candidate.strip() == "":
            return original_string

        return translation_candidate