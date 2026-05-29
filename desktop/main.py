import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QSharedMemory
import dotenv
from ui.main_window import MainWindow

def load_stylesheet(app: QApplication, theme_name: str):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    qss_path = os.path.join(script_dir, "ui", "styles", f"{theme_name}.qss")
    try:
        with open(qss_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print(f"Warning: Stylesheet {qss_path} not found.")

def main():
    # ISS-017: Multi-instance application lock to coordinate with Inno Setup installer upgrades
    shared_mem = QSharedMemory("FileHarborInstanceMutex")
    if not shared_mem.create(1):
        # Mutex lock exists; exit cleanly to prevent GUI conflicts
        sys.exit(0)

    # Initialize environment variables using python-dotenv
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dotenv.load_dotenv(os.path.join(script_dir, ".env"))

    app = QApplication(sys.argv)
    app.setApplicationName("FileHarbor")
    app.setOrganizationName("FileHarborSolutions")
    
    # Load dark theme by default
    load_stylesheet(app, "dark")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
