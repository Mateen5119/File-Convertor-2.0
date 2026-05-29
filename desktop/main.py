import sys
import os
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow

def load_stylesheet(app: QApplication, theme_name: str):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    qss_path = os.path.join(script_dir, "ui", "styles", f"{theme_name}.qss")
    try:
        with open(qss_path, "r") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print(f"Warning: Stylesheet {qss_path} not found.")

def main():
    app = QApplication(sys.argv)
    
    # Load dark theme by default
    load_stylesheet(app, "dark")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
