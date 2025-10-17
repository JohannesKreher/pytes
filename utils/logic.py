from utils import ui


def write_note():
    theme, title, content = "", "", ""
    while True:
        ui.c()
        if theme:
            ui.full_line("_")
            print(f"Theme: {theme}")
        if title:
            ui.full_line("-")
            print(f"Title: {title}")
        if not theme: theme = ui.get_entry_screen("Theme", "_")
        if not theme: continue
        if not title: title = ui.get_entry_screen("Title", "-")
        if not title: continue
        content = ui.get_entry_screen("Content", "-")
        if not content: continue
        break

#__________ intern recourses

