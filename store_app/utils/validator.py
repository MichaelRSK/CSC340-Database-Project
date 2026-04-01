"""Input validation helpers for login and registration."""

from __future__ import annotations

from store_app.utils.constants import USERNAME_MAX_LENGTH


def validate_login(username: str, password: str) -> tuple[bool, str | None]:
    """
    Validate username and password for sign-in.
    Returns (ok, error_message). error_message is None when ok is True.
    """
    if not username or not username.strip():
        return False, "Username is required."
    name = username.strip()
    if len(name) > USERNAME_MAX_LENGTH:
        return False, f"Username must be at most {USERNAME_MAX_LENGTH} characters."
    if not password:
        return False, "Password is required."
    return True, None


def validate_new_account(
    username: str,
    password: str,
    confirm: str,
) -> tuple[bool, str | None]:
    """Validate fields for creating a new account."""
    ok, err = validate_login(username, password)
    if not ok:
        return False, err
    if password != confirm:
        return False, "Passwords do not match."
    return True, None
