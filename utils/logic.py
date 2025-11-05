
from utils import ui, db_manager

def write_a_note():
    result = {"theme": "", "title": "", "content": ""}
    while True:
        write_app = ui.apps.write_a_note_app(result["theme"], result["title"], result["content"])
        ui.c()
        result = write_app.run()
        if not result: return
        if not result["theme"] or not result["title"] or not result["content"]:
            continue

        db_manager.add_note(result["theme"], result["title"], result["content"])
        break

def update_a_note():
    old_position = ([-1], "", [0])
    while True:
        ui.c()
        search_app = ui.apps.live_note_search_app(old_position)
        target_note = search_app.run()
        if not target_note: return
        id = target_note["id"]
        old_position = target_note["old_position"]

        new_note = {"theme": target_note["theme"], "title": target_note["title"], "content": target_note["content"]}

        while True:
            read_app = ui.apps.edit_a_note_app(new_note["theme"], new_note["title"], new_note["content"])
            ui.c()
            new_note = read_app.run()
            if not new_note: break
            if new_note["theme"] and new_note["title"] and new_note["content"]:
                db_manager.update_note(id, new_note["theme"], new_note["title"], new_note["content"])
                return












