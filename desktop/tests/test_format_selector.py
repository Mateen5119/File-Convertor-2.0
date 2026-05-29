import pytest
from PyQt6.QtWidgets import QApplication
from ui.format_selector import FormatSelector

def test_format_selector_valid_source():
    app = QApplication.instance() or QApplication([])
    selector = FormatSelector("png")
    
    # Should contain at least jpg
    items = [selector.itemText(i) for i in range(selector.count())]
    assert "jpg" in items
    assert selector.isEnabled()

def test_format_selector_invalid_source():
    app = QApplication.instance() or QApplication([])
    selector = FormatSelector("unknownext")
    
    assert selector.count() == 1
    assert selector.itemText(0) == "No formats available"
    assert not selector.isEnabled()
