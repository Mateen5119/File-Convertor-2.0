import pytest
from engine.archive import rar_to_zip
import shutil

@pytest.mark.skipif(shutil.which('unrar') is None, reason="Requires unrar")
def test_rar_to_zip(sample_rar):
    result = rar_to_zip(sample_rar)
    assert result.startswith(b'PK\x03\x04')
