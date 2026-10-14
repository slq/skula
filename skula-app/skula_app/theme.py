"""Desktop theme matching Android's DesignUi. No account or network access."""
from pathlib import Path
import tkinter as tk
from tkinter import ttk

BG = "#f4f7f7"
WHITE = "#ffffff"
INK = "#17354a"
MUTED = "#687b84"
TEAL = "#087c75"
TEAL_DARK = "#096860"
TEAL_PALE = "#e3f1ed"
DARK = "#153d46"
LINE = "#e0e9e7"
SIDEBAR = WHITE
SIDEBAR_MUTED = MUTED
WARNING_BG = "#fff4dc"
WARNING_FG = "#855d13"
ERROR_BG = "#fff0ed"
ERROR_FG = "#994835"


def setup_styles(root):
    root.option_add("*Font", ("Segoe UI", 10))
    root.option_add("*TCombobox*Listbox.background", WHITE)
    root.option_add("*TCombobox*Listbox.foreground", INK)
    root.option_add("*TCombobox*Listbox.selectBackground", TEAL_PALE)
    root.option_add("*TCombobox*Listbox.selectForeground", INK)
    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("TButton", font=("Segoe UI", 10), padding=(14, 9), borderwidth=0,
                    background=WHITE, foreground=INK, focuscolor=TEAL)
    style.configure("Accent.TButton", background=TEAL, foreground=WHITE,
                    padding=(16, 10), font=("Segoe UI", 10, "bold"))
    style.map("Accent.TButton", background=[("disabled", "#cbdcd8"), ("active", TEAL_DARK)],
              foreground=[("disabled", "#657e79")])
    style.configure("Quiet.TButton", background=WHITE, foreground=INK,
                    borderwidth=1, bordercolor=LINE, lightcolor=WHITE, darkcolor=LINE, padding=(12, 8))
    style.map("Quiet.TButton", background=[("disabled", BG), ("active", TEAL_PALE)],
              foreground=[("disabled", MUTED)])
    style.configure("Pill.TButton", background=BG, foreground=MUTED, padding=(14, 8))
    style.map("Pill.TButton", background=[("active", TEAL_PALE)])
    style.configure("Selected.TButton", background=TEAL_PALE, foreground=TEAL,
                    font=("Segoe UI", 10, "bold"), padding=(14, 8))
    style.map("Selected.TButton", background=[("active", "#d3e9e2")])
    style.configure("Calendar.TButton", background=WHITE, foreground=INK, padding=(8, 4))
    style.map("Calendar.TButton", background=[("active", TEAL_PALE)], foreground=[("disabled", MUTED)])
    style.configure("Danger.TButton", background=WHITE, foreground=ERROR_FG,
                    borderwidth=1, bordercolor="#edcec7", padding=(14, 9))
    style.map("Danger.TButton", background=[("active", ERROR_BG)])
    style.configure("Panel.TEntry", fieldbackground=WHITE, foreground=INK,
                    insertcolor=INK, bordercolor=LINE, lightcolor=LINE, darkcolor=LINE, padding=8)
    style.map("Panel.TEntry", bordercolor=[("focus", TEAL)])
    style.configure("TCombobox", fieldbackground=WHITE, background=WHITE,
                    foreground=INK, bordercolor=LINE, padding=7)
    style.map("TCombobox", fieldbackground=[("readonly", WHITE)], selectbackground=[("readonly", WHITE)],
              selectforeground=[("readonly", INK)])
    style.configure("Panel.TCheckbutton", background=WHITE, foreground=INK, padding=(0, 5))
    style.map("Panel.TCheckbutton", background=[("active", WHITE)])
    style.configure("Panel.Treeview", background=WHITE, fieldbackground=WHITE, foreground=INK,
                    rowheight=42, font=("Segoe UI", 10), borderwidth=0, bordercolor=LINE, lightcolor=WHITE, darkcolor=LINE)
    style.map("Panel.Treeview", background=[("selected", TEAL_PALE)], foreground=[("selected", TEAL)])
    style.configure("Panel.Treeview.Heading", background=WHITE, foreground=MUTED,
                    font=("Segoe UI", 9, "bold"), padding=(10, 11), relief="flat")
    style.map("Panel.Treeview.Heading", background=[("active", TEAL_PALE)])
    style.configure("TScrollbar", background="#cddbd7", troughcolor=BG, borderwidth=0, arrowsize=12,
                    bordercolor=BG, lightcolor=BG, darkcolor=BG, arrowcolor=MUTED)
    style.configure("TPanedwindow", background=BG)


def load_icons(root):
    folder = Path(__file__).with_name("assets")
    names = ("overview", "schedule", "announcements", "messages", "grades", "attendance",
             "timetable", "reminders", "settings", "refresh", "account")
    icons = {(name, tone): tk.PhotoImage(master=root, file=str(folder / f"{name}-{tone}.png"))
             for name in names for tone in ("muted", "teal")}
    icons["brand"] = tk.PhotoImage(master=root, file=str(folder / "brand.png"))
    return icons


class Surface(tk.Frame):
    """Rounded background with ordinary, keyboard-accessible widgets inside."""

    def __init__(self, parent, *, color=WHITE, inset=18):
        super().__init__(parent, bg=parent.cget("bg"), borderwidth=0)
        self.canvas = tk.Canvas(self, bg=self.cget("bg"), highlightthickness=0, borderwidth=0)
        self.canvas.place(x=0, y=0, relwidth=1, relheight=1)
        self.body = tk.Frame(self, bg=color)
        self.body.pack(fill="both", expand=True, padx=inset, pady=inset)
        self.color = color
        self.bind("<Configure>", self._draw)

    def _draw(self, event):
        if event.widget is not self:
            return
        w, h, r = event.width - 1, event.height - 1, 16
        self.canvas.delete("surface")
        self.canvas.create_polygon(
            r, 0, w-r, 0, w, 0, w, r, w, h-r, w, h, w-r, h,
            r, h, 0, h, 0, h-r, 0, r, 0, 0,
            smooth=True, splinesteps=20, fill=self.color, outline=LINE if self.color == WHITE else self.color,
            tags="surface")


def wrapped_label(parent, *, margin=0, **kwargs):
    """Wrap school titles with the window instead of widening the layout."""
    label = tk.Label(parent, anchor="w", justify="left", wraplength=260, **kwargs)
    label.bind("<Configure>", lambda event: label.configure(wraplength=max(40, event.width - margin)))
    return label
