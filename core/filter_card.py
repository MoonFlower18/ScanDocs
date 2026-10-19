import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


class FilterCard(ttk.LabelFrame):

    def __init__(self, parent, title):
        super().__init__(parent, text=f" {title} ", padding=8)
        self.items = []

        top = ttk.Frame(self)
        top.pack(fill=tk.X, pady=(0, 6))

        self.counter = ttk.Label(
            top, text="0",
            foreground="#2563eb", font=("Segoe UI", 12, "bold"),
        )
        self.counter.pack(side=tk.LEFT)

        ttk.Label(
            top, text="найдено",
            foreground="#9ca3af", font=("Segoe UI", 9),
        ).pack(side=tk.LEFT, padx=(4, 0))

        self.save_btn = ttk.Button(
            top, text="", width=3,
            command=self.save, state=tk.DISABLED,
        )
        self.save_btn.pack(side=tk.RIGHT)

        self.copy_btn = ttk.Button(
            top, text="❐", width=3,
            command=self.copy, state=tk.DISABLED,
        )
        self.copy_btn.pack(side=tk.RIGHT, padx=(0, 4))

        list_frame = ttk.Frame(self)
        list_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL)
        self.listbox = tk.Listbox(
            list_frame, yscrollcommand=scrollbar.set,
            font=("Consolas", 9), activestyle="none",
            selectbackground="#cfe8ff", selectforeground="#000",
            height=6, borderwidth=0, highlightthickness=1,
            highlightbackground="#e5e7eb",
        )
        scrollbar.config(command=self.listbox.yview)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox.bind("<Double-Button-1>", self._copy_selected)

    def update_items(self, items):
        self.items = items
        self.listbox.delete(0, tk.END)
        for it in items:
            self.listbox.insert(tk.END, it)
        self.counter.config(text=str(len(items)))
        state = tk.NORMAL if items else tk.DISABLED
        self.save_btn.config(state=state)
        self.copy_btn.config(state=state)

    def copy(self):
        if not self.items:
            return
        self.clipboard_clear()
        self.clipboard_append("\n".join(self.items))
        self._flash_copy_btn()

    def _copy_selected(self, _event=None):
        sel = self.listbox.curselection()
        if not sel:
            return
        self.clipboard_clear()
        self.clipboard_append(self.listbox.get(sel[0]))

    def _flash_copy_btn(self):
        original = self.copy_btn.cget("text")
        self.copy_btn.config(text="✓")
        self.after(600, lambda: self.copy_btn.config(text=original))

    def save(self):
        if not self.items:
            return
        title = self.cget("text").strip(" 🌐📎🔐✉️🛡️🌍 ")
        slug = re.sub(r'\W+', '_', title).strip("_") or "results"
        path = filedialog.asksaveasfilename(
            title="Сохранить результат",
            defaultextension=".txt",
            initialfile=f"{slug}.txt",
            filetypes=[("Текстовый файл", "*.txt"), ("Все файлы", "*.*")],
        )
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write("\n".join(self.items))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить:\n{e}")
            return
        messagebox.showinfo("Готово", f"Файл сохранён:\n{path}")