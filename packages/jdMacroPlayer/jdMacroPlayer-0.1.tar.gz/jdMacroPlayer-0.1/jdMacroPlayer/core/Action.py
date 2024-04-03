from .action_types.ActionTypeBase import ActionTypeBase
from .action_types import get_action_type_by_id
from typing import Type, Any


class Action:
    def __init__(self) -> None:
        self.type = ""
        self.config: Any = None

    @classmethod
    def from_save_data(cls: Type["Action"], data: dict[str, Any]) -> "Action":
        action = cls()

        action.type = data["type"]
        action.config = data["config"]

        return action

    def get_save_data(self) -> dict[str, Any]:
        return {
            "type": self.type,
            "config": self.config,
        }

    def get_type_object(self) -> ActionTypeBase | None:
        return get_action_type_by_id(self.type)

    def get_list_text(self) -> str:
        return self.get_type_object().get_list_text(self.config)
