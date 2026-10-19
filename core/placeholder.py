import tkinter as tk
from tkinter import ttk

from core.base_page import BasePage


class PlaceholderPage(BasePage):

    def __init__(self, parent, title, subtitle="", hint=""):
        self.title = title
        self.subtitle = subtitle
        self._hint = hint
        super().__init__(parent)

    def build_body(self):
        box = ttk.LabelFrame(self, text=" В разработке", padding=20)
        box.pack(fill=tk.BOTH, expand=True)
        ttk.Label(
            box, text=self._hint or "Тут что-то будет",
            font=("Segoe UI", 11), foreground="#6b7280", justify=tk.CENTER,
        ).pack(expand=True)