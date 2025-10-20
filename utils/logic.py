
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

def read_a_note():
    original = {"theme": "", "title": "", "content": ""}
    app = ui.apps.read_a_note_app("theme = test", "title, ", "afjghdilfahg\nsdgasg\nadfd")
    ui.c()
    result = app.run()
    print(result)

def select_a_note():
    ui.c()
    app = ui.apps.live_note_search_app()
    result = app.run()
    print(result)
    input("Press enter to continue...")





