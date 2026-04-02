"""Owner dashboard: full navigation plus user administration."""

from __future__ import annotations

from typing import Any

import tkinter as tk

from store_app.ui.dashboard_frame import DashboardFrame, OnLogout

OWNER_NAV: list[tuple[str, str]] = [
    ("dashboard", "Dashboard"),
    ("products", "Products"),
    ("categories", "Categories"),
    ("suppliers", "Suppliers"),
    ("inventory", "Inventory"),
    ("customers", "Customers"),
    ("orders", "Orders"),
    ("returns", "Returns"),
    ("users", "Users"),
]


class OwnerDashboardFrame(DashboardFrame):
    """Sidebar with owner-level routes."""

    def __init__(
        self,
        master: tk.Misc,
        *,
        user: dict[str, Any],
        on_logout: OnLogout,
    ) -> None:
        super().__init__(master, user=user, nav_items=OWNER_NAV, on_logout=on_logout)
