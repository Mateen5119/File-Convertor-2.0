from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QPushButton, QLabel, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt, QPoint, QSettings
from ui.drop_zone import DropZone
from ui.conversion_queue import ConversionQueueWidget

try:
    from features.editor.pdf_editor import PDFEditorWidget
    from features.editor.docx_editor import DocxEditorWidget
    EDITOR_AVAILABLE = True
except ImportError:
    EDITOR_AVAILABLE = False

try:
    from features.compressor import CompressorWidget
    COMPRESSOR_AVAILABLE = True
except ImportError:
    COMPRESSOR_AVAILABLE = False

class TitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setObjectName("titleBar")
        self.setFixedHeight(40)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 0)
        
        self.close_btn = QPushButton()
        self.close_btn.setObjectName("macCloseBtn")
        self.close_btn.setFixedSize(12, 12)
        self.close_btn.clicked.connect(self.parent.close)
        
        self.min_btn = QPushButton()
        self.min_btn.setObjectName("macMinBtn")
        self.min_btn.setFixedSize(12, 12)
        self.min_btn.clicked.connect(self.parent.showMinimized)
        
        self.max_btn = QPushButton()
        self.max_btn.setObjectName("macMaxBtn")
        self.max_btn.setFixedSize(12, 12)
        self.max_btn.clicked.connect(self.toggle_maximize)
        
        layout.addWidget(self.close_btn)
        layout.addWidget(self.min_btn)
        layout.addWidget(self.max_btn)
        
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        layout.addItem(spacer)
        
        title = QLabel("File Harbor")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        spacer2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        layout.addItem(spacer2)
        
        self.start_pos = None

    def toggle_maximize(self):
        if self.parent.isMaximized():
            self.parent.showNormal()
        else:
            self.parent.showMaximized()
            
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.start_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.start_pos is not None:
            delta = event.globalPosition().toPoint() - self.start_pos
            self.parent.move(self.parent.pos() + delta)
            self.start_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.start_pos = None

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Window)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(800, 600)
        
        self.settings = QSettings("Web Harbor Solutions", "File Harbor")
        
        central_widget = QWidget()
        central_widget.setObjectName("mainContainer")
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.title_bar = TitleBar(self)
        layout.addWidget(self.title_bar)
        
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        
        self.setup_convert_tab()
        self.setup_edit_tab()
        self.setup_compress_tab()
        
    def setup_convert_tab(self):
        convert_tab = QWidget()
        convert_layout = QVBoxLayout(convert_tab)
        
        self.drop_zone = DropZone()
        self.conversion_queue = ConversionQueueWidget()
        
        self.drop_zone.filesDropped.connect(self.conversion_queue.add_files)
        
        convert_layout.addWidget(self.drop_zone)
        convert_layout.addWidget(self.conversion_queue)
        
        self.tabs.addTab(convert_tab, "Convert")
        
    def setup_edit_tab(self):
        edit_tab = QWidget()
        edit_layout = QVBoxLayout(edit_tab)
        
        if EDITOR_AVAILABLE:
            editor_tabs = QTabWidget()
            editor_tabs.addTab(PDFEditorWidget(), "PDF Editor")
            editor_tabs.addTab(DocxEditorWidget(), "DOCX Editor")
            edit_layout.addWidget(editor_tabs)
        else:
            label = QLabel("Editor features currently unavailable (missing dependencies).")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            edit_layout.addWidget(label)
            
        self.tabs.addTab(edit_tab, "Edit")
        
    def setup_compress_tab(self):
        if COMPRESSOR_AVAILABLE:
            self.tabs.addTab(CompressorWidget(), "Compress")
        else:
            compress_tab = QWidget()
            layout = QVBoxLayout(compress_tab)
            label = QLabel("Compressor features currently unavailable (missing dependencies).")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(label)
            self.tabs.addTab(compress_tab, "Compress")
