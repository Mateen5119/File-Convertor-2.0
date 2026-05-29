import pytest
from engine.font import ttf_to_woff2, otf_to_woff2

def test_ttf_to_woff2(sample_ttf):
    result = ttf_to_woff2(sample_ttf)
    assert result.startswith(b'wOF2')

def test_otf_to_woff2(sample_otf):
    result = otf_to_woff2(sample_otf)
    assert result.startswith(b'wOF2')
