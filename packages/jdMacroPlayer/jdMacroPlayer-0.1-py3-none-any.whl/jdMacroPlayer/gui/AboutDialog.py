from ..ui_compiled.AboutDialog import Ui_AboutDialog
from PyQt6.QtWidgets import QDialog, QStyle
from typing import TYPE_CHECKING
from PyQt6.QtGui import QIcon
import os


if TYPE_CHECKING:
    from ..Environment import Environment
    from .MainWindow import MainWindow


class AboutDialog(QDialog, Ui_AboutDialog):
    def __init__(self, main_window: "MainWindow", env: "Environment") -> None:
        super().__init__(main_window)

        self.setupUi(self)

        self.icon_label.setPixmap(env.icon.pixmap(64, 64))
        self.version_label.setText(self.version_label.text().replace("{{version}}", env.version))

        self.ok_button.setIcon(QIcon(env.app.style().standardIcon(QStyle.StandardPixmap.SP_DialogOkButton)))

        self.ok_button.clicked.connect(self.close)
