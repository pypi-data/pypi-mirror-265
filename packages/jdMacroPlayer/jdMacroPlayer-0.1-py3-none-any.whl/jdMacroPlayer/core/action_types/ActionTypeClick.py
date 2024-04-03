from PyQt6.QtWidgets import QWidget, QComboBox, QLabel, QHBoxLayout, QVBoxLayout
from ...Functions import select_combo_box_data
from .ActionTypeBase import ActionTypeBase
from PyQt6.QtCore import QCoreApplication
from typing import Any, TYPE_CHECKING
import subprocess


if TYPE_CHECKING:
    from ...Environment import Environment


class ActionTypeClick(ActionTypeBase):
    def get_id(self) -> str:
        return "click"

    def get_name(self) -> str:
        return QCoreApplication.translate("ActionType", "Click mouse")

    def get_config_widget(self, env: "Environment") -> QWidget:
        widget = QWidget()

        widget.button_box = QComboBox()
        widget.button_box.addItem(QCoreApplication.translate("ActionType", "Left", "The mouse button"), "0xC0")
        widget.button_box.addItem(QCoreApplication.translate("ActionType", "Right", "The mouse button"), "0xC1")
        widget.button_box.addItem(QCoreApplication.translate("ActionType", "Middle", "The mouse button"), "0xC2")

        button_layout = QHBoxLayout()
        button_layout.addWidget(QLabel(QCoreApplication.translate("ActionType", "Button", "The mouse button")))
        button_layout.addWidget(widget.button_box)

        main_layout = QVBoxLayout()
        main_layout.addLayout(button_layout)
        main_layout.addStretch(1)
        main_layout.setContentsMargins(0, 0, 0, 0)

        widget.setLayout(main_layout)

        return widget

    def update_config_widget(self, widget: QWidget, config: Any) -> None:
        select_combo_box_data(widget.button_box, config)

    def get_config_from_widget(self, widget: QWidget) -> Any:
        return widget.button_box.currentData()

    def get_list_text(self, config: Any) -> str:
        text = QCoreApplication.translate("ActionType", "Click mouse") + " "

        match config:
            case "0xC0":
                text += QCoreApplication.translate("ActionType", "Left", "The mouse button")
            case "0xC1":
                text += QCoreApplication.translate("ActionType", "Right", "The mouse button")
            case "0xC2":
                text += QCoreApplication.translate("ActionType", "Middle", "The mouse button")

        return text

    def execute_action(self, env: "Environment", config: Any) -> None:
        import time
        time.sleep(1)
        subprocess.run(["ydotool", "click", config])
