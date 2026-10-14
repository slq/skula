"""Regression checks for the new cached Start screen and native navigation."""
import tkinter as tk

import pytest

from skula_app.data import demo_sections
from skula_app.home_view import lesson_period
from test_calendar import schedule_app


def demo(app):
    for pending in app.root.tk.call("after", "info"):
        app.root.after_cancel(pending)
    app.controller.demo()
    assert app.controller.wait_idle()
    app._render_state(app.controller._state())
    app.select_page("overview")


def descendants(widget):
    for child in widget.winfo_children():
        yield child
        yield from descendants(child)


def test_start_shows_all_lessons_and_changes_and_switches_day_without_fetching(schedule_app, monkeypatch):
    app, _ = schedule_app
    demo(app)
    sections=demo_sections()
    for index in range(9):
        sections["messages"].append(dict(sections["messages"][0],id=f"changed-{index}",title=f"Nowość {index}",changed=True))
    app._render_state({"sections":sections})
    calls=[]
    monkeypatch.setattr(app,"call",lambda *a,**k:calls.append(a))
    assert len(app.home.lesson_rows)==4
    assert len(app.home.change_rows)==9
    app.home.day_buttons[1].invoke()
    assert len(app.home.lesson_rows)==1
    assert "jutro" in str(app.home.plan_note["text"]).lower()
    app.home.day_buttons[0].invoke()
    assert len(app.home.lesson_rows)==4
    assert len(app.home.change_rows)==9
    assert calls==[]


def test_cached_links_select_exact_item_without_reading_message_content(schedule_app, monkeypatch):
    app,_=schedule_app
    demo(app)
    app.select_page("messages")
    view=app.views["messages"]
    view.unread_var.set(True)
    view.search_var.set("nie pasuje")
    message=app.state["sections"]["messages"][-1]
    calls=[]
    monkeypatch.setattr(app,"call",lambda *a,**k:calls.append(a))
    app.show_cached_item("messages",message)
    assert view.selected_item["id"]==message["id"]
    assert not view.unread_var.get()
    assert str(view.read_button["state"])=="normal"
    assert calls==[]


def test_message_unread_filter_combines_with_search_without_marking_read(schedule_app, monkeypatch):
    app,_=schedule_app
    demo(app)
    app.select_page("messages")
    view=app.views["messages"]
    calls=[]
    monkeypatch.setattr(app,"call",lambda *a,**k:calls.append(a))
    view.message_filters[1].invoke()
    assert len(view.tree.get_children())==2
    view.search_var.set("muzeum")
    assert len(view.tree.get_children())==1
    view.search_var.set("materiały")
    assert not view.tree.get_children()
    view.message_filters[0].invoke()
    assert len(view.tree.get_children())==1
    assert calls==[]


def test_start_retains_plan_and_shows_error_when_refresh_failed(schedule_app):
    app,_=schedule_app
    demo(app)
    app._render_state({"mode":"offline","errors":{"timetable":"SYNTHETIC_FETCH_FAILURE"}})
    assert len(app.home.lesson_rows)==4
    assert "Plan lekcji" in str(app.home.errors["text"])
    assert "Odczyt:" in str(app.home.plan_note["text"])
    assert app.home.errors.winfo_manager()=="pack"
    app.home.day_buttons[1].invoke()
    assert len(app.home.lesson_rows)==1


def test_lesson_period_preserves_teacher_and_does_not_invent_times():
    assert lesson_period({"when":"2026-10-14T08:00:00","subtitle":"08:00–08:45 · sala 12 · Nauczyciel"}) == ("08:00–08:45","sala 12 · Nauczyciel")
    assert lesson_period({"when":"2026-10-14T08:00:00","subtitle":"Sala 12"}) == ("08:00","Sala 12")
    assert lesson_period({"when":"2026-10-14","subtitle":"Sala 12"}) == ("—","Sala 12")
    assert lesson_period({"when":"brak","subtitle":""}) == ("—","")


@pytest.mark.parametrize("size",["1080x720","1280x880"])
def test_start_scrolls_complete_long_content_and_navigation_stays_visible(schedule_app,size):
    app,_=schedule_app
    demo(app)
    app.root.update()
    sections=demo_sections()
    sections["timetable"]=[dict(sections["timetable"][0],id=f"lesson-{i}",title="Długi tytuł przedmiotu " * 6)
                           for i in range(12)]
    sections["messages"]=[dict(sections["messages"][0],id=f"message-{i}",changed=True,
                              title="Ważna wiadomość szkolna " * 8) for i in range(8)]
    app._render_state({"sections":sections})
    app.root.geometry(size+"+20000+20000")
    app.root.deiconify()
    app.root.update()
    assert len(app.home.lesson_rows)==12
    assert len(app.home.change_rows)==8
    canvas=app.scroll_canvases["overview"]
    assert canvas.yview()[1] < 1
    assert app.home.columns.winfo_width() <= canvas.winfo_width()
    canvas.yview_moveto(1)
    app.root.update()
    last=app.home.lesson_rows[-1]
    assert last.winfo_rooty()+last.winfo_height() <= canvas.winfo_rooty()+canvas.winfo_height()+2
    for button in app.nav_buttons.values():
        assert button.winfo_ismapped()
        assert button.winfo_rooty()+button.winfo_height() <= app.root.winfo_rooty()+app.root.winfo_height()
    for offset in (1,0):
        app.home.day_buttons[offset].invoke()
        app.root.update()
    assert len(app.home.lesson_rows)==12


def test_start_empty_plan_does_not_offer_invented_lessons(schedule_app):
    app,_=schedule_app
    demo(app)
    sections=demo_sections()
    sections["timetable"]=[]
    app._render_state({"sections":sections})
    assert app.home.lesson_rows==[]
    texts=" ".join(str(w.cget("text")) for w in descendants(app.home.plan_body) if isinstance(w,tk.Label))
    assert "Brak lekcji" in texts
