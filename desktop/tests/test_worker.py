import pytest
from PyQt6.QtCore import QCoreApplication
from engine.worker import ConversionWorker
import tempfile
from pathlib import Path
import base64

def test_worker_success(qtbot):
    app = QCoreApplication.instance() or QCoreApplication([])
    
    # 1x1 PNG data
    png_data = base64.b64decode(b"iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=")
    
    with tempfile.TemporaryDirectory() as td:
        out_path = str(Path(td) / "out.jpg")
        
        worker = ConversionWorker(png_data, "png", "jpg", out_path)
        
        with qtbot.waitSignal(worker.finished, timeout=2000) as blocker:
            worker.start()
            
        assert blocker.args[1] == out_path
        assert Path(out_path).exists()
        
def test_worker_error(qtbot):
    app = QCoreApplication.instance() or QCoreApplication([])
    
    # Invalid data for conversion
    invalid_data = b"not an image"
    
    with tempfile.TemporaryDirectory() as td:
        out_path = str(Path(td) / "out.jpg")
        
        worker = ConversionWorker(invalid_data, "png", "jpg", out_path)
        
        with qtbot.waitSignal(worker.error, timeout=2000) as blocker:
            worker.start()
            
        assert blocker.args[0] is not None
