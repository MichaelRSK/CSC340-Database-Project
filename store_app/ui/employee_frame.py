"""Employee dashboard: limited navigation."""

from __future__ import annotations

from typing import Any

import tkinter as tk

from store_app.ui.dashboard_frame import DashboardFrame, OnLogout

EMPLOYEE_NAV: list[tuple[str, str]] = [
    ("dashboard", "Dashboard"),
    ("orders", "Orders"),
    ("inventory", "Inventory"),
]


class EmployeeDashboardFrame(DashboardFrame):
    """Sidebar with employee-only routes."""

    def __init__(
        self,
        master: tk.Misc,
        *,
        user: dict[str, Any],
        on_logout: OnLogout,
    ) -> None:
        super().__init__(master, user=user, nav_items=EMPLOYEE_NAV, on_logout=on_logout)
