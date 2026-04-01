"""Application entry: optional manager seed and login UI."""

from __future__ import annotations

import os
import tkinter as tk
from tkinter import messagebox
from typing import Any

from store_app.auth import seed_manager_account
from store_app.ui.login_frame import LoginFrame
from store_app.utils.constants import BACKGROUND_COLOR, WINDOW_HEIGHT, WINDOW_WIDTH


def _env_flag(name: str, default: str = "true") -> bool:
    return os.getenv(name, default).strip().lower() in ("1", "true", "yes", "on")


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
    root.title("Store Manager — Sign In")
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    root.minsize(900, 560)
    root.configure(bg=BACKGROUND_COLOR)

    def on_login_success(user: dict[str, Any]) -> None:
        role = user.get("role", "")
        username = user.get("username", "")
        messagebox.showinfo(
            "Signed in",
            f"Welcome, {username}.\nRole: {role}\n\n"
            "The dashboard will load here in Phase 5.",
        )
        root.destroy()

    frame = LoginFrame(root, on_login_success=on_login_success)
    frame.pack(fill=tk.BOTH, expand=True)
    root.mainloop()


if __name__ == "__main__":
    main()
