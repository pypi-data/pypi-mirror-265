from PyQt6.QtWidgets import QWidget, QSpinBox, QCheckBox, QLabel, QFormLayout, QVBoxLayout
from ...Constants import SPIN_BOX_MAX, SPIN_BOX_MIN
from .ActionTypeBase import ActionTypeBase
from PyQt6.QtCore import QCoreApplication
from typing import Any, TYPE_CHECKING
import subprocess


if TYPE_CHECKING:
    from ...Environment import Environment


class ActionTypeMousemove(ActionTypeBase):
    def get_id(self) -> str:
        return "mousemove"

    def get_name(self) -> str:
        return QCoreApplication.translate("ActionType", "Move mouse")

    def get_config_widget(self, env: "Environment") -> QWidget:
        widget = QWidget()

        widget.x_spin_box = QSpinBox()
        widget.y_spin_box = QSpinBox()
        widget.absolute_check_box = QCheckBox(QCoreApplication.translate("ActionType", "Absolute"))

        widget.x_spin_box.setMaximum(SPIN_BOX_MAX)
        widget.x_spin_box.setMinimum(SPIN_BOX_MIN)

        widget.y_spin_box.setMaximum(SPIN_BOX_MAX)
        widget.y_spin_box.setMinimum(SPIN_BOX_MIN)

        form_layout = QFormLayout()
        form_layout.addRow(QLabel("X:"), widget.x_spin_box)
        form_layout.addRow(QLabel("Y:"), widget.y_spin_box)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addWidget(widget.absolute_check_box)
        main_layout.addStretch(1)
        main_layout.setContentsMargins(0, 0, 0, 0)

        widget.setLayout(main_layout)

        return widget

    def update_config_widget(self, widget: QWidget, config: Any) -> None:
        widget.x_spin_box.setValue(config["x"])
        widget.y_spin_box.setValue(config["y"])
        widget.absolute_check_box.setChecked(config["absolute"])

    def get_config_from_widget(self, widget: QWidget) -> Any:
        return {
            "x": widget.x_spin_box.value(),
            "y": widget.y_spin_box.value(),
            "absolute": widget.absolute_check_box.isChecked(),
        }

    def get_list_text(self, config: Any) -> str:
        text = QCoreApplication.translate("ActionType", "Move mouse") + f" X:{config['x']} Y:{config['y']}"

        if config["absolute"]:
            text += " " + QCoreApplication.translate("ActionType", "Absolute")

        return text

    def execute_action(self, env: "Environment", config: Any) -> None:
        command = ["ydotool", "mousemove", "-x", str(config["x"]), "-y", str(config["y"])]

        if config["absolute"]:
            command.append("-a")

        subprocess.run(command)
