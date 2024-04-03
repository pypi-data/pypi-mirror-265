from typing import Any
import json
import os


class Settings:
    def __init__(self, save_path: str) -> None:
        self._save_path = save_path

        self._default_settings = {
            "language": "default",
            "welcomeDialogStartup": True,
        }

        self._user_settings = {}

    def get(self, key: str) -> Any:
        """Returns the given setting"""
        if key in self._user_settings:
            return self._user_settings[key]
        elif key in self._default_settings:
            return self._default_settings[key]
        else:
            return None

    def set(self, key: str, value: Any):
        """Set the value of a setting"""
        self._user_settings[key] = value

    def save(self):
        """Save settings into file"""
        if len(self._user_settings) == 0 and not os.path.isfile(self._save_path):
            return

        try:
            os.makedirs(os.path.dirname(self._save_path))
        except FileExistsError:
            pass

        with open(self._save_path, "w", encoding="utf-8") as f:
            json.dump(self._user_settings, f, ensure_ascii=False, indent=4)

    def load(self) -> None:
        """Load settings from file"""
        if not os.path.isfile(self._save_path):
            return

        with open(self._save_path, "r", encoding="utf-8") as f:
            self._user_settings = json.load(f)

    def reset(self) -> None:
        """Resets all settings to the default values"""
        self._user_settings.clear()
