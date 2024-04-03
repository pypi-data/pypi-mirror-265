from ..core.action_types import get_all_action_types, get_action_type_by_id
from ..ui_compiled.AddEditActionDialog import Ui_AddEditActionDialog
from ..Functions import select_combo_box_data
from PyQt6.QtWidgets import QDialog, QStyle
from typing import Optional, TYPE_CHECKING
from PyQt6.QtCore import QCoreApplication
from PyQt6.QtGui import QIcon
import copy


if TYPE_CHECKING:
    from .AddEditMacroDialog import AddEditMacroDialog
    from ..Environment import Environment
    from ..core.Action import Action


class AddEditActionDialog(QDialog, Ui_AddEditActionDialog):
    def __init__(self, parent: "AddEditMacroDialog", env: "Environment", action: "Action") -> None:
        super().__init__(parent)

        self.setupUi(self)

        self._env = env
        self._ok = False
        self._action = action

        for action_type in get_all_action_types():
            self.type_box.addItem(action_type.get_name(), action_type.get_id())

        self._load_action(action)

        self.ok_button.setIcon(QIcon(env.app.style().standardIcon(QStyle.StandardPixmap.SP_DialogOkButton)))
        self.cancel_button.setIcon(QIcon(env.app.style().standardIcon(QStyle.StandardPixmap.SP_DialogCancelButton)))

        self.type_box.currentIndexChanged.connect(self._update_config_widget)

        self.ok_button.clicked.connect(self._ok_button_clicked)
        self.cancel_button.clicked.connect(self.close)

        if action.type == "":
            self.setWindowTitle(QCoreApplication.translate("AddEditActionDialog", "Add Action"))
        else:
            self.setWindowTitle(QCoreApplication.translate("AddEditActionDialog", "Edit Action"))

    def _load_action(self, action: "Action") -> None:
        select_combo_box_data(self.type_box, action.type)

        self._update_config_widget()
        action_type = get_action_type_by_id(self.type_box.currentData())

        if action_type is None:
            return

        action_type.update_config_widget(self._config_widget, action.config)

    def _set_action_data(self, action: "Action") -> None:
        action.type = self.type_box.currentData()

        action_type = get_action_type_by_id(self.type_box.currentData())

        if action_type is None:
            return

        action.config = action_type.get_config_from_widget(self._config_widget)

    def _update_config_widget(self) -> None:
        action_type = get_action_type_by_id(self.type_box.currentData())

        if action_type is None:
            return

        item = self.config_layout.takeAt(0)
        if item is not None:
            item.widget().setParent(None)

        self._config_widget = action_type.get_config_widget(self._env)
        self.config_layout.addWidget(self._config_widget)

    def _ok_button_clicked(self) -> None:
        self._ok = True
        self.close()

    def open_dialog(self) -> Optional["Action"]:
        self.exec()

        if not self._ok:
            return None

        action = copy.deepcopy(self._action)
        self._set_action_data(action)

        return action
