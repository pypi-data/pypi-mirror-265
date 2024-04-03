from typing import Any, TYPE_CHECKING
from PyQt6.QtWidgets import QWidget


if TYPE_CHECKING:
    from ...Environment import Environment


class ActionTypeBase:
    def get_id(self) -> str:
        raise NotImplementedError()

    def get_name(self) -> str:
        raise NotImplementedError()

    def get_config_widget(self, env: "Environment") -> QWidget:
        raise NotImplementedError()

    def update_config_widget(self, widget: QWidget, config: Any) -> None:
        raise NotImplementedError()

    def get_config_from_widget(self, widget: QWidget) -> Any:
        raise NotImplementedError()

    def get_list_text(self, config: Any) -> str:
        raise NotImplementedError()

    def execute_action(self, env: "Environment", config: Any) -> None:
        raise NotImplementedError()
