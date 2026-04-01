"""Base dashboard: sidebar navigation and main content area."""

from __future__ import annotations

import tkinter as tk
from collections.abc import Callable
from typing import Any

from store_app.utils.constants import (
    ACTION_COLOR,
    ALERT_COLOR,
    BACKGROUND_COLOR,
    FONT_BODY,
    FONT_BUTTON,
    PRIMARY_COLOR,
)

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

        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self._build_sidebar()
        self._content_wrap = tk.Frame(self, bg=BACKGROUND_COLOR)
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
            pady=(24, 4),
        )

        brand.pack(fill=tk.X)
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
        header = tk.Frame(self._content_wrap, bg=BACKGROUND_COLOR)
        header.grid(row=0, column=0, sticky="ew", padx=32, pady=(32, 8))
        title = tk.Label(
            header,
            textvariable=self._title_var,
            font=("Segoe UI", 20, "bold"),
            fg=PRIMARY_COLOR,
            bg=BACKGROUND_COLOR,
            anchor="w",
        )
        title.pack(anchor="w")

        body_frame = tk.Frame(self._content_wrap, bg="#FFFFFF", highlightbackground="#DDDDDD", highlightthickness=1)
        body_frame.grid(row=1, column=0, sticky="nsew", padx=32, pady=(8, 32))
        body_frame.columnconfigure(0, weight=1)
        body_frame.rowconfigure(0, weight=1)

        inner = tk.Frame(body_frame, bg="#FFFFFF", padx=28, pady=28)
        inner.grid(row=0, column=0, sticky="nsew")

        tk.Label(
            inner,
            textvariable=self._body_var,
            font=FONT_BODY,
            fg=PRIMARY_COLOR,
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
