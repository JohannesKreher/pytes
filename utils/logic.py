
from utils import ui, db_manager
from utils.config import get_password

def write_a_note():
    result = {"theme": "", "title": "", "content": ""}
    while True:
        write_app = ui.apps.write_a_note_app(result["theme"], result["title"], result["content"])
        ui.c()
        result = write_app.run()
        if not result["theme"] or not result["title"] or not result["content"]:
            continue

        db_manager.add_note(result["theme"], result["title"], result["content"])
        break

def update_a_note():
    ui.c()
    app = ui.apps.live_note_search_app()
    target_note = app.run()
    id, theme, title, content = target_note["id"], target_note["theme"], target_note["title"], target_note["content"]

    while True:
        ui.c()
        app = ui.apps.read_a_note_app(theme, title, content)
        new_theme, new_title, new_content = app.run()
        if new_theme and new_title and new_content:
            db_manager.update_a_note(id, new_theme, new_title, new_content)
            break











