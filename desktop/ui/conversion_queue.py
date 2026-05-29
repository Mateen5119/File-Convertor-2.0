from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QProgressBar, QScrollArea
from PyQt6.QtCore import pyqtSignal, Qt
from pathlib import Path
from ui.format_selector import FormatSelector
from engine.worker import ConversionWorker

class QueueRow(QWidget):
    removed = pyqtSignal(object) # self
    
    def __init__(self, file_path: Path):
        super().__init__()
        self.file_path = file_path
        self.setObjectName("glassCardRow")
        self.worker = None
        
        layout = QHBoxLayout(self)
        
        self.name_label = QLabel(file_path.name)
        self.name_label.setObjectName("labelPrimary")
        layout.addWidget(self.name_label)
        
        size_mb = file_path.stat().st_size / (1024 * 1024)
        self.size_label = QLabel(f"{size_mb:.2f} MB")
        self.size_label.setObjectName("labelOutline")
        layout.addWidget(self.size_label)
        
        self.format_selector = FormatSelector(file_path.suffix)
        layout.addWidget(self.format_selector)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel()
        self.status_label.hide()
        layout.addWidget(self.status_label)
        
        self.convert_btn = QPushButton("Convert")
        self.convert_btn.setObjectName("primaryBtn")
        self.convert_btn.clicked.connect(self.start_conversion)
        layout.addWidget(self.convert_btn)
        
        self.remove_btn = QPushButton("X")
        self.remove_btn.clicked.connect(lambda: self.removed.emit(self))
        layout.addWidget(self.remove_btn)
        
    def start_conversion(self):
        target_fmt = self.format_selector.current_format()
        if not target_fmt or not self.format_selector.isEnabled():
            return
            
        self.convert_btn.setEnabled(False)
        self.remove_btn.setEnabled(False)
        self.format_selector.setEnabled(False)
        self.progress_bar.show()
        self.progress_bar.setRange(0, 0) # Indeterminate
        
        try:
            with open(self.file_path, "rb") as f:
                data = f.read()
        except Exception as e:
            self.conversion_error(str(e))
            return
            
        output_path = str(self.file_path.with_suffix(f".{target_fmt}"))
        source_fmt = self.file_path.suffix.lstrip(".").lower()
        
        self.worker = ConversionWorker(data, source_fmt, target_fmt, output_path)
        self.worker.finished.connect(self.conversion_finished)
        self.worker.error.connect(self.conversion_error)
        self.worker.start()
        
    def conversion_finished(self, result: bytes, output_path: str):
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(100)
        self.status_label.setText(f"Saved: {Path(output_path).name}")
        self.status_label.setObjectName("labelTertiary")
        self.status_label.show()
        self.remove_btn.setEnabled(True)
        
    def conversion_error(self, error_msg: str):
        self.progress_bar.hide()
        self.status_label.setText(f"Error: {error_msg}")
        self.status_label.setObjectName("labelError")
        self.status_label.show()
        self.convert_btn.setEnabled(True)
        self.remove_btn.setEnabled(True)
        self.format_selector.setEnabled(True)

class ConversionQueueWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setObjectName("glassCard")
        
        self.queue_container = QWidget()
        self.queue_layout = QVBoxLayout(self.queue_container)
        self.queue_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.scroll_area.setWidget(self.queue_container)
        layout.addWidget(self.scroll_area)
        
    def add_files(self, file_paths: list[Path]):
        for path in file_paths:
            row = QueueRow(path)
            row.removed.connect(self.remove_row)
            self.queue_layout.addWidget(row)
            
    def remove_row(self, row: QueueRow):
        self.queue_layout.removeWidget(row)
        row.deleteLater()
