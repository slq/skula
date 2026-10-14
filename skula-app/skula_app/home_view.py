"""Start screen built exclusively from the controller's cached snapshots."""
from datetime import datetime, timedelta
import re
import tkinter as tk
from tkinter import ttk

from .theme import BG, WHITE, INK, MUTED, TEAL, TEAL_PALE, DARK, LINE, ERROR_BG, ERROR_FG, Surface, wrapped_label
from .ui import SECTION_TITLES, _ordered_items, _parse_datetime, _when

DAYS = ("Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek", "Sobota", "Niedziela")
MONTHS = ("", "stycznia", "lutego", "marca", "kwietnia", "maja", "czerwca",
          "lipca", "sierpnia", "września", "października", "listopada", "grudnia")


def local_date(item):
    parsed = _parse_datetime(item.get("when"))
    if parsed is None:
        return None
    return (parsed.astimezone() if parsed.tzinfo else parsed).date()


def lesson_period(item):
    """Use the supplied end time only; do not invent lesson duration."""
    subtitle = str(item.get("subtitle") or "")
    match = re.search(r"(\d{1,2}:\d{2})\s*[–—-]\s*(\d{1,2}:\d{2})", subtitle)
    parsed = _parse_datetime(item.get("when"))
    has_time = bool(re.search(r"[T ]\d{1,2}:\d{2}", str(item.get("when") or "")))
    start = (parsed.astimezone() if parsed.tzinfo else parsed).strftime("%H:%M") if parsed and has_time else "—"
    if not match:
        return start, subtitle
    return match.group(1) + "–" + match.group(2), (subtitle[:match.start()] + subtitle[match.end():]).strip(" ·|")


def link_button(parent, title, command, *, color=WHITE, foreground=TEAL, bold=False, wrap=True):
    button = tk.Button(parent, text=title, command=command, bg=color, fg=foreground,
                       activebackground=color, activeforeground=foreground, anchor="w",
                       relief="flat", borderwidth=0, highlightthickness=1, highlightbackground=color,
                       highlightcolor=TEAL, font=("Segoe UI", 10, "bold" if bold else "normal"),
                       cursor="hand2", padx=0, pady=2, wraplength=220, justify="left")
    if wrap:
        button.bind("<Configure>", lambda e: button.configure(wraplength=max(40, e.width-8)))
    else:
        button.configure(wraplength=0)
    return button


