"""Database helpers for user auth and login history."""

from __future__ import annotations

import os
from typing import Any

import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "store_db"),
}


def get_connection():
    """Create and return a MySQL connection."""
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as exc:
        raise ConnectionError(f"Could not connect to database: {exc}") from exc


def get_user(username: str) -> dict[str, Any] | None:
    """Fetch one user by username."""
    query = """
        SELECT user_id, username, password_hash, role, created_at
        FROM Users
        WHERE username = %s
        LIMIT 1
    """
    connection = get_connection()
    try:
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute(query, (username,))
            return cursor.fetchone()
    finally:
        connection.close()


def create_user(username: str, password_hash: str, role: str) -> int:
    """Insert a new user and return created user_id."""
    query = """
        INSERT INTO Users (username, password_hash, role)
        VALUES (%s, %s, %s)
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (username, password_hash, role))
            connection.commit()
            return cursor.lastrowid
    finally:
        connection.close()


def add_login_history(username: str) -> None:
    """Insert a login history record for autocomplete."""
    query = "INSERT INTO LoginHistory (username) VALUES (%s)"
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (username,))
            connection.commit()
    finally:
        connection.close()


def get_recent_usernames(limit: int = 10) -> list[str]:
    """Return distinct recently used usernames ordered by latest login."""
    query = """
        SELECT username
        FROM LoginHistory
        GROUP BY username
        ORDER BY MAX(logged_in_at) DESC
        LIMIT %s
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (limit,))
            return [row[0] for row in cursor.fetchall()]
    finally:
        connection.close()
