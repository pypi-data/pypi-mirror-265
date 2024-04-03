from PyQt6.QtWidgets import QWidget, QListWidget, QPushButton, QHBoxLayout, QVBoxLayout
from .SelectKeyDialog import SelectKeyDialog
from PyQt6.QtCore import QCoreApplication
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from ..Environment import Environment


class KeylistWidget(QWidget):
    def __init__(self, env: "Environment") -> None:
        super().__init__()

        self._env = env
        self._list_widget = QListWidget()
        add_button = QPushButton(QCoreApplication.translate("KeylistWidget", "Add"))
        self._remove_button = QPushButton(QCoreApplication.translate("KeylistWidget", "Remove"))

        self._update_remove_button_enabled()

        self._list_widget.currentItemChanged.connect(self._update_remove_button_enabled)
        add_button.clicked.connect(self._add_button_clicked)
        self._remove_button.clicked.connect(self._remove_button_clicked)

        button_layout = QHBoxLayout()
        button_layout.addWidget(add_button)
        button_layout.addWidget(self._remove_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self._list_widget)
        main_layout.addLayout(button_layout)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(main_layout)

    def _update_remove_button_enabled(self) -> None:
        self._remove_button.setEnabled(self._list_widget.currentItem() is not None)

    def _add_button_clicked(self) -> None:
        dialog = SelectKeyDialog(self, self._env)
        keyname = dialog.get_keyname()

        if keyname is None:
            return

        self._list_widget.addItem(keyname)

    def _remove_button_clicked(self) -> None:
        self._list_widget.takeItem(self._list_widget.currentRow())

    def get_keynames(self) -> list[str]:
        name_list: list[str] = []
        for i in range(self._list_widget.count()):
            name_list.append(self._list_widget.item(i).text())
        return name_list

    def set_keynames(self, name_list: list[str]) -> None:
        self._list_widget.clear()
        for name in name_list:
            self._list_widget.addItem(name)
