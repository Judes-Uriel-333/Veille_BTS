import hashlib
import hmac
from app.services.db import get_conn
from app.utils.config import AppConfig

def _hash_password(password: str) -> str:
    # Hash simple + salt (OK BTS). On pourra upgrader plus tard (bcrypt).
    salt = AppConfig.password_salt().encode("utf-8")
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100_000).hex()

def register_user(email: str, password: str) -> None:
    email = email.strip().lower()
    password_hash = _hash_password(password)

    with get_conn() as conn:
        conn.execute(
            "INSERT INTO users(email, password_hash) VALUES (?, ?)",
            (email, password_hash)
        )
        conn.commit()

def authenticate_user(email: str, password: str) -> bool:
    email = email.strip().lower()
    password_hash = _hash_password(password)

    with get_conn() as conn:
        row = conn.execute(
            "SELECT password_hash FROM users WHERE email = ?",
            (email,)
        ).fetchone()

    if row is None:
        return False

    # comparaison sécurisée
    return hmac.compare_digest(row["password_hash"], password_hash)
