from PyQt6.QtWidgets import QWidget, QDialog, QListWidgetItem, QStyle
from ..ui_compiled.SelectKeyDialog import Ui_SelectKeyDialog
from typing import TYPE_CHECKING
from PyQt6.QtGui import QIcon


if TYPE_CHECKING:
    from ..Environment import Environment


class SelectKeyDialog(QDialog, Ui_SelectKeyDialog):
    def __init__(self, parent: QWidget | None, env: "Environment") -> None:
        super().__init__(parent)

        self.setupUi(self)

        self._ok = False

        for name, code in env.keycodes.items():
            item = QListWidgetItem(name)
            item.setData(42, code)
            self.key_list.addItem(item)

        self._update_ok_button_enabled()

        self.ok_button.setIcon(QIcon(env.app.style().standardIcon(QStyle.StandardPixmap.SP_DialogOkButton)))
        self.cancel_button.setIcon(QIcon(env.app.style().standardIcon(QStyle.StandardPixmap.SP_DialogCancelButton)))

        self.search_edit.textChanged.connect(self._update_items_visible)
        self.key_list.currentItemChanged.connect(self._update_ok_button_enabled)
        self.ok_button.clicked.connect(self._ok_button_clicked)
        self.cancel_button.clicked.connect(self.close)

    def _update_items_visible(self) -> None:
        search_text = self.search_edit.text().lower()
        for i in range(self.key_list.count()):
            item = self.key_list.item(i)
            if search_text in item.text().lower():
                item.setHidden(False)
            else:
                item.setHidden(True)

    def _update_ok_button_enabled(self) -> None:
        self.ok_button.setEnabled(self.key_list.currentItem() is not None)

    def _ok_button_clicked(self) -> None:
        self._ok = True
        self.close()

    def get_keyname(self) -> str | None:
        self.exec()

        if self._ok:
            return self.key_list.currentItem().text()
        else:
            return None
