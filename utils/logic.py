from utils import apps

def write_a_note():
    result = {"theme": "", "title": "", "content": ""}
    while True:
        write_app = apps.write_a_note_app(result["theme"], result["title"], result["content"])
        result = write_app.run()

        if not result["theme"] or not result["title"] or not result["content"]:
            print("fill in all fields!!!")
            continue
        print(result)



        input("Press Enter to continue...")
        break



