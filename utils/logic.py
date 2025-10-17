from utils import ui, db_manager

def write_a_note(password: bytes):
    result = {"theme": "", "title": "", "content": ""}
    while True:
        ui.c()
        write_app = ui.apps.write_a_note_app(result["theme"], result["title"], result["content"])
        result = write_app.run()
        if not result["theme"] or not result["title"] or not result["content"]:
            continue

        db_manager.add_note(password, result["theme"], result["title"], result["content"])
        break



