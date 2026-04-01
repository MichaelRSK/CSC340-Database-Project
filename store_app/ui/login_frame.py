"""Login screen: autocomplete usernames, validation, and role-based handoff."""

from __future__ import annotations

import tkinter as tk
from collections.abc import Callable
from tkinter import messagebox, ttk
from typing import Any

from store_app.auth import create_account, verify_login
from store_app.db import count_users, get_recent_usernames
from store_app.utils.constants import (
    ACTION_COLOR,
    ALERT_COLOR,
    BACKGROUND_COLOR,
    FONT_BODY,
    FONT_BUTTON,
    FONT_HEADING,
    FONT_SMALL,
    PRIMARY_COLOR,
)
from store_app.utils.validator import validate_login, validate_new_account

OnLoginSuccess = Callable[[dict[str, Any]], None]


class LoginFrame(tk.Frame):
    """
    Username (with autocomplete), masked password, Sign In, optional Create Account,
    and an error message area. Calls on_login_success with the user dict from the DB.
    """

    def __init__(
        self,
        master: tk.Misc,
        on_login_success: OnLoginSuccess,
    ) -> None:
        super().__init__(master, bg=BACKGROUND_COLOR)
        self._on_login_success = on_login_success
        self._username_var = tk.StringVar()
        self._password_var = tk.StringVar()

        self._build_layout()
        self._refresh_username_list()
        self._update_create_account_visibility()

    def _build_layout(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        card = tk.Frame(self, bg=BACKGROUND_COLOR, padx=48, pady=48)
        card.grid(row=0, column=0)

        title = tk.Label(
            card,
            text="Store Manager",
            font=FONT_HEADING,
            fg=PRIMARY_COLOR,
            bg=BACKGROUND_COLOR,
        )
        title.grid(row=0, column=0, columnspan=2, pady=(0, 8))

        subtitle = tk.Label(
            card,
            text="Sign in to continue",
            font=FONT_SMALL,
            fg=PRIMARY_COLOR,
            bg=BACKGROUND_COLOR,
        )
        subtitle.grid(row=1, column=0, columnspan=2, pady=(0, 28))

        tk.Label(
            card,
            text="Username",
            font=FONT_BODY,
            fg=PRIMARY_COLOR,
            bg=BACKGROUND_COLOR,
            anchor="w",
        ).grid(row=2, column=0, sticky="ew", pady=(0, 6))
        self._username_combo = ttk.Combobox(
            card,
            textvariable=self._username_var,
            width=36,
            font=FONT_BODY,
        )
        self._username_combo.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 16))
        self._username_combo.bind("<FocusIn>", lambda _e: self._refresh_username_list())

        tk.Label(
            card,
            text="Password",
            font=FONT_BODY,
            fg=PRIMARY_COLOR,
            bg=BACKGROUND_COLOR,
            anchor="w",
        ).grid(row=4, column=0, sticky="ew", pady=(0, 6))
        self._password_entry = tk.Entry(
            card,
            textvariable=self._password_var,
            show="•",
            width=40,
            font=FONT_BODY,
            fg=PRIMARY_COLOR,
            bg="#FFFFFF",
            insertbackground=PRIMARY_COLOR,
            relief=tk.FLAT,
            highlightthickness=1,
            highlightbackground="#CCCCCC",
            highlightcolor=ACTION_COLOR,
        )
        self._password_entry.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(0, 12))

        self._error_var = tk.StringVar()
        self._error_label = tk.Label(
            card,
            textvariable=self._error_var,
            font=FONT_SMALL,
            fg=ALERT_COLOR,
            bg=BACKGROUND_COLOR,
            wraplength=420,
            justify="center",
        )
        self._error_label.grid(row=6, column=0, columnspan=2, pady=(0, 16))

        btn_row = tk.Frame(card, bg=BACKGROUND_COLOR)
        btn_row.grid(row=7, column=0, columnspan=2, pady=(8, 0))

        self._sign_in_btn = tk.Button(
            btn_row,
            text="Sign In",
            font=FONT_BUTTON,
            fg="#FFFFFF",
            bg=ACTION_COLOR,
            activebackground=PRIMARY_COLOR,
            activeforeground="#FFFFFF",
            relief=tk.FLAT,
            padx=28,
            pady=10,
            cursor="hand2",
            command=self._on_sign_in,
        )
        self._sign_in_btn.pack(side=tk.LEFT, padx=(0, 12))

        self._create_btn = tk.Button(
            btn_row,
            text="Create Account",
            font=FONT_BUTTON,
            fg=PRIMARY_COLOR,
            bg="#FFFFFF",
            activebackground=BACKGROUND_COLOR,
            activeforeground=PRIMARY_COLOR,
            relief=tk.SOLID,
            borderwidth=1,
            highlightbackground=PRIMARY_COLOR,
            padx=20,
            pady=10,
            cursor="hand2",
            command=self._open_create_account_dialog,
        )

        self._password_entry.bind("<Return>", lambda _e: self._on_sign_in())
        self._username_combo.bind("<Return>", lambda _e: self._on_sign_in())

        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TCombobox", fieldbackground="#FFFFFF", foreground=PRIMARY_COLOR)

    def _clear_error(self) -> None:
        self._error_var.set("")

    def _set_error(self, message: str) -> None:
        self._error_var.set(message)

    def _refresh_username_list(self) -> None:
        try:
            names = get_recent_usernames()
        except (ConnectionError, OSError) as exc:
            self._set_error(f"Could not load recent usernames: {exc}")
            names = []
        self._username_combo["values"] = names

    def _update_create_account_visibility(self) -> None:
        """Show Create Account only before any user exists (first-run bootstrap)."""
        try:
            total = count_users()
        except (ConnectionError, OSError) as exc:
            self._set_error(f"Database error: {exc}")
            total = -1
        if total == 0:
            self._create_btn.pack(side=tk.LEFT, after=self._sign_in_btn)
        else:
            self._create_btn.pack_forget()

    def _on_sign_in(self) -> None:
        self._clear_error()
        username = self._username_var.get()
        password = self._password_var.get()

        ok, err = validate_login(username, password)
        if not ok:
            self._set_error(err or "Invalid input.")
            return

        try:
            user = verify_login(username.strip(), password)
        except (ConnectionError, OSError) as exc:
            self._set_error(f"Could not sign in: {exc}")
            return

        if not user:
            self._set_error("Invalid username or password.")
            return

        self._on_login_success(user)

    def _open_create_account_dialog(self) -> None:
        if count_users() != 0:
            messagebox.showinfo(
                "Create Account",
                "Only a manager can create new accounts after the first user exists. "
                "Sign in as a manager to use that feature in the full app.",
            )
            return

        dialog = tk.Toplevel(self)
        dialog.title("Create first account")
        dialog.configure(bg=BACKGROUND_COLOR)
        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()
        dialog.resizable(False, False)

        pad = tk.Frame(dialog, bg=BACKGROUND_COLOR, padx=28, pady=24)
        pad.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            pad,
            text="Create your first user",
            font=FONT_HEADING,
            fg=PRIMARY_COLOR,
            bg=BACKGROUND_COLOR,
        ).pack(anchor="w", pady=(0, 12))

        err_var = tk.StringVar()

        def row(label: str, show: str | None = None) -> tk.Entry:
            tk.Label(pad, text=label, font=FONT_BODY, fg=PRIMARY_COLOR, bg=BACKGROUND_COLOR).pack(
                anchor="w", pady=(10, 4)
            )
            ent = tk.Entry(
                pad,
                show=show,
                width=36,
                font=FONT_BODY,
                fg=PRIMARY_COLOR,
                bg="#FFFFFF",
                relief=tk.FLAT,
                highlightthickness=1,
                highlightbackground="#CCCCCC",
            )
            ent.pack(anchor="w")
            return ent

        u_ent = row("Username")
        p_ent = row("Password", show="•")
        c_ent = row("Confirm password", show="•")

        tk.Label(pad, text="Role", font=FONT_BODY, fg=PRIMARY_COLOR, bg=BACKGROUND_COLOR).pack(
            anchor="w", pady=(10, 4)
        )
        role_var = tk.StringVar(value="manager")
        role_frame = tk.Frame(pad, bg=BACKGROUND_COLOR)
        role_frame.pack(anchor="w")
        ttk.Radiobutton(
            role_frame,
            text="Manager",
            value="manager",
            variable=role_var,
        ).pack(side=tk.LEFT, padx=(0, 16))
        ttk.Radiobutton(role_frame, text="Employee", value="employee", variable=role_var).pack(
            side=tk.LEFT
        )

        err_lbl = tk.Label(
            pad,
            textvariable=err_var,
            font=FONT_SMALL,
            fg=ALERT_COLOR,
            bg=BACKGROUND_COLOR,
            wraplength=360,
            justify="left",
        )
        err_lbl.pack(anchor="w", pady=(12, 0))

        def submit() -> None:
            err_var.set("")
            u = u_ent.get()
            p1 = p_ent.get()
            p2 = c_ent.get()
            ok, msg = validate_new_account(u, p1, p2)
            if not ok:
                err_var.set(msg or "Invalid input.")
                return
            role = role_var.get()
            if role not in ("manager", "employee"):
                err_var.set("Select a role.")
                return
            try:
                create_account(u.strip(), p1, role)
            except ValueError as exc:
                err_var.set(str(exc))
                return
            except (ConnectionError, OSError) as exc:
                err_var.set(str(exc))
                return

            messagebox.showinfo("Account created", "You can sign in with the new account.")
            dialog.destroy()
            self._refresh_username_list()
            self._update_create_account_visibility()
            self._username_var.set(u.strip())

        btns = tk.Frame(pad, bg=BACKGROUND_COLOR)
        btns.pack(pady=(20, 0))
        tk.Button(
            btns,
            text="Create",
            font=FONT_BUTTON,
            fg="#FFFFFF",
            bg=ACTION_COLOR,
            relief=tk.FLAT,
            padx=20,
            pady=8,
            command=submit,
        ).pack(side=tk.LEFT, padx=(0, 8))
        tk.Button(
            btns,
            text="Cancel",
            font=FONT_BODY,
            fg=PRIMARY_COLOR,
            bg=BACKGROUND_COLOR,
            relief=tk.FLAT,
            padx=16,
            pady=8,
            command=dialog.destroy,
        ).pack(side=tk.LEFT)

        dialog.update_idletasks()
        x = self.winfo_rootx() + (self.winfo_width() // 2) - (dialog.winfo_width() // 2)
        y = self.winfo_rooty() + (self.winfo_height() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
