"""Application entry: optional manager seed, login, and role-based dashboard."""

from __future__ import annotations

import os
import tkinter as tk
from tkinter import messagebox
from typing import Any

from store_app.auth import seed_manager_account
from store_app.ui.employee_frame import EmployeeDashboardFrame
from store_app.ui.login_frame import LoginFrame
from store_app.ui.manager_frame import ManagerDashboardFrame
from store_app.utils.constants import BACKGROUND_COLOR, WINDOW_HEIGHT, WINDOW_WIDTH


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

    def show_login() -> None:
        root.title("Store Manager — Sign In")
        _clear_children(container)
        LoginFrame(container, on_login_success=on_login_success).pack(
            fill=tk.BOTH, expand=True
        )

    def on_logout() -> None:
        show_login()

    def on_login_success(user: dict[str, Any]) -> None:
        role = user.get("role")
        if role not in ("manager", "employee"):
            messagebox.showerror("Sign in", "Unknown role; cannot open dashboard.")
            return

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

    show_login()
    root.mainloop()


if __name__ == "__main__":
    main()
