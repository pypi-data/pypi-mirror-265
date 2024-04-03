from ..ui_compiled.WelcomeDialog import Ui_WelcomeDialog
from PyQt6.QtWidgets import QDialog, QStyle
from PyQt6.QtGui import QCloseEvent, QIcon
from typing import TYPE_CHECKING
import os


if TYPE_CHECKING:
    from ..Environment import Environment
    from .MainWindow import MainWindow


class WelcomeDialog(QDialog, Ui_WelcomeDialog):
    def __init__(self, main_window: "MainWindow", env: "Environment") -> None:
        super().__init__(main_window)

        self.setupUi(self)

        self._env = env

        with open(os.path.join(env.program_dir, "data", "welcome.html"), "r", encoding="utf-8") as f:
            self.text_browser.setHtml(f.read())

        self.startup_check_box.setChecked(env.settings.get("welcomeDialogStartup"))

        self.ok_button.setIcon(QIcon(env.app.style().standardIcon(QStyle.StandardPixmap.SP_DialogOkButton)))

        self.ok_button.clicked.connect(self.close)

    def closeEvent(self, event: QCloseEvent | None) -> None:
        self._env.settings.set("welcomeDialogStartup", self.startup_check_box.isChecked())
        self._env.settings.save()

        return super().closeEvent(event)
