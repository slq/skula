"""Grade grouping, cached navigation and compatibility with saved snapshots."""
import copy

import pytest

from skula_app.data import SnapshotTracker
from skula_app.grades_view import grade_subject
from test_calendar import schedule_app


@pytest.fixture
def grades_app(schedule_app):
    app, _ = schedule_app
    for pending in app.root.tk.call("after", "info"):
        app.root.after_cancel(pending)
    rows = [
        dict(id="math-old", title="Matematyka: 4", subject="Matematyka", when="2026-10-11",
             subtitle="Sprawdzian", details="Przykładowy komentarz", kind="grades"),
        dict(id="english", title="Język angielski: 5", subject="Język angielski", when="2026-10-14",
             subtitle="Odpowiedź ustna", details="", kind="grades"),
        dict(id="math-new", title="Matematyka: 5+", subject="Matematyka", when="2026-10-15",
             subtitle="Kartkówka", details="Poprawa", kind="grades", changed=True),
        dict(id="art", title="Plastyka — ocena opisowa", when="2026-10-13",
             subtitle="Praca plastyczna", details="Przedmiot: Plastyka\nOpis: Staranna praca.", kind="grades"),
        dict(id="math-undated", title="Matematyka: +", subject="matematyka", when="",
             subtitle="Aktywność", details="", kind="grades"),
    ]
    app._render_state({"sections": {"grades": rows}, "mode": "offline",
                       "updated_at": {"grades": "2026-10-15T12:00:00"}})
    app.select_page("grades")
    return app, app.views["grades"], rows


def ids(view, parent=""):
    return [view.items_by_row[row]["id"] for row in view.tree.get_children(parent)]


def subjects(view):
    return {view.tree.item(row, "values")[0]: row for row in view.tree.get_children()}


def test_date_and_subject_modes_keep_all_grades_newest_first(grades_app, monkeypatch):
    app, view, rows = grades_app
    original = copy.deepcopy(rows)
    calls = []
    monkeypatch.setattr(app, "call", lambda *args, **kwargs: calls.append(args))
    assert ids(view) == ["math-new", "english", "art", "math-old", "math-undated"]
    view.mode_buttons["subject"].invoke()
    groups = subjects(view)
    assert list(groups) == ["Język angielski", "Matematyka", "Plastyka"]
    assert all(view.tree.item(row, "open") for row in groups.values())
    assert ids(view, groups["Matematyka"]) == ["math-new", "math-old", "math-undated"]
    assert ids(view, groups["Plastyka"]) == ["art"]
    assert "Ocen: 5" in view.count_label["text"]
    assert "Przedmiotów: 3" in view.count_label["text"]
    assert view.tree.item(groups["Matematyka"], "values")[1] == "Ocen: 3"
    view.mode_buttons["date"].invoke()
    assert ids(view) == ["math-new", "english", "art", "math-old", "math-undated"]
    assert calls == []
    assert rows == original


def test_subject_search_filters_grades_and_hides_empty_groups(grades_app):
    _, view, _ = grades_app
    view.set_mode("subject")
    view.search_var.set("sprawdzian")
    groups = subjects(view)
    assert list(groups) == ["Matematyka"]
    assert ids(view, groups["Matematyka"]) == ["math-old"]
    assert "Ocen: 1" in view.count_label["text"]
    view.search_var.set("przedmiot bez wyników")
    assert not view.tree.get_children()
    assert view.empty_label.winfo_manager() == "place"
    view.search_var.set("")
    assert len(view.items_by_row) == 5


def test_grade_selection_and_cached_start_link_survive_grouping(grades_app, monkeypatch):
    app, view, rows = grades_app
    app.show_cached_item("grades", rows[0])
    view.set_mode("subject")
    assert view.selected_item["id"] == "math-old"
    assert "Przykładowy komentarz" in view.detail_text.get("1.0", "end")
    group = subjects(view)["Matematyka"]
    view.tree.item(group, open=False)
    view.render()
    assert not view.tree.item(subjects(view)["Matematyka"], "open")
    calls = []
    monkeypatch.setattr(app, "call", lambda *args, **kwargs: calls.append(args))
    app.show_cached_item("grades", rows[2])
    assert view.selected_item["id"] == "math-new"
    assert view.tree.item(subjects(view)["Matematyka"], "open")
    assert calls == []
    view.set_mode("date")
    assert view.selected_item["id"] == "math-new"


