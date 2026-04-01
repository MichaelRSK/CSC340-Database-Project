"""Manager dashboard: full navigation per Activity 3 blueprint."""

from __future__ import annotations

from typing import Any

import tkinter as tk

from store_app.ui.dashboard_frame import DashboardFrame, OnLogout

MANAGER_NAV: list[tuple[str, str]] = [
    ("dashboard", "Dashboard"),
    ("products", "Products"),
    ("categories", "Categories"),
    ("suppliers", "Suppliers"),
    ("inventory", "Inventory"),
    ("customers", "Customers"),
    ("orders", "Orders"),
    ("returns", "Returns"),
]


class ManagerDashboardFrame(DashboardFrame):
    """Sidebar with all manager routes."""

    def __init__(
        self,
        master: tk.Misc,
        *,
        user: dict[str, Any],
        on_logout: OnLogout,
    ) -> None:
        super().__init__(master, user=user, nav_items=MANAGER_NAV, on_logout=on_logout)