class HomeView:
    def __init__(self, app):
        self.app = app
        self.day_offset = 0
        self.lesson_rows = []
        self.change_rows = []
        self.frame = app._scrollable_page("overview")
        top = tk.Frame(self.frame, bg=BG)
        top.pack(fill="x", pady=(0, 18))
        tabs = tk.Frame(top, bg=BG)
        tabs.pack(side="right")
        self.day_buttons = []
        for offset, text in enumerate(("Dzisiaj", "Jutro")):
            button = ttk.Button(tabs, text=text, command=lambda day=offset: self.select_day(day))
            button.pack(side="left", padx=(4, 0))
            self.day_buttons.append(button)
        greeting = tk.Frame(top, bg=BG)
        greeting.pack(side="left", fill="x", expand=True)
        tk.Label(greeting, text="Dzień dobry", bg=BG, fg=INK, font=("Segoe UI", 21, "bold"), anchor="w").pack(fill="x")
        self.date_label = tk.Label(greeting, bg=BG, fg=MUTED, font=("Segoe UI", 10), anchor="w")
        self.date_label.pack(fill="x", pady=(4, 0))

        self.welcome = Surface(self.frame)
        wrapped_label(self.welcome.body, text="Twój dziennik pod ręką", bg=WHITE, fg=INK,
                      font=("Segoe UI", 16, "bold")).pack(fill="x")
        wrapped_label(self.welcome.body, text="Połącz konto Synergia lub obejrzyj aplikację na fikcyjnych danych demo.",
                      bg=WHITE, fg=MUTED, font=("Segoe UI", 10)).pack(fill="x", pady=(6, 14))
        actions = tk.Frame(self.welcome.body, bg=WHITE)
        actions.pack(fill="x")
        ttk.Button(actions, text="Połącz konto", command=app.show_login, style="Accent.TButton").pack(side="left")
        ttk.Button(actions, text="Zobacz demo", command=lambda: app.call("demo"), style="Quiet.TButton").pack(side="left", padx=8)

        self.errors = wrapped_label(self.frame, text="", bg=ERROR_BG, fg=ERROR_FG,
                                    font=("Segoe UI", 10), padx=14, pady=12)
        self.columns = tk.Frame(self.frame, bg=BG)
        self.columns.pack(fill="x")
        self.columns.columnconfigure(0, weight=3, uniform="home")
        self.columns.columnconfigure(1, weight=2, uniform="home")
        left = tk.Frame(self.columns, bg=BG)
        left.grid(row=0, column=0, sticky="new", padx=(0, 16))
        right = tk.Frame(self.columns, bg=BG)
        right.grid(row=0, column=1, sticky="new")

        news = Surface(left, color=TEAL_PALE)
        news.pack(fill="x", pady=(0, 16))
        self.news_title = wrapped_label(news.body, text="Nowości w ostatnim odczycie", bg=TEAL_PALE, fg=TEAL,
                                        font=("Segoe UI", 12, "bold"))
        self.news_title.pack(fill="x")
        self.news_body = tk.Frame(news.body, bg=TEAL_PALE)
        self.news_body.pack(fill="x", pady=(6, 0))

        plan = Surface(left)
        plan.pack(fill="x")
        self.plan_heading = self.heading(plan.body, "Najbliżej w planie", "timetable")
        self.plan_note = wrapped_label(plan.body, bg=WHITE, fg=MUTED, font=("Segoe UI", 9))
        self.plan_note.pack(fill="x", pady=(0, 12))
        self.plan_body = tk.Frame(plan.body, bg=WHITE)
        self.plan_body.pack(fill="x")

        metrics = tk.Frame(right, bg=BG)
        metrics.pack(fill="x", pady=(0, 16))
        self.metric_values = {}
        for column, (key, title, note) in enumerate((("messages", "Wiadomości", "nieprzeczytane"),
                                                    ("schedule", "Wydarzenia", "nadchodzące"))):
            metrics.columnconfigure(column, weight=1, uniform="metric")
            card = Surface(metrics, inset=14)
            card.grid(row=0, column=column, sticky="nsew", padx=(0, 8) if column == 0 else (0, 0))
            tk.Label(card.body, image=app.icons[(key, "teal")], bg=WHITE).pack(anchor="w")
            value = tk.Label(card.body, text="—", bg=WHITE, fg=INK, font=("Segoe UI", 25, "bold"), anchor="w")
            value.pack(fill="x", pady=(3, 0))
            self.metric_values[key] = value
            link_button(card.body, title, lambda section=key: app.select_page(section), bold=True).pack(fill="x")
            wrapped_label(card.body, text=note, bg=WHITE, fg=MUTED, font=("Segoe UI", 9)).pack(fill="x")
        self.preview_lists = {}
        for key, title in (("grades", "Ostatnie oceny"), ("schedule", "Nadchodzące wydarzenia")):
            card = Surface(right)
            card.pack(fill="x", pady=(0, 16))
            self.heading(card.body, title, key)
            body = tk.Frame(card.body, bg=WHITE)
            body.pack(fill="x", pady=(8, 0))
            self.preview_lists[key] = body

    def heading(self, parent, text, section):
        row = tk.Frame(parent, bg=WHITE)
        row.pack(fill="x", pady=(0, 8))
        link_button(row, "Zobacz ›", lambda: self.app.select_page(section), wrap=False).pack(side="right", padx=(8, 0))
        label = wrapped_label(row, text=text, bg=WHITE, fg=INK, font=("Segoe UI", 12, "bold"))
        label.pack(side="left", fill="x", expand=True)
        return label

    def select_day(self, offset):
        self.day_offset = offset
        self.render()

    def item_row(self, parent, item, section, *, color=WHITE):
        row = tk.Frame(parent, bg=color)
        row.pack(fill="x", pady=5)
        link_button(row, str(item.get("title") or "Bez tytułu"),
                    lambda: self.app.show_cached_item(section, item), color=color, foreground=INK, bold=True).pack(fill="x")
        meta = " · ".join(str(p) for p in (item.get("subtitle"), _when(item.get("when"), compact=True)) if p and p != "—")
        wrapped_label(row, text=meta, bg=color, fg=MUTED, font=("Segoe UI", 9)).pack(fill="x", pady=(2, 0))
        return row

    @staticmethod
    def clear(parent):
        for child in parent.winfo_children():
            child.destroy()

    def render(self):
        state = self.app.state
        sections, updated = state.get("sections", {}), state.get("updated_at", {})
        day = datetime.now().date() + timedelta(days=self.day_offset)
        self.date_label.configure(text=f"{DAYS[day.weekday()]}, {day.day} {MONTHS[day.month]}")
        for index, button in enumerate(self.day_buttons):
            button.configure(style="Selected.TButton" if index == self.day_offset else "Pill.TButton")
        if state.get("mode") == "idle" and not any(sections.values()):
            self.welcome.pack(fill="x", pady=(0, 16), before=self.columns)
        else:
            self.welcome.pack_forget()
        errors = state.get("errors", {})
        if errors:
            names = [SECTION_TITLES.get(key, {"connection":"Połączenie", "storage":"Zapis danych"}.get(key,key)) for key in errors]
            self.errors.configure(text="Sprawdź komunikaty: " + ", ".join(names) + ". Dane mogą pochodzić z poprzedniego odczytu.")
            self.errors.pack(fill="x", pady=(0, 16), before=self.columns)
        else:
            self.errors.pack_forget()

        self.clear(self.news_body)
        changes = [(key, item) for key, items in sections.items() if key in SECTION_TITLES
                   for item in items if item.get("changed")]
        self.change_rows = []
        self.news_title.configure(text="Nowości w ostatnim odczycie" + (f" · {len(changes)}" if changes else ""))
        if not changes:
            text = "Brak nowych lub zmienionych wpisów w ostatnio pobranych danych." if updated else "Nowe i zmienione wpisy pojawią się po kolejnych odczytach."
            wrapped_label(self.news_body, text=text, bg=TEAL_PALE, fg=INK, font=("Segoe UI", 10)).pack(fill="x")
        for section, item in changes:
            self.change_rows.append(self.item_row(self.news_body, item, section, color=TEAL_PALE))

        self.clear(self.plan_body)
        lessons = [item for item in _ordered_items(list(sections.get("timetable") or []), "timetable")
                   if local_date(item) == day]
        self.lesson_rows = []
        date_note = "Dzisiaj" if self.day_offset == 0 else "Jutro"
        stamp = updated.get("timetable")
        count = len(lessons)
        noun = "lekcja" if count == 1 else "lekcje" if count % 10 in (2, 3, 4) and count % 100 not in (12, 13, 14) else "lekcji"
        self.plan_note.configure(text=f"{date_note} · cały plan dnia · {count} {noun}" +
                                 (f"\nOdczyt: {_when(stamp)}" if stamp else ""))
        if not lessons:
            text = f"Brak lekcji w pobranym planie na {'dzisiaj' if self.day_offset == 0 else 'jutro'}." if stamp else self.app.empty_text("timetable")
            wrapped_label(self.plan_body, text=text, bg=WHITE, fg=MUTED, font=("Segoe UI", 10)).pack(fill="x", pady=12)
        now = datetime.now().astimezone()
        upcoming = next((item for item in lessons if (parsed := _parse_datetime(item.get("when"))) is not None
                         and parsed.astimezone() >= now), None)
        for index, item in enumerate(lessons):
            active = item is upcoming
            color = DARK if active else WHITE
            surface = Surface(self.plan_body, color=color, inset=10)
            surface.pack(fill="x", pady=(0, 6))
            self.lesson_rows.append(surface)
            period, info = lesson_period(item)
            time_box = tk.Frame(surface.body, bg=color)
            time_box.pack(side="left", anchor="n", padx=(0, 14))
            tk.Label(time_box, text=period.replace("–", "\n"), bg=color, fg=WHITE if active else TEAL,
                     font=("Segoe UI", 10, "bold"), anchor="w", justify="left").pack(anchor="w")
            detail = tk.Frame(surface.body, bg=color)
            detail.pack(side="left", fill="x", expand=True)
            link_button(detail, str(item.get("title") or "Lekcja"),
                        lambda value=item: self.app.show_cached_item("timetable", value),
                        color=color, foreground=WHITE if active else INK, bold=True).pack(fill="x")
            wrapped_label(detail, text=info or f"Lekcja {index+1}", bg=color,
                          fg="#c5ddd8" if active else MUTED, font=("Segoe UI", 9)).pack(fill="x", pady=(3, 0))
        upcoming_events = self.app._upcoming()
        for key, value in (("messages", sum(bool(i.get("unread")) for i in sections.get("messages", []))),
                           ("schedule", len(upcoming_events))):
            self.metric_values[key].configure(text=str(value) if updated.get(key) or sections.get(key) else "—")
        for key, body in self.preview_lists.items():
            self.clear(body)
            items = upcoming_events if key == "schedule" else _ordered_items(list(sections.get(key) or []), key)
            if not items:
                text = "Brak nadchodzących wydarzeń w pobranych danych." if key == "schedule" and updated.get(key) else self.app.empty_text(key)
                wrapped_label(body, text=text, bg=WHITE, fg=MUTED, font=("Segoe UI", 10)).pack(fill="x", pady=8)
            for index, item in enumerate(items[:4]):
                if index:
                    tk.Frame(body, bg=LINE, height=1).pack(fill="x", pady=6)
                self.item_row(body, item, key)
