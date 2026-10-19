import os
import time
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from core.base_page import BasePage
from core.filter_card import FilterCard

from tab1_ksc_ksmg import (
    filter_urls_ips,
    filter_extensions,
    filter_bdu,
    filter_emails,
    filter_sha256,
)
from tab1_ksc_ksmg.loader import read_all_text

FILTERS = [
    ("urls_ips",   "URL и IP",          filter_urls_ips.extract),
    ("extensions", "Расширения файлов", filter_extensions.extract),
    ("bdu",        "Уязвимости BDU",    filter_bdu.extract),
    ("emails",     "E-mail",            filter_emails.extract),
    ("sha256",     "Хэши SHA-256",      filter_sha256.extract),
]

LAYOUT = [
    ("urls_ips",   0, 0, 1),
    ("extensions", 0, 1, 1),
    ("bdu",        0, 2, 1),
    ("emails",     1, 0, 1),
    ("sha256",     1, 1, 2),
]


class KaspPage(BasePage):
    title = "Извлечение данных из документа"

    def build_body(self):
        self.source_path = None

        loader = ttk.LabelFrame(self, text=" Документ ", padding=10)
        loader.pack(fill=tk.X, pady=(0, 12))

        ttk.Button(
            loader, text="Загрузить .docx",
            command=self.load_file,
        ).pack(side=tk.LEFT)

        self.reprocess_btn = ttk.Button(
            loader, text="Обработать заново",
            command=self.reprocess, state=tk.DISABLED,
        )
        self.reprocess_btn.pack(side=tk.LEFT, padx=6)

        self.file_label = ttk.Label(
            loader, text="Файл не выбран",
            foreground="#888", font=("Segoe UI", 9),
        )
        self.file_label.pack(side=tk.LEFT, padx=(10, 0))

        grid = ttk.Frame(self)
        grid.pack(fill=tk.BOTH, expand=True)

        for col in range(3):
            grid.columnconfigure(col, weight=1, uniform="card")
        for row in range(2):
            grid.rowconfigure(row, weight=1, uniform="card")

        self.cards = {}
        for key, title, _ in FILTERS:
            self.cards[key] = FilterCard(grid, title)

        for key, row, col, span in LAYOUT:
            self.cards[key].grid(
                row=row, column=col, columnspan=span,
                sticky="nsew", padx=4, pady=4,
            )

        self.status = ttk.Label(
            self, text="Готово к работе",
            foreground="#6b7280", font=("Segoe UI", 9),
        )
        self.status.pack(anchor=tk.W, pady=(8, 0))

    def load_file(self):
        path = filedialog.askopenfilename(
            title="Выберите документ Word",
            filetypes=[("Word documents", "*.docx"), ("Все файлы", "*.*")],
        )
        if not path:
            return
        self.source_path = path
        self.file_label.config(text=os.path.basename(path), foreground="#333")
        self.reprocess_btn.config(state=tk.NORMAL)
        self.process()

    def reprocess(self):
        if self.source_path:
            self.process()

    def process(self):
        if not self.source_path:
            return

        start = time.perf_counter()
        self.status.config(text="Обработка документа...")

        try:
            texts = read_all_text(self.source_path)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось прочитать файл:\n{e}")
            self.status.config(text="Ошибка чтения файла")
            return

        results = {key: [] for key, _, _ in FILTERS}
        for key, _, func in FILTERS:
            seen = set()
            for text in texts:
                for item in func(text):
                    if item not in seen:
                        seen.add(item)
                        results[key].append(item)

        for key, _, _ in FILTERS:
            self.cards[key].update_items(results[key])

        elapsed = time.perf_counter() - start
        total = sum(len(v) for v in results.values())
        self.status.config(
            text=f"Обработано за {elapsed:.2f} сек · всего найдено: {total}"
        )