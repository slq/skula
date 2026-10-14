"""Date and subject views of locally cached grades."""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from .ui import BG, TEAL, TEAL_PALE, SectionView


def grade_subject(item: dict) -> str:
    """Use explicit metadata; older saved snapshots only have formatted text."""
    subject = str(item.get("subject") or "").strip()
    if subject:
        return subject
    for line in str(item.get("details") or "").splitlines():
        label, separator, value = line.partition(":")
        if separator and label.strip().casefold() == "przedmiot" and value.strip():
            return value.strip()
    title = str(item.get("title") or "").strip()
    for separator in (" — ocena opisowa", ": ", " · "):
        subject, found, _ = title.rpartition(separator)
        if found and subject.strip():
            return subject.strip()
    return "Bez przedmiotu"


class GradesView(SectionView):
    def __init__(self, app) -> None:
        self.mode = "date"
        self.subject_rows: dict[str, str] = {}
        self.collapsed_subjects: set[str] = set()
        super().__init__(app, "grades")
        modes = tk.Frame(self.frame, bg=BG)
        modes.pack(fill="x", pady=(0, 10), before=self.source_label)
        self.mode_buttons = {}
        for mode, title in (("date", "Według daty"), ("subject", "Według przedmiotów")):
            button = ttk.Button(modes, text=title, command=lambda value=mode: self.set_mode(value))
            button.pack(side="left", padx=(0, 4))
            self.mode_buttons[mode] = button
        self.tree.heading("title", text="Przedmiot / ocena")
        self.tree.heading("subtitle", text="Kategoria / nauczyciel")
        self.tree.tag_configure("subject", background=TEAL_PALE, foreground=TEAL,
                                font=("Segoe UI", 10, "bold"))

    def set_mode(self, mode: str) -> None:
        self.mode = mode
        # Each mode starts with the newest grades; header sorting remains available.
        self.sort_column = None
        self.sort_reverse = False
        self.render()
        if self.tree.selection():
            self.tree.see(self.tree.selection()[0])
        else:
            self.tree.yview_moveto(0)

    def render(self) -> None:
        for row, key in self.subject_rows.items():
            if self.tree.exists(row):
                if self.tree.item(row, "open"):
                    self.collapsed_subjects.discard(key)
                else:
                    self.collapsed_subjects.add(key)
        super().render()
        for mode, button in self.mode_buttons.items():
            button.configure(style="Selected.TButton" if mode == self.mode else "Pill.TButton")
        self.tree.column("#0", width=54 if self.mode == "subject" else 32,
                         minwidth=54 if self.mode == "subject" else 32)
        count = f"Ocen: {len(self.items_by_row)}"
        if self.mode == "subject":
            count += f" · Przedmiotów: {len(self.subject_rows)}"
        self.count_label.configure(text=count)

    def _insert_rows(self, items: list[dict], current_id: str | None, *, parent: str = "") -> str | None:
        self.subject_rows.clear()
        if self.mode == "date":
            return super()._insert_rows(items, current_id)
        groups: dict[str, tuple[str, list[dict]]] = {}
        for item in items:
            subject = grade_subject(item)
            key = subject.casefold()
            groups.setdefault(key, (subject, []))[1].append(item)
        selected_row = None
        for index, key in enumerate(sorted(groups)):
            subject, grades = groups[key]
            row = f"subject_{index}"
            self.subject_rows[row] = key
            self.tree.insert("", "end", iid=row, values=(subject, f"Ocen: {len(grades)}", ""),
                             tags=("subject",), open=key not in self.collapsed_subjects or bool(self.search_var.get().strip()))
            child = super()._insert_rows(grades, current_id, parent=row)
            if child:
                selected_row = child
        return selected_row

    def _double_click(self, event) -> None:
        if self.tree.identify_row(event.y) in self.items_by_row:
            super()._double_click(event)

    def _show_selected_dialog(self, _event=None) -> None:
        selection = self.tree.selection()
        if selection and selection[0] in self.subject_rows:
            row = selection[0]
            self.tree.item(row, open=not self.tree.item(row, "open"))
        else:
            super()._show_selected_dialog(_event)
