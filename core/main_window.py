import tkinter as tk
from tkinter import ttk

from tab1_ksc_ksmg.page import KaspPage
from tab2_vulns.page import VulnPage
from tab3_settings.page import SettingsPage


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Анализ документов")
        self.root.geometry("1200x720")
        self.root.minsize(950, 600)

        self._setup_style()
        self._build_layout()
        self.show_page("kasp")

    def _setup_style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("Sidebar.TFrame", background="#1e293b")
        style.configure(
            "SidebarTitle.TLabel",
            background="#1e293b", foreground="#ffffff",
            font=("Segoe UI", 12, "bold"), padding=(16, 18, 16, 10),
        )
        style.configure(
            "SidebarItem.TButton",
            background="#1e293b", foreground="#cbd5e1",
            borderwidth=0, anchor="w", padding=(16, 10),
            font=("Segoe UI", 10),
        )
        style.map(
            "SidebarItem.TButton",
            background=[("active", "#334155"), ("pressed", "#475569")],
            foreground=[("active", "#ffffff")],
        )
        style.configure(
            "SidebarItemActive.TButton",
            background="#2563eb", foreground="#ffffff",
            borderwidth=0, anchor="w", padding=(16, 10),
            font=("Segoe UI", 10, "bold"),
        )
        style.map(
            "SidebarItemActive.TButton",
            background=[("active", "#2563eb"), ("pressed", "#1d4ed8")],
            foreground=[("active", "#ffffff")],
        )
        style.configure(
            "SidebarFooter.TLabel",
            background="#1e293b", foreground="#64748b",
            font=("Segoe UI", 9), padding=(16, 10),
        )

    def _build_layout(self):
        container = ttk.Frame(self.root)
        container.pack(fill=tk.BOTH, expand=True)

        self._build_sidebar(container)

        self.content = ttk.Frame(container)
        self.content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.pages = {}
        self._register_pages()

    def _build_sidebar(self, parent):
        sidebar = ttk.Frame(parent, style="Sidebar.TFrame", width=210)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)

        ttk.Label(
            sidebar, text="Анализ документов",
            style="SidebarTitle.TLabel",
        ).pack(fill=tk.X)

        self.menu_items = [
            ("kasp",  "KSC + KSMG"),
            ("vuln",   "Уязвимости"),
            ("settings", "Настройки"),
        ]

        self.menu_buttons = {}
        for key, label in self.menu_items:
            btn = ttk.Button(
                sidebar, text=label, style="SidebarItem.TButton",
                command=lambda k=key: self.show_page(k),
            )
            btn.pack(fill=tk.X)
            self.menu_buttons[key] = btn

    def _register_pages(self):
        self.pages["kasp"]  = KaspPage(self.content)
        self.pages["vuln"]   = VulnPage(self.content)
        self.pages["settings"]    = SettingsPage(self.content)

    def show_page(self, key):
        for page in self.pages.values():
            page.pack_forget()
        self.pages[key].pack(fill=tk.BOTH, expand=True)
        for k, btn in self.menu_buttons.items():
            btn.configure(
                style="SidebarItemActive.TButton" if k == key
                else "SidebarItem.TButton"
            )