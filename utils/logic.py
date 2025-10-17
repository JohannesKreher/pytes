from utils import ui

def write_a_note():
    result = {"theme": "", "title": "", "content": ""}
    while True:
        ui.c()
        write_app = ui.apps.write_a_note_app(result["theme"], result["title"], result["content"])
        result = write_app.run()

        if not result["theme"] or not result["title"] or not result["content"]:
            continue
        print(result)



        input("Press Enter to continue...")
        break



