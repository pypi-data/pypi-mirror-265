from PyQt6.QtWidgets import QWidget, QPlainTextEdit, QLabel, QVBoxLayout
from typing import cast, Any, TYPE_CHECKING
from .ActionTypeBase import ActionTypeBase
from PyQt6.QtCore import QCoreApplication
import subprocess


if TYPE_CHECKING:
    from ...Environment import Environment


class ActionTypeType(ActionTypeBase):
    def get_id(self) -> str:
        return "type"

    def get_name(self) -> str:
        return QCoreApplication.translate("ActionType", "Type text")

    def get_config_widget(self, env: "Environment") -> QWidget:
        widget = QWidget()
        widget.text_edit = QPlainTextEdit()

        layout = QVBoxLayout()
        layout.addWidget(QLabel(QCoreApplication.translate("ActionType", "Text:")))
        layout.addWidget(widget.text_edit)

        widget.setLayout(layout)

        return widget

    def update_config_widget(self, widget: QWidget, config: Any) -> None:
        if isinstance(config, str):
            cast(QPlainTextEdit, widget.text_edit).setPlainText(config)

    def get_config_from_widget(self, widget: QWidget) -> Any:
        return cast(QPlainTextEdit, widget.text_edit).toPlainText()

    def get_list_text(self, config: Any) -> str:
        return QCoreApplication.translate("ActionType", "Type text") + " " + str(config)

    def execute_action(self, env: "Environment", config: Any) -> None:
        subprocess.run(["ydotool", "type", "-e", config])
