"""Threaded conversion worker for desktop app.

Runs file conversions in a QThread to keep the UI responsive.
Emits signals on completion or error.
"""

from PyQt6.QtCore import QThread, pyqtSignal
from pathlib import Path


class ConversionWorker(QThread):
    """Worker thread for file conversion.

    Signals:
        finished(str): Emitted with output path on success.
        error(str): Emitted with error message on failure.
    """

    # ISS-024: finished signal emits output path string only (prevents memory bloat)
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(
        self,
        input_path: Path,
        source_fmt: str,
        target_fmt: str,
        output_path: str,
    ) -> None:
        super().__init__()
        self.input_path = input_path
        self.source_fmt = source_fmt
        self.target_fmt = target_fmt
        self.output_path = output_path

    def run(self) -> None:
        try:
            # ISS-015: Stream / read files in background thread to prevent UI freezing
            data = self.input_path.read_bytes()
            
            from engine import convert
            # Execute conversion router with is_web=False for desktop
            result = convert(data, self.source_fmt, self.target_fmt, is_web=False)
            
            # Write bytes to destination
            with open(self.output_path, "wb") as f:
                f.write(result)
                
            self.finished.emit(self.output_path)
        except Exception as e:
            self.error.emit(str(e))
