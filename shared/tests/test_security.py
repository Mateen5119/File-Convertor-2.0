import pytest
from engine.security import pem_to_crt, pem_to_pfx

def test_pem_to_crt(sample_pem):
    result = pem_to_crt(sample_pem)
    assert b"BEGIN CERTIFICATE" in result or b"END CERTIFICATE" in result
