Usage
=====
1. Place your translation files in the directory tree structured as below:
.. code-block:: console

    i18n/en_GB/messages.po
    i18n/fr_FR/messages.po

2. Load the translation strings:
.. code-block:: python

    from translations import init_translations
    dir_path = os.path.dirname(os.path.realpath(__file__))
    init_translations(dir_path + "/i18n")

3. Get translation string:
.. code-block:: python

    from translations import translate
    translate("de_DE", "Hello, %user%", {"user": "Alexey"}) # Prints "Hello, Alexey"

New version release
--------------------

To release new version:
1. Update sphinx_integral_theme/__init__.py with new __version__ and __version_info__
2. Run the following command:
.. code-block:: console

   (.venv) $ flit publish