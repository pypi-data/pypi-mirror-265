import os

from python_gettext_translations.translations import init_translations, translate

dir_path = os.path.dirname(os.path.realpath(__file__))

def test_happy_pass():
    init_translations(dir_path + "/i18n")
    assert translate("de_DE", "Hello, %user%", {"user": "Alexey"}) == "Hallo, Alexey"

def test_untranslated_string():
    init_translations(dir_path + "/i18n")
    assert translate("de_DE", "String is not translated in DE") == "String is not translated in DE"

def test_fr_language():
    init_translations(dir_path + "/i18n")
    assert translate("fr_FR", "Slug is already in use") == "Slug est déjà utilisé"

def test_nonexisting_key():
    init_translations(dir_path + "/i18n")
    assert translate("fr_FR", "String is not translated in DE") == "String is not translated in DE"