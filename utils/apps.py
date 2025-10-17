
from prompt_toolkit import Application
from prompt_toolkit.layout import Layout, HSplit
from prompt_toolkit.widgets import TextArea, Button, Frame

def write_a_note_app(theme_content:str ="", title_content:str ="", content_content:str =""):

    theme = TextArea(text=theme_content, prompt="Theme: ", focus_on_click=True, height=1)
    title = TextArea(text=title_content, prompt="Title: ", focus_on_click=True, height=1)
    content = TextArea(text=content_content, prompt="Content: ", focus_on_click=True)

    submit_button = Button(
        text="Submit",
        left_symbol="<",
        right_symbol=">",
        handler=lambda: app.exit(result={
            "theme": theme.text.strip(),
            "title": title.text.strip(),
            "content": content.text.strip()
        })
    )

    write_a_note = HSplit([
        Frame(body=title),
        Frame(body=theme),
        Frame(body=content),
        submit_button,
    ])

    app = Application(layout=Layout(write_a_note), mouse_support=True)
    return app

