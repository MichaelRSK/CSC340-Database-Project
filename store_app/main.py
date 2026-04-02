"""Application entry: optional manager seed, login, and role-based dashboard."""

from __future__ import annotations

import os
import tkinter as tk
from tkinter import messagebox
from typing import Any

from store_app.auth import SessionTimer, seed_manager_account
from store_app.ui.employee_frame import EmployeeDashboardFrame
from store_app.ui.login_frame import LoginFrame
from store_app.ui.manager_frame import ManagerDashboardFrame
from store_app.utils.constants import (
    BACKGROUND_COLOR,
    INACTIVITY_TIMEOUT_SECONDS,
    INACTIVITY_WARNING_SECONDS,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)


def _env_flag(name: str, default: str = "true") -> bool:
    return os.getenv(name, default).strip().lower() in ("1", "true", "yes", "on")


def _clear_children(parent: tk.Misc) -> None:
    for child in parent.winfo_children():
        child.destroy()


def main() -> None:
    if _env_flag("SEED_MANAGER_ON_START", "true"):
        created = seed_manager_account()
        if created:
            print("Manager seed account created.")
        else:
            print("Manager seed account already exists.")
    else:
        print("Skipping manager seed (SEED_MANAGER_ON_START is false).")

    root = tk.Tk()
    root.title("Store Manager")
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    root.minsize(900, 560)
    root.configure(bg=BACKGROUND_COLOR)

    container = tk.Frame(root, bg=BACKGROUND_COLOR)
    container.pack(fill=tk.BOTH, expand=True)
    current_user: dict[str, Any] | None = None
    session_timer: SessionTimer | None = None
    warning_dialog: tk.Toplevel | None = None
    warning_after_id: str | None = None
    monitor_after_id: str | None = None

    def _cancel_warning_timer() -> None:
        nonlocal warning_after_id
        if warning_after_id:
            root.after_cancel(warning_after_id)
            warning_after_id = None

    def _close_warning_dialog() -> None:
        nonlocal warning_dialog
        _cancel_warning_timer()
        if warning_dialog and warning_dialog.winfo_exists():
            warning_dialog.destroy()
        warning_dialog = None

    def _reset_activity(_event: tk.Event | None = None) -> None:
        if current_user and session_timer:
            session_timer.touch()
            if warning_dialog and warning_dialog.winfo_exists():
                _close_warning_dialog()

    def _force_logout_due_to_timeout() -> None:
        messagebox.showwarning(
            "Session timed out",
            "Your session has expired due to inactivity. Please sign in again.",
        )
        on_logout()

    def _start_warning_countdown(seconds_left: int, label: tk.Label) -> None:
        nonlocal warning_after_id
        if not current_user or not session_timer:
            _close_warning_dialog()
            return
        if warning_dialog is None or not warning_dialog.winfo_exists():
            return

        if seconds_left <= 0:
            _close_warning_dialog()
            _force_logout_due_to_timeout()
            return

        label.configure(
            text=f"You will be logged out in {seconds_left} seconds due to inactivity."
        )
        warning_after_id = root.after(
            1000, lambda: _start_warning_countdown(seconds_left - 1, label)
        )

    def _show_timeout_warning() -> None:
        nonlocal warning_dialog
        if warning_dialog and warning_dialog.winfo_exists():
            return

        warning_dialog = tk.Toplevel(root)
        warning_dialog.title("Inactivity warning")
        warning_dialog.configure(bg=BACKGROUND_COLOR)
        warning_dialog.transient(root)
        warning_dialog.grab_set()
        warning_dialog.resizable(False, False)
        warning_dialog.protocol("WM_DELETE_WINDOW", lambda: None)

        frame = tk.Frame(warning_dialog, bg=BACKGROUND_COLOR, padx=24, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            frame,
            text="Inactivity detected",
            font=("Segoe UI", 12, "bold"),
            bg=BACKGROUND_COLOR,
        ).pack(anchor="w", pady=(0, 8))

        countdown_label = tk.Label(
            frame,
            text="",
            font=("Segoe UI", 10),
            bg=BACKGROUND_COLOR,
            justify=tk.LEFT,
            wraplength=360,
        )
        countdown_label.pack(anchor="w", pady=(0, 14))

        tk.Button(
            frame,
            text="Stay signed in",
            command=lambda: _reset_activity(None),
            padx=12,
            pady=6,
        ).pack(anchor="e")

        warning_dialog.update_idletasks()
        x = root.winfo_rootx() + (root.winfo_width() // 2) - (warning_dialog.winfo_width() // 2)
        y = root.winfo_rooty() + (root.winfo_height() // 2) - (warning_dialog.winfo_height() // 2)
        warning_dialog.geometry(f"+{x}+{y}")

        _start_warning_countdown(INACTIVITY_WARNING_SECONDS, countdown_label)

    def _monitor_inactivity() -> None:
        nonlocal monitor_after_id
        if current_user and session_timer and session_timer.is_timed_out():
            _show_timeout_warning()
        monitor_after_id = root.after(1000, _monitor_inactivity)

    def show_login() -> None:
        nonlocal current_user, session_timer
        root.title("Store Manager — Sign In")
        current_user = None
        session_timer = None
        _close_warning_dialog()
        _clear_children(container)
        LoginFrame(container, on_login_success=on_login_success).pack(
            fill=tk.BOTH, expand=True
        )

    def on_logout() -> None:
        show_login()

    def on_login_success(user: dict[str, Any]) -> None:
        nonlocal current_user, session_timer
        role = user.get("role")
        if role not in ("manager", "employee"):
            messagebox.showerror("Sign in", "Unknown role; cannot open dashboard.")
            return

        current_user = user
        session_timer = SessionTimer(timeout_seconds=INACTIVITY_TIMEOUT_SECONDS)
        _reset_activity(None)
        root.title("Store Manager — Dashboard")
        _clear_children(container)

        if role == "manager":
            ManagerDashboardFrame(
                container,
                user=user,
                on_logout=on_logout,
            ).pack(fill=tk.BOTH, expand=True)
        else:
            EmployeeDashboardFrame(
                container,
                user=user,
                on_logout=on_logout,
            ).pack(fill=tk.BOTH, expand=True)

    root.bind_all("<Any-KeyPress>", _reset_activity)
    root.bind_all("<Any-ButtonPress>", _reset_activity)
    root.bind_all("<Motion>", _reset_activity)

    show_login()
    _monitor_inactivity()
    try:
        root.mainloop()
    finally:
        if monitor_after_id:
            root.after_cancel(monitor_after_id)


if __name__ == "__main__":
    main()
