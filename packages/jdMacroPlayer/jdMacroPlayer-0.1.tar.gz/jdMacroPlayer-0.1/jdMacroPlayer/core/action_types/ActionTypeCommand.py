from PyQt6.QtWidgets import QWidget, QLabel, QPlainTextEdit, QVBoxLayout
from typing import cast, Any, TYPE_CHECKING
from .ActionTypeBase import ActionTypeBase
from PyQt6.QtCore import QCoreApplication
from ...Functions import is_flatpak
import subprocess
import os


if TYPE_CHECKING:
    from ...Environment import Environment


class ActionTypeCommand(ActionTypeBase):
    def get_id(self) -> str:
        return "command"

    def get_name(self) -> str:
        return QCoreApplication.translate("ActionType", "Execute command")

    def get_config_widget(self, env: "Environment") -> QWidget:
        widget = QWidget()
        widget.text_edit = QPlainTextEdit()

        layout = QVBoxLayout()
        layout.addWidget(QLabel(QCoreApplication.translate("ActionType", "Command:")))
        layout.addWidget(widget.text_edit)

        widget.setLayout(layout)

        return widget

    def update_config_widget(self, widget: QWidget, config: Any) -> None:
        if isinstance(config, str):
            cast(QPlainTextEdit, widget.text_edit).setPlainText(config)

    def get_config_from_widget(self, widget: QWidget) -> Any:
        return cast(QPlainTextEdit, widget.text_edit).toPlainText()

    def get_list_text(self, config: Any) -> str:
        return QCoreApplication.translate("ActionType", "Execute command")

    def execute_action(self, env: "Environment", config: Any) -> None:
        if is_flatpak():
            subprocess.run(["flatpak-spawn", "--host", "sh", "-c", config], cwd=os.path.expanduser("~"))
        else:
            subprocess.run(["sh", "-c", config], cwd=os.path.expanduser("~"))
