#from .core.MacroManager import MacroManager
from .core.Settings import Settings
import json
import os


class Environment:
    def __init__(self) -> None:
        self.program_dir = os.path.dirname(__file__)
        self.data_dir = os.path.join(os.getenv("XDG_DATA_HOME", os.path.expanduser("~/.local/share")), "JakobDev", "jdMacroPlayer")

        self.settings = Settings(os.path.join(self.data_dir, "settings.json"))
        self.settings.load()

        from .core.MacroManager import MacroManager

        self.macro_manager = MacroManager(self)
        self.macro_manager.load_file()

        with open(os.path.join(self.program_dir, "Version.txt"), "r", encoding="utf-8") as f:
            self.version = f.read().strip()

        with open(os.path.join(self.program_dir, "data", "keycodes.json"), "r", encoding="utf-8")as f:
            self.keycodes = json.load(f)
