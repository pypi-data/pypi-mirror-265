<h1 align="center">jdMacroPlayer</h1>

<h3 align="center">Wayland compatible macro player for Linux</h3>

<p align="center">
    <img alt="jdMacroPlayer" src="screenshots/MainWindow.png"/>
</p>

jdMacroPlayer allows you to create and execute Macros under Wayland and X11. You can simulate Keybaord and Mouse input or execute a Command by pressing a Shortcut.

## Translate
You can help translating jdMacroPlayer on [Codeberg Translate](https://translate.codeberg.org/projects/jdMacroPlayer)

## Develop
jdMacroPlayer is written in Python and uses PyQt6 as GUI toolkit. You should have some experience in both.
You can run `jdMacroPlayer.py`to start jdMacroPlayer from source and test your local changes.
It ships with a few scripts in the tools directory that you need to develop.

#### CompileUI.py
This is the most important script. It will take all `.ui` files in `jdMacroPlayer/ui` and compiles it to a Python class
and stores it in `jdMacroPlayer/ui_compiled`. Without running this script first, you can't start jdMacroPlayer.
You need to rerun it every time you changed or added a `.ui` file.

#### BuildTranslations.py
This script takes all `.ts` files and compiles it to `.qm` files.
The `.ts` files are containing the translation source and are being used during the translation process.
The `.qm` contains the compiled translation and are being used by the Program.
You need to compile a `.ts` file to a `.qm` file to see the translations in the Program.

#### UpdateTranslations.py
This regenerates the `.ts` files. You need to run it, when you changed something in the source code.
The `.ts` files are contains the line in the source, where the string to translate appears,
so make sure you run it even when you don't changed a translatable string, so the location is correct.

####  UpdateUnixDataTranslations.py
This regenerates the translation files in `deploy/translations`. these files contains the translations for the Desktop Entry and the AppStream File.
It uses gettext, as it is hard to translate this using Qt.
These files just exists to integrate the translation with Weblate, because Weblate can't translate the Desktop Entry and the AppStream file.
Make sure you run this when you edited one of these files.
You need to have gettext installed to use it.

#### UpdateKeycodes.py
This generates `jdMacroPlayer/data/keycodes.json`
