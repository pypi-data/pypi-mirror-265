from typing import Type, Any
from .Action import Action


class Macro:
    def __init__(self) -> None:
        self.id = ""
        self.name = ""
        self.description = ""
        self.actions: list[Action] = []

    @classmethod
    def from_save_data(cls: Type["Macro"], data: dict[str, Any]) -> "Macro":
        macro = cls()

        macro.id = data["id"]
        macro.name = data["name"]
        macro.description = data["description"]

        for i in data["actions"]:
            macro.actions.append(Action.from_save_data(i))

        return macro

    def get_save_data(self) -> dict[str, Any]:
        data = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "actions": [],
        }

        for action in self.actions:
            data["actions"].append(action.get_save_data())

        return data
