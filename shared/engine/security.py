"""Security/certificate conversion module.

Handles: pem→pfx, pem→crt
"""

import re
from .validator import validate


def pem_to_pfx(data: bytes, is_web: bool = False, password: bytes = b"changeme") -> bytes:
    """Convert combined PEM (key + cert) to PFX/PKCS12 format."""
    validate(data, "pem", is_web=is_web)
    
    from cryptography.hazmat.primitives.serialization import (
        pkcs12, load_pem_private_key,
    )
    from cryptography.x509 import load_pem_x509_certificate

    # Extract private key
    key_match = re.search(
        b"(-----BEGIN (?:RSA )?PRIVATE KEY-----.*?-----END (?:RSA )?PRIVATE KEY-----)",
        data,
        re.DOTALL,
    )
    if not key_match:
        raise ValueError("No private key block found in PEM")

    # Extract certificate
    cert_match = re.search(
        b"(-----BEGIN CERTIFICATE-----.*?-----END CERTIFICATE-----)",
        data,
        re.DOTALL,
    )
    if not cert_match:
        raise ValueError("No certificate block found in PEM")

    private_key = load_pem_private_key(key_match.group(1), password=None)
    cert = load_pem_x509_certificate(cert_match.group(1))

    pfx = pkcs12.serialize_key_and_certificates(
        name=b"fileharbor",
        key=private_key,
        cert=cert,
        cas=None,
        encryption_algorithm=pkcs12.BestAvailableEncryption(password),
    )
    return pfx


def pem_to_crt(data: bytes, is_web: bool = False) -> bytes:
    """Extract the certificate block from a PEM file (already .crt-compatible)."""
    validate(data, "pem", is_web=is_web)
    
    match = re.search(
        b"(-----BEGIN CERTIFICATE-----.*?-----END CERTIFICATE-----)",
        data,
        re.DOTALL,
    )
    if not match:
        raise ValueError("No certificate block found in PEM")
    return match.group(1)
