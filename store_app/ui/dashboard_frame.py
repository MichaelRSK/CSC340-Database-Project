"""Base dashboard: sidebar navigation and main content area."""

from __future__ import annotations

import tkinter as tk
from collections.abc import Callable
from tkinter import messagebox, ttk
from typing import Any

from store_app.auth import create_account
from store_app.utils.constants import (
    ACTION_COLOR,
    ALERT_COLOR,
    BACKGROUND_COLOR,
    FONT_BODY,
    FONT_BUTTON,
    FONT_SMALL,
    PRIMARY_COLOR,
)
from store_app.utils.validator import validate_new_account

OnLogout = Callable[[], None]

# Human-readable placeholder copy per section (extend as screens are built).
SECTION_PLACEHOLDERS: dict[str, str] = {
    "dashboard": "Overview metrics, alerts, and recent activity will appear here.",
    "products": "Product list and add/edit product flows will appear here.",
    "categories": "Category management will appear here.",
    "suppliers": "Supplier management will appear here.",
    "inventory": "Inventory levels and receive stock will appear here.",
    "customers": "Customer list and details will appear here.",
    "orders": "Orders list, new order, and payment flows will appear here.",
    "returns": "Returns logging and tracking will appear here.",
    "users": "Owner user administration and role management will appear here.",
}


