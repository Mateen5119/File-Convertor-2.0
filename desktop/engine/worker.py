"""Threaded conversion worker for desktop app.

Runs file conversions in a QThread to keep the UI responsive.
Emits signals on completion or error.
"""

from PyQt6.QtCore import QThread, pyqtSignal


class ConversionWorker(QThread):
    """Worker thread for file conversion.

    Signals:
        finished(bytes, str): Emitted with result bytes and output path on success.
        error(str): Emitted with error message on failure.
    """

    finished = pyqtSignal(bytes, str)
    error = pyqtSignal(str)

    def __init__(
        self,
        data: bytes,
        source_fmt: str,
        target_fmt: str,
        output_path: str,
    ) -> None:
        super().__init__()
        self.data = data
        self.source_fmt = source_fmt
        self.target_fmt = target_fmt
        self.output_path = output_path

    def run(self) -> None:
        try:
            from engine import convert

            result = convert(self.data, self.source_fmt, self.target_fmt, is_web=False)
            with open(self.output_path, "wb") as f:
                f.write(result)
            self.finished.emit(result, self.output_path)
        except Exception as e:
            self.error.emit(str(e))
