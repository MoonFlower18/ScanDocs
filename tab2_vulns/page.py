import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from core.base_page import BasePage
from core.paths import get_template_path

from tab2_vulns.loader import read_all_text
from tab2_vulns.vulnerability_parser import parse_vulnerabilities
from tab2_vulns.case_dict import normalize_first_word
from tab2_vulns.datestamp import extract_datestamp
from tab2_vulns.report_builder import build_report


# Пути к встроенным шаблонам СНЕСТИ ОТДЕЛЬНО К СЛОВАРЯМ ВОЗМОЖНОСТЬ ВЫБОРА ПУТИ
TEMPLATE_1 = get_template_path("Report_for_departments.docx")
TEMPLATE_2 = get_template_path("Report_for_FSTEC.docx")


class VulnPage(BasePage):
    title = "Распознавание уязвимостей и выгрузка в .docx"

    def build_body(self):
        self.source_path = None
        self.found = []
        self.datestamp = ""

        src_box = ttk.LabelFrame(self, text="Документ с уязвимостями ", padding=10)
        src_box.pack(fill=tk.X, pady=(0, 10))

        ttk.Button(
            src_box, text="Загрузить .docx",
            command=self.load_source,
        ).pack(side=tk.LEFT)

        self.src_label = ttk.Label(
            src_box, text="Файл не выбран",
            foreground="#888", font=("Segoe UI", 9),
        )
        self.src_label.pack(side=tk.LEFT, padx=(10, 0))

        self.datestamp_label = ttk.Label(
            src_box, text="",
            foreground="#2563eb", font=("Segoe UI", 9, "bold"),
        )
        self.datestamp_label.pack(side=tk.LEFT, padx=(20, 0))

        res_box = ttk.LabelFrame(self, text="Найденные уязвимости ", padding=10)
        res_box.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        toolbar = ttk.Frame(res_box)
        toolbar.pack(fill=tk.X, pady=(0, 6))

        self.counter = ttk.Label(
            toolbar, text="Найдено: 0",
            foreground="#2563eb", font=("Segoe UI", 10, "bold"),
        )
        self.counter.pack(side=tk.LEFT)

        list_frame = ttk.Frame(res_box)
        list_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL)
        self.listbox = tk.Listbox(
            list_frame, yscrollcommand=scrollbar.set,
            font=("Consolas", 9), activestyle="none",
            selectbackground="#cfe8ff", selectforeground="#000",
            height=8, borderwidth=0, highlightthickness=1,
            highlightbackground="#e5e7eb",
        )
        scrollbar.config(command=self.listbox.yview)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        actions = ttk.Frame(self)
        actions.pack(fill=tk.X)

        self.copy_btn = ttk.Button(
            actions, text="Скопировать список",
            command=self.copy_list, state=tk.DISABLED,
        )
        self.copy_btn.pack(side=tk.LEFT)

        self.export1_btn = ttk.Button(
            actions, text="Экспорт (шаблон №1)",
            command=lambda: self.export_docx(1), state=tk.DISABLED,
        )
        self.export1_btn.pack(side=tk.LEFT, padx=6)

        self.export2_btn = ttk.Button(
            actions, text="Экспорт (шаблон №2)",
            command=lambda: self.export_docx(2), state=tk.DISABLED,
        )
        self.export2_btn.pack(side=tk.LEFT)

        self.status = ttk.Label(
            self, text="Готово к работе",
            foreground="#6b7280", font=("Segoe UI", 9),
        )
        self.status.pack(anchor=tk.W, pady=(10, 0))

        self._check_templates()

    def _check_templates(self):
        missing = []
        if not os.path.exists(TEMPLATE_1):
            missing.append("template_1.docx")
        if not os.path.exists(TEMPLATE_2):
            missing.append("template_2.docx")
        if missing:
            self.status.config(
                text=f"Не найдены шаблоны: {', '.join(missing)}",
                foreground="#dc2626",
            )

    def load_source(self):
        path = filedialog.askopenfilename(
            title="Выберите документ с уязвимостями",
            filetypes=[("Word documents", "*.docx"), ("Все файлы", "*.*")],
        )
        if not path:
            return

        self.source_path = path
        self.src_label.config(text=os.path.basename(path), foreground="#333")

        self.datestamp = extract_datestamp(path)
        if self.datestamp:
            self.datestamp_label.config(text=f"{self.datestamp}")
        else:
            self.datestamp_label.config(
                text="datestamp не найден в имени файла",
                foreground="#dc2626",
            )

        self._process()

    def _process(self):
        if not self.source_path:
            return
        self.status.config(text="Обработка документа...")

        try:
            texts = read_all_text(self.source_path)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось прочитать файл:\n{e}")
            return

        full_text = "\n".join(texts)
        vulns = parse_vulnerabilities(full_text)

        self.found = []
        for v in vulns:
            self.found.append({
                "bdu": v["bdu"],
                "description": normalize_first_word(v["description"]),
            })

        self._render()
        self.status.config(text=f"Найдено уязвимостей: {len(self.found)}")

    def _render(self):
        self.listbox.delete(0, tk.END)
        for v in self.found:
            self.listbox.insert(tk.END, f"{v['bdu']} — {v['description']}")
        self.counter.config(text=f"Найдено: {len(self.found)}")
        self.copy_btn.config(state=tk.NORMAL if self.found else tk.DISABLED)

        state = tk.NORMAL if self.found else tk.DISABLED
        self.export1_btn.config(state=state)
        self.export2_btn.config(state=state)

    def copy_list(self):
        if not self.found:
            return
        lines = [f"{v['bdu']} — {v['description']}" for v in self.found]
        self.clipboard_clear()
        self.clipboard_append("\n".join(lines))
        self.status.config(text="Скопировано в буфер обмена")

    def export_docx(self, number: int):
        if not self.found:
            return

        template = TEMPLATE_1 if number == 1 else TEMPLATE_2

        if not os.path.exists(template):
            messagebox.showerror(
                "Ошибка",
                f"Встроенный шаблон №{number} не найден:\n{template}",
            )
            return

        base = "report"
        if self.source_path:
            base = os.path.splitext(os.path.basename(self.source_path))[0]
        default_name = f"{base}_Итог_{number}.docx"

        path = filedialog.asksaveasfilename(
            title=f"Сохранить отчёт №{number}",
            defaultextension=".docx",
            initialfile=default_name,
            filetypes=[("Word documents", "*.docx"), ("Все файлы", "*.*")],
        )
        if not path:
            return

        try:
            build_report(template, path, self.found, self.datestamp)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось создать отчёт:\n{e}")
            return

        self.status.config(text=f"Отчёт №{number} сохранён: {os.path.basename(path)}")
        messagebox.showinfo("Готово", f"Отчёт №{number} сохранён:\n{path}")