class DashboardFrame(tk.Frame):
    """
    Role-specific dashboards subclass this and pass `nav_items` as (section_id, label).
    """

    def __init__(
        self,
        master: tk.Misc,
        *,
        user: dict[str, Any],
        nav_items: list[tuple[str, str]],
        on_logout: OnLogout,
    ) -> None:
        super().__init__(master, bg=BACKGROUND_COLOR)
        self._user = user
        self._nav_items = nav_items
        self._on_logout = on_logout
        self._nav_buttons: dict[str, tk.Button] = {}
        self._active_key: str | None = None
        self._role = str(user.get("role", "")).lower()

        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self._build_sidebar()
        # Slightly darker than BACKGROUND_COLOR so the white content card reads as a distinct panel.
        self._content_wrap = tk.Frame(self, bg="#E8EAED")
        self._content_wrap.grid(row=0, column=1, sticky="nsew", padx=(0, 0), pady=0)
        self._content_wrap.columnconfigure(0, weight=1)
        self._content_wrap.rowconfigure(1, weight=1)

        self._title_var = tk.StringVar()
        self._body_var = tk.StringVar()
        self._build_content_shell()

        first_key = nav_items[0][0] if nav_items else "dashboard"
        self._select_nav(first_key)

    def _build_sidebar(self) -> None:
        sidebar = tk.Frame(self, bg=PRIMARY_COLOR, width=260)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)
        sidebar.rowconfigure(1, weight=1)

        brand = tk.Label(
            sidebar,
            text="Store Manager",
            font=("Segoe UI", 16, "bold"),
            fg="#FFFFFF",
            bg=PRIMARY_COLOR,
            anchor="w",
            padx=20,
        )

        # Label's pady= must be a single value; use pack() for asymmetric vertical padding.
        brand.pack(fill=tk.X, pady=(24, 4))
        user_label = tk.Label(
            sidebar,
            text=f"Signed in as\n{self._user.get('username', '')}",
            font=("Segoe UI", 9),
            fg="#BDC3C7",
            bg=PRIMARY_COLOR,
            anchor="w",
            justify=tk.LEFT,
            padx=20,
        )
        user_label.pack(fill=tk.X, pady=(0, 16))

        nav_frame = tk.Frame(sidebar, bg=PRIMARY_COLOR)
        nav_frame.pack(fill=tk.BOTH, expand=True, padx=12)

        for key, label in self._nav_items:
            btn = tk.Button(
                nav_frame,
                text=label,
                font=FONT_BODY,
                fg="#FFFFFF",
                bg=PRIMARY_COLOR,
                activebackground=ACTION_COLOR,
                activeforeground="#FFFFFF",
                relief=tk.FLAT,
                anchor="w",
                padx=16,
                pady=10,
                cursor="hand2",
                command=lambda k=key: self._select_nav(k),
            )
            btn.pack(fill=tk.X, pady=2)
            self._nav_buttons[key] = btn

        logout_btn = tk.Button(
            sidebar,
            text="Log out",
            font=FONT_BUTTON,
            fg="#FFFFFF",
            bg="#1B2631",
            activebackground=ALERT_COLOR,
            activeforeground="#FFFFFF",
            relief=tk.FLAT,
            padx=16,
            pady=12,
            cursor="hand2",
            command=self._on_logout,
        )
        logout_btn.pack(side=tk.BOTTOM, fill=tk.X, padx=12, pady=24)

    def _build_content_shell(self) -> None:
        wrap_bg = "#E8EAED"
        header = tk.Frame(self._content_wrap, bg=wrap_bg)
        header.grid(row=0, column=0, sticky="ew", padx=32, pady=(32, 8))
        header.columnconfigure(0, weight=1)
        title = tk.Label(
            header,
            textvariable=self._title_var,
            font=("Segoe UI", 20, "bold"),
            fg=PRIMARY_COLOR,
            bg=wrap_bg,
            anchor="w",
        )
        title.grid(row=0, column=0, sticky="w")
        if self._role in {"owner", "manager"}:
            create_btn = tk.Button(
                header,
                text="Create User",
                font=FONT_BUTTON,
                fg="#FFFFFF",
                bg=ACTION_COLOR,
                activebackground=PRIMARY_COLOR,
                activeforeground="#FFFFFF",
                relief=tk.FLAT,
                padx=14,
                pady=6,
                cursor="hand2",
                command=self._open_create_user_dialog,
            )
            create_btn.grid(row=0, column=1, sticky="e")
        tk.Label(
            header,
            text="Placeholder — charts and lists are added in later milestones.",
            font=FONT_SMALL,
            fg="#5D6D7E",
            bg=wrap_bg,
            anchor="w",
        ).grid(row=1, column=0, columnspan=2, sticky="w", pady=(4, 0))

        body_frame = tk.Frame(
            self._content_wrap,
            bg="#FFFFFF",
            highlightbackground="#C5CCD3",
            highlightthickness=1,
        )
        body_frame.grid(row=1, column=0, sticky="nsew", padx=32, pady=(8, 32))
        body_frame.columnconfigure(0, weight=1)
        body_frame.rowconfigure(0, weight=1)

        inner = tk.Frame(body_frame, bg="#FFFFFF", padx=28, pady=28)
        inner.grid(row=0, column=0, sticky="nsew")

        tk.Label(
            inner,
            textvariable=self._body_var,
            font=FONT_BODY,
            fg="#34495E",
            bg="#FFFFFF",
            anchor="nw",
            justify=tk.LEFT,
            wraplength=900,
        ).pack(anchor="nw")

    def _select_nav(self, key: str) -> None:
        """Highlight nav and refresh main content."""
        self._active_key = key
        for nav_key, btn in self._nav_buttons.items():
            if nav_key == key:
                btn.configure(bg=ACTION_COLOR)
            else:
                btn.configure(bg=PRIMARY_COLOR)

        label = next((lbl for k, lbl in self._nav_items if k == key), key.title())
        self._title_var.set(label)
        self._body_var.set(SECTION_PLACEHOLDERS.get(key, "This section is coming soon."))

    def _open_create_user_dialog(self) -> None:
        """Allow owner/manager to create accounts from dashboard."""
        if self._role not in {"owner", "manager"}:
            messagebox.showerror("Create User", "You do not have permission to create users.")
            return

        dialog = tk.Toplevel(self)
        dialog.title("Create user")
        dialog.configure(bg=BACKGROUND_COLOR)
        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()
        dialog.resizable(False, False)

        pad = tk.Frame(dialog, bg=BACKGROUND_COLOR, padx=28, pady=24)
        pad.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            pad,
            text="Create account",
            font=("Segoe UI", 14, "bold"),
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
        role_var = tk.StringVar(value="employee")
        role_values = ["employee", "manager"] if self._role == "manager" else ["employee", "manager", "owner"]
        role_combo = ttk.Combobox(
            pad,
            textvariable=role_var,
            values=role_values,
            state="readonly",
            width=18,
            font=FONT_BODY,
        )
        role_combo.pack(anchor="w")
        role_combo.current(0)

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
            username = u_ent.get()
            password = p_ent.get()
            confirm = c_ent.get()
            ok, msg = validate_new_account(username, password, confirm)
            if not ok:
                err_var.set(msg or "Invalid input.")
                return

            role = role_var.get().strip().lower()
            if role not in role_values:
                err_var.set("Select a valid role.")
                return

            try:
                create_account(username.strip(), password, role)
            except ValueError as exc:
                err_var.set(str(exc))
                return
            except (ConnectionError, OSError) as exc:
                err_var.set(str(exc))
                return

            messagebox.showinfo("Account created", f"Created {role} account for '{username.strip()}'.")
            dialog.destroy()

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
