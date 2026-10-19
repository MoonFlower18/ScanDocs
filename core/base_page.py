import tkinter as tk
from tkinter import ttk


class BasePage(ttk.Frame):
    title = "Страница"
    subtitle = ""

    def __init__(self, parent):
        super().__init__(parent, padding=16)
        self._build_header()
        self.build_body()

    def _build_header(self):
        header = ttk.Frame(self)
        header.pack(fill=tk.X, pady=(0, 12))
        ttk.Label(header, text=self.title,
                  font=("Segoe UI", 15, "bold")).pack(anchor=tk.W)
        if self.subtitle:
            ttk.Label(header, text=self.subtitle,
                      font=("Segoe UI", 9),
                      foreground="#6b7280").pack(anchor=tk.W, pady=(2, 0))

    def build_body(self):
        raise NotImplementedError