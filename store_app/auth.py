"""Authentication logic: hashing, login checks, account creation, inactivity timeout."""

from __future__ import annotations

import hashlib
import os
import time
from typing import Any

import bcrypt
from mysql.connector import IntegrityError

from store_app.db import add_login_history, create_user, get_user
from store_app.utils.constants import INACTIVITY_TIMEOUT_SECONDS


def hash_password(password: str) -> str:
    """Hash password with bcrypt and return utf-8 string."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(password: str, stored_hash: str) -> bool:
    """Verify password against stored hash (supports legacy SHA256 hashes)."""
    if stored_hash.startswith("$2"):
        return bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8"))

    # Backward-compatible fallback if a legacy SHA256 hash exists.
    return hashlib.sha256(password.encode("utf-8")).hexdigest() == stored_hash


def verify_login(username: str, password: str) -> dict[str, Any] | None:
    """
    Validate credentials against DB.
    Returns user dict (includes role) on success, otherwise None.
    """
    user = get_user(username)
    if not user:
        return None

    if not verify_password(password, user["password_hash"]):
        return None

    add_login_history(username)
    return user


def create_account(username: str, password: str, role: str) -> int:
    """Create a user account with hashed password."""
    if role not in {"owner", "manager", "employee"}:
        raise ValueError("Role must be 'owner', 'manager', or 'employee'.")
    if not username or not password:
        raise ValueError("Username and password are required.")

    password_hash = hash_password(password)
    try:
        return create_user(username, password_hash, role)
    except IntegrityError as exc:
        raise ValueError("Username already exists.") from exc


class SessionTimer:
    """Tracks user activity and determines inactivity timeout."""

    def __init__(self, timeout_seconds: int = INACTIVITY_TIMEOUT_SECONDS) -> None:
        self.timeout_seconds = timeout_seconds
        self._last_activity = time.time()

    def touch(self) -> None:
        """Reset last activity timestamp."""
        self._last_activity = time.time()

    def seconds_until_timeout(self) -> int:
        """Return remaining active seconds before timeout."""
        elapsed = int(time.time() - self._last_activity)
        remaining = self.timeout_seconds - elapsed
        return max(0, remaining)

    def is_timed_out(self) -> bool:
        """Return True when inactivity timeout has elapsed."""
        return self.seconds_until_timeout() == 0


def seed_manager_account() -> bool:
    """
    Seed a manager account from env vars.
    Returns True if account created, False if user already exists.
    """
    username = os.getenv("SEED_MANAGER_USERNAME", "manager")
    password = os.getenv("SEED_MANAGER_PASSWORD", "ChangeMe123!")

    if get_user(username):
        return False

    create_account(username, password, "manager")
    return True
