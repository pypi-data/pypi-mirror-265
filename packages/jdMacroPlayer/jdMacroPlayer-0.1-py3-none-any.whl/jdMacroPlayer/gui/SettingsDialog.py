from ..ui_compiled.SettingsDialog import Ui_SettingsDialog
from ..core.Languages import get_language_names
from PyQt6.QtCore import Qt, QCoreApplication
from ..Functions import select_combo_box_data
from PyQt6.QtWidgets import QDialog, QStyle
from typing import TYPE_CHECKING
from PyQt6.QtGui import QIcon
import copy
import os


if TYPE_CHECKING:
    from ..Environment import Environment
    from ..core.Settings import Settings
    from .MainWindow import MainWindow


class SettingsDialog(QDialog, Ui_SettingsDialog):
    def __init__(self, main_window: "MainWindow", env: "Environment") -> None:
        super().__init__(main_window)

        self.setupUi(self)

        self._env = env

        language_names = get_language_names()
        self.language_box.addItem(language_names["en"], "en")
        for i in os.listdir(os.path.join(env.program_dir, "translations")):
            if not i.endswith(".qm"):
                continue

            lang = i.removeprefix("jdMacroPlayer_").removesuffix(".qm")
            self.language_box.addItem(language_names.get(lang, lang), lang)

        self.language_box.model().sort(0, Qt.SortOrder.AscendingOrder)
        self.language_box.insertItem(0, QCoreApplication.translate("SettingsDialog", "System language"), "default")

        self.reset_button.setIcon(QIcon(env.app.style().standardIcon(QStyle.StandardPixmap.SP_DialogResetButton)))
        self.ok_button.setIcon(QIcon(env.app.style().standardIcon(QStyle.StandardPixmap.SP_DialogOkButton)))
        self.cancel_button.setIcon(QIcon(env.app.style().standardIcon(QStyle.StandardPixmap.SP_DialogCancelButton)))

        self._update_widgets(env.settings)

        self.reset_button.clicked.connect(self._reset_button_clicked)
        self.ok_button.clicked.connect(self._ok_button_clicked)
        self.cancel_button.clicked.connect(self.close)

    def _update_widgets(self, settings: "Settings") -> None:
        select_combo_box_data(self.language_box, settings.get("language"))
        self.welcome_dialog_check_box.setChecked(settings.get("welcomeDialogStartup"))

    def _reset_button_clicked(self) -> None:
        settings = copy.deepcopy(self._env.settings)
        settings.reset()
        self._update_widgets(settings)

    def _ok_button_clicked(self) -> None:
        self._env.settings.set("language", self.language_box.currentData())
        self._env.settings.set("welcomeDialogStartup", self.welcome_dialog_check_box.isChecked())

        self._env.settings.save()

        self.close()
