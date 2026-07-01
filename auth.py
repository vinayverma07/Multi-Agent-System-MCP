import os
import hashlib
import binascii
from datetime import datetime

from dotenv import load_dotenv
import psycopg

load_dotenv(override=True)

DATABASE_URL = os.getenv("DATABASE_URL")


def get_conn():
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not set in environment")
    return psycopg.connect(DATABASE_URL)


def init_db():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    salt TEXT NOT NULL,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                );
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS user_history (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    query TEXT NOT NULL,
                    plan TEXT NOT NULL,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                );
                """
            )
        conn.commit()


def hash_password(password: str, salt: bytes | None = None) -> tuple[str, str]:
    if salt is None:
        salt = os.urandom(16)
    hashed = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 200_000)
    return binascii.hexlify(hashed).decode("ascii"), binascii.hexlify(salt).decode("ascii")


def create_user(username: str, password: str) -> tuple[bool, str]:
    normalized = username.strip().lower()
    if not normalized or not password:
        return False, "Username and password are required."

    password_hash, salt = hash_password(password)
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO users (username, password_hash, salt) VALUES (%s, %s, %s) RETURNING id",
                    (normalized, password_hash, salt),
                )
                user_id = cur.fetchone()[0]
            conn.commit()
        return True, str(user_id)
    except psycopg.errors.UniqueViolation:
        return False, "This username is already taken."
    except Exception as exc:
        return False, str(exc)


def verify_user(username: str, password: str) -> tuple[bool, str | None]:
    normalized = username.strip().lower()
    if not normalized or not password:
        return False, "Username and password are required."

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, password_hash, salt FROM users WHERE username = %s",
                (normalized,),
            )
            row = cur.fetchone()
            if not row:
                return False, "Invalid username or password."
            user_id, stored_hash, salt_hex = row

    salt = binascii.unhexlify(salt_hex.encode("ascii"))
    computed_hash, _ = hash_password(password, salt)
    if computed_hash != stored_hash:
        return False, "Invalid username or password."
    return True, str(user_id)


def get_history(user_id: str, limit: int = 10) -> list[dict]:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT query, plan, created_at FROM user_history WHERE user_id = %s ORDER BY created_at DESC LIMIT %s",
                (user_id, limit),
            )
            rows = cur.fetchall()
    return [
        {
            "query": row[0],
            "plan": row[1],
            "created_at": row[2].isoformat() if isinstance(row[2], datetime) else str(row[2]),
        }
        for row in rows
    ]


def save_history(user_id: str, query: str, plan: str) -> None:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO user_history (user_id, query, plan) VALUES (%s, %s, %s)",
                (user_id, query, plan),
            )
        conn.commit()
