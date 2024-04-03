from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QVBoxLayout
from ...shared.KeylistWidget import KeylistWidget
from typing import cast, Any, TYPE_CHECKING
from .ActionTypeBase import ActionTypeBase
from PyQt6.QtCore import QCoreApplication
import subprocess


if TYPE_CHECKING:
    from ...Environment import Environment


class ActionTypeKeypress(ActionTypeBase):
    def get_id(self) -> str:
        return "keypress"

    def get_name(self) -> str:
        return QCoreApplication.translate("ActionType", "Press key")

    def get_config_widget(self, env: "Environment") -> QWidget:
        widget = QWidget()

        widget.keylist = KeylistWidget(env)

        layout = QVBoxLayout()
        layout.addWidget(QLabel(QCoreApplication.translate("ActionType", "These buttons are pressed simultaneously")))
        layout.addWidget(widget.keylist)
        layout.setContentsMargins(0, 0, 0, 0)

        widget.setLayout(layout)

        return widget

    def update_config_widget(self, widget: QWidget, config: Any) -> None:
        cast(KeylistWidget, widget.keylist).set_keynames(config)

    def get_config_from_widget(self, widget: QWidget) -> Any:
        return cast(KeylistWidget, widget.keylist).get_keynames()

    def get_list_text(self, config: Any) -> str:
        return QCoreApplication.translate("ActionType", "Press key") + " " + " ".join(config)

    def execute_action(self, env: "Environment", config: Any) -> None:
        import time
        time.sleep(1)

        command = ["ydotool", "key"]

        for key in config:
            command.append(f"{env.keycodes.get(key, 0)}:1")

        for key in config:
            command.append(f"{env.keycodes.get(key, 0)}:0")

        subprocess.run(command)
