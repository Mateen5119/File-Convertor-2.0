from PyQt6.QtWidgets import QComboBox
from engine import CONVERSION_MAP

class FormatSelector(QComboBox):
    def __init__(self, source_ext: str):
        super().__init__()
        self.source_ext = source_ext.lower().lstrip(".")
        self.populate_targets()
        
    def populate_targets(self):
        targets = [target for src, target in CONVERSION_MAP.keys() if src == self.source_ext]
        if targets:
            self.addItems(targets)
        else:
            self.addItem("No formats available")
            self.setEnabled(False)
            
    def current_format(self):
        return self.currentText()
