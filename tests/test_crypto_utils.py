"""用标准测试向量验证密码学工具的正确性。

sha256_hex 的期望值来自 FIPS 180-4 / NIST 公布的样例：
    SHA256("") = e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    SHA256("abc") = ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from crypto_utils import derive_key, sha256_hex


def test_sha256_empty_string():
    assert sha256_hex(b"") == (
        "e3b0c44298fc1c149afbf4c8996fb924"
        "27ae41e4649b934ca495991b7852b855"
    )


def test_sha256_abc():
    assert sha256_hex(b"abc") == (
        "ba7816bf8f01cfea414140de5dae2223"
        "b00361a396177a9cb410ff61f20015ad"
    )


def test_derive_key_is_deterministic_and_length_correct():
    k1 = derive_key(b"secret", b"salt", length=32)
    k2 = derive_key(b"secret", b"salt", length=32)
    assert k1 == k2
    assert len(k1) == 32


def test_derive_key_salt_changes_output():
    assert derive_key(b"secret", b"salt1") != derive_key(b"secret", b"salt2")
