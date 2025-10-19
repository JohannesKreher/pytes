
from utils import ui, db_manager

def write_a_note(password: bytes):
    result = {"theme": "", "title": "", "content": ""}
    while True:
        write_app = ui.apps.write_a_note_app(result["theme"], result["title"], result["content"])
        ui.c()
        result = write_app.run()
        if not result["theme"] or not result["title"] or not result["content"]:
            continue

        db_manager.add_note(password, result["theme"], result["title"], result["content"])
        break

def read_a_note(password: bytes):
    original = {"theme": "", "title": "", "content": ""}
    app = ui.apps.read_a_note_app("theme = test", "title, ", "asfklghaljghasdilfhglakdfjghdilfahg\nsdgasg\nadfd")
    ui.c()
    result = app.run()
    print(result)

def select_a_note(password: bytes):
    ui.c()
    app = ui.apps.live_note_search_app()
    app.run()