def test_group_header_is_not_a_grade_and_keyboard_can_toggle_it(grades_app, monkeypatch):
    app, view, _ = grades_app
    view.set_mode("subject")
    group = subjects(view)["Matematyka"]
    view.tree.selection_set(group)
    view._select()
    assert view.selected_item is None
    assert str(view.open_button["state"]) == "disabled"
    dialogs = []
    monkeypatch.setattr(app, "show_text", lambda *args: dialogs.append(args))
    view._show_selected_dialog()
    assert not view.tree.item(group, "open")
    view._show_selected_dialog()
    assert view.tree.item(group, "open")
    assert dialogs == []


def test_refresh_and_page_changes_keep_group_mode_and_collapsed_subjects(grades_app):
    app, view, rows = grades_app
    view.set_mode("subject")
    view.tree.item(subjects(view)["Plastyka"], open=False)
    app._render_state({"busy": True})
    assert not view.tree.item(subjects(view)["Plastyka"], "open")
    new = dict(rows[2], id="math-latest", when="2026-10-16")
    app._render_state({"busy": False, "sections": {"grades": rows + [new]}})
    assert ids(view, subjects(view)["Matematyka"])[0] == "math-latest"
    app.select_page("overview")
    app.select_page("grades")
    assert view.mode == "subject"
    assert not view.tree.item(subjects(view)["Plastyka"], "open")
    app._render_state({"errors": {"grades": "Przykładowy błąd odczytu"}})
    assert len(view.items_by_row) == 6
    assert "Przykładowy błąd" in view.error_label["text"]


@pytest.mark.parametrize("size", ["1080x720", "1280x880"])
def test_grade_modes_fit_the_window(grades_app, size):
    app, view, _ = grades_app
    app.root.geometry(size + "+20000+20000")
    app.root.deiconify()
    app.root.update()
    for mode in ("date", "subject"):
        view.mode_buttons[mode].invoke()
        app.root.update()
        for button in view.mode_buttons.values():
            assert button.winfo_ismapped()
            assert button.winfo_width() >= button.winfo_reqwidth()
            assert button.winfo_rootx() + button.winfo_width() <= app.root.winfo_rootx() + app.root.winfo_width()
        assert view.tree.winfo_height() >= 100
        assert view.tree.winfo_rootx() + view.tree.winfo_width() <= app.root.winfo_rootx() + app.root.winfo_width()


@pytest.mark.parametrize("item,expected", [
    ({"subject": "  Matematyka  ", "title": "5"}, "Matematyka"),
    ({"details": "Ocena: 5\nPrzedmiot: Wiedza o społeczeństwie\nSemestr: 1"}, "Wiedza o społeczeństwie"),
    ({"title": "Edukacja: bezpieczeństwo: 4+"}, "Edukacja: bezpieczeństwo"),
    ({"title": "Plastyka — ocena opisowa"}, "Plastyka"),
    ({"title": "Język angielski · 5"}, "Język angielski"),
    ({"title": "Nieznana ocena", "details": ""}, "Bez przedmiotu"),
])
def test_subjects_work_with_older_cached_grades(item, expected):
    assert grade_subject(item) == expected


def test_subject_metadata_survives_storage_without_false_change_notifications():
    old = dict(id="grade-1", title="Matematyka: 5", when="2026-10-14",
               details="Przedmiot: Matematyka\nOcena: 5")
    tracker = SnapshotTracker()
    tracker.apply("grades", [old])
    restored = SnapshotTracker(tracker.export())
    assert grade_subject(restored.sections["grades"][0]) == "Matematyka"
    assert restored.apply("grades", [dict(old, subject="Matematyka")]) == 0
    saved = SnapshotTracker(restored.export()).sections["grades"][0]
    assert saved["subject"] == "Matematyka"
    assert not saved["changed"]
