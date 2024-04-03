from ..ui_compiled.AddEditMacroDialog import Ui_AddEditMacroDialog
from PyQt6.QtWidgets import QDialog, QListWidgetItem, QStyle
from .AddEditActionDialog import AddEditActionDialog
from PyQt6.QtCore import QCoreApplication
from typing import TYPE_CHECKING
from ..core.Action import Action
from PyQt6.QtGui import QIcon
import copy


if TYPE_CHECKING:
    from ..Environment import Environment
    from .MainWindow import MainWindow
    from ..core.Macro import Macro


class AddEditMacroDialog(QDialog, Ui_AddEditMacroDialog):
    def __init__(self, main_window: "MainWindow", env: "Environment", macro: "Macro") -> None:
        super().__init__(main_window)

        self.setupUi(self)

        self._env = env
        self._macro = macro

        self.tab_widget.tabBar().setDocumentMode(True)
        self.tab_widget.tabBar().setExpanding(True)
        self.tab_widget.setCurrentIndex(0)

        self._load_macro(macro)

        self._update_action_buttons_enabled()

        self.ok_button.setIcon(QIcon(env.app.style().standardIcon(QStyle.StandardPixmap.SP_DialogOkButton)))
        self.cancel_button.setIcon(QIcon(env.app.style().standardIcon(QStyle.StandardPixmap.SP_DialogCancelButton)))

        self.action_list.currentItemChanged.connect(self._update_action_buttons_enabled)
        self.add_action_button.clicked.connect(self._add_action_button_clicked)
        self.edit_action_button.clicked.connect(self._edit_action_button_clicked)
        self.remove_action_button.clicked.connect(self._remove_action_button_clicked)

        self.ok_button.clicked.connect(self._ok_button_clicked)
        self.cancel_button.clicked.connect(self.close)

        if macro.name == "":
            self.setWindowTitle(QCoreApplication.translate("AddEditMacroDialog", "Add Macro"))
        else:
            self.setWindowTitle(QCoreApplication.translate("AddEditMacroDialog", "Edit Macro"))

    def _load_macro(self, macro: "Macro") -> None:
        self.name_edit.setText(macro.name)
        self.description_edit.setText(macro.description)

        self.action_list.clear()
        for action in macro.actions:
            item = QListWidgetItem(action.get_list_text())
            item.setData(42, action)
            self.action_list.addItem(item)

    def _set_macro_data(self, macro: "Macro") -> None:
        macro.name = self.name_edit.text()
        macro.description = self.description_edit.toPlainText()

        macro.actions.clear()
        for i in range(self.action_list.count()):
            macro.actions.append(self.action_list.item(i).data(42))

    def _update_action_buttons_enabled(self) -> None:
        enabled = self.action_list.currentItem() is not None
        self.edit_action_button.setEnabled(enabled)
        self.remove_action_button.setEnabled(enabled)

    def _add_action_button_clicked(self) -> None:
        dialog = AddEditActionDialog(self, self._env, Action())
        action = dialog.open_dialog()

        if action is None:
            return

        item = QListWidgetItem(action.get_list_text())
        item.setData(42, action)
        self.action_list.addItem(item)

    def _edit_action_button_clicked(self) -> None:
        dialog = AddEditActionDialog(self, self._env, self.action_list.currentItem().data(42))
        action = dialog.open_dialog()

        if action is None:
            return

        self.action_list.currentItem().setData(42, action)
        self.action_list.currentItem().setText(action.get_list_text())

    def _remove_action_button_clicked(self) -> None:
        self.action_list.takeItem(self.action_list.currentRow())

    def _ok_button_clicked(self) -> None:
        macro = copy.deepcopy(self._macro)
        self._set_macro_data(macro)
        self._env.macro_manager.update_macro(macro)
        self.close()

    def open_dialog(self) -> None:
        self.exec()
