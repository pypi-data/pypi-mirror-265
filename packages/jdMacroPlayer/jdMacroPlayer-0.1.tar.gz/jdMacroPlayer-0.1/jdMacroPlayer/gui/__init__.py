from PyQt6.QtCore import QCoreApplication, QTranslator, QLocale, QLibraryInfo
from PyQt6.QtDBus import QDBusConnection, QDBusMessage
from PyQt6.QtWidgets import QApplication, QMessageBox
from .MainWindow import MainWindow
from PyQt6.QtGui import QIcon
import argparse
import shutil
import sys
import os


def _startup_check() -> None:
    for program in ("ydotool", "ydotoold"):
        if shutil.which(program) is None:
            QMessageBox.critical(
                None,
                QCoreApplication.translate("jdMacroPlayer", "{{program}} not found").replace("{{program}}", program),
                QCoreApplication.translate("jdMacroPlayer", "{{program}} was not found. Make sure it's installed and in PATH.", "Don't translate PATH").replace("{{program}}", program),
            )
            sys.exit(0)

    if os.getenv("KDE_SESSION_VERSION") == "5":
        QMessageBox.critical(
            None,
            QCoreApplication.translate("jdMacroPlayer", "KDE Plasma 5 not supported"),
            QCoreApplication.translate("jdMacroPlayer", "KDE Plasma 5 does not implement the Global Shortcuts Portal correctly, so it is not supported by jdMacroPlayer.", "Don't translate Global Shortcuts"),
        )
        sys.exit(0)

    msg = QDBusMessage.createMethodCall("org.freedesktop.portal.Desktop", "/org/freedesktop/portal/desktop", "org.freedesktop.DBus.Properties", "Get")
    msg.setArguments(("org.freedesktop.portal.GlobalShortcuts", "version"))
    resp = QDBusConnection.sessionBus().call(msg)

    if resp.errorMessage() != "":
        QMessageBox.critical(
            None,
            QCoreApplication.translate("jdMacroPlayer", "Global Shortcuts not available", "Don't translate Global Shortcuts"),
            QCoreApplication.translate("jdMacroPlayer", "Your desktop does not support the Global Shortcuts Portal. This portal is needed for jdMacroPlayer to work.", "Don't translate Global Shortcuts")
        )
        sys.exit(0)


def main() -> None:
    from ..Environment import Environment

    app = QApplication(sys.argv)

    env = Environment()

    env.app = app
    env.icon = QIcon(os.path.join(env.program_dir, "Icon.png"))

    app.setWindowIcon(env.icon)
    app.setOrganizationName("JakobDev")
    app.setApplicationVersion(env.version)
    app.setApplicationName("jdMacroPlayer")
    app.setDesktopFileName("page.codeberg.JakobDev.jdMacroPlayer")

    if env.settings.get("language") == "default":
        locale = QLocale()
    else:
        locale = QLocale(env.settings.get("language"))

    qt_translator = QTranslator()
    if qt_translator.load(locale, "qt", "_", QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath)):
        app.installTranslator(qt_translator)

    app_translator = QTranslator()
    if app_translator.load(locale, "jdMacroPlayer", "_", os.path.join(env.program_dir, "translations")):
        app.installTranslator(app_translator)

    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-startup-check", action="store_true", help=QCoreApplication.translate("jdMacroPlayer", "Skips the startup check"))
    args = parser.parse_known_args()[0]

    if not args.skip_startup_check:
        _startup_check()

    main_window = MainWindow(env)
    main_window.show()

    if env.settings.get("welcomeDialogStartup"):
        main_window.open_welcome_dialog()

    sys.exit(app.exec())
