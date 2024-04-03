from PyQt6.QtWidgets import QComboBox
from typing import Any
import os


def is_flatpak() -> bool:
    return os.path.exists("/.flatpak-info")


def select_combo_box_data(box: QComboBox, data: Any, default_index: int = 0) -> None:
    """Set the index to the item with the given data"""
    index = box.findData(data)
    if index == -1:
        box.setCurrentIndex(default_index)
    else:
        box.setCurrentIndex(index)
