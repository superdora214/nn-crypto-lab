"""密码学工具模块示例。

约定：本目录下每个核心函数都应有对应测试。涉及密码学的函数
用标准测试向量（如 NIST / RFC 文档给出的样例）验证正确性。
"""
import hashlib


def sha256_hex(data: bytes) -> str:
    """计算 SHA-256 摘要的十六进制表示。"""
    return hashlib.sha256(data).hexdigest()


def derive_key(secret: bytes, salt: bytes, length: int = 32) -> bytes:
    """从口令派生密钥。

    TODO: 换成课题实际用到的 KDF（如 HKDF / Argon2）。
    """
    return hashlib.pbkdf2_hmac("sha256", secret, salt, 100_000, dklen=length)
