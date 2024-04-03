import os

from python_gettext_translations.storage import Storage

dir_path = os.path.dirname(os.path.realpath(__file__))

def test_happy_pass():
    Storage.load(dir_path + "/i18n")
    assert len(Storage.storage.keys()) == 2
    assert "de_DE" in Storage.storage.keys()
    assert "fr_FR" in Storage.storage.keys()