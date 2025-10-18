
from prompt_toolkit import Application
from prompt_toolkit.filters import in_editing_mode
from prompt_toolkit.enums import EditingMode
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout, HSplit, VSplit
from prompt_toolkit.widgets import TextArea, Button, Frame
from prompt_toolkit.key_binding.vi_state import InputMode

def write_a_note_app(theme_content:str ="", title_content:str ="", content_content:str =""):
    theme, title, content = ttc_template(theme_content, title_content, content_content)
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
        Frame(body=theme),
        Frame(body=title),
        Frame(body=content),
        submit_button,
    ])
    kb = keybinds_template()
    app = Application(layout=Layout(write_a_note), mouse_support=True, key_bindings=kb, editing_mode=EditingMode.VI)
    return app

def read_a_note_app(theme_content:str, title_content:str, content_content:str=""):
    theme, title, content = ttc_template(theme_content, title_content, content_content)

    def set_normal_mode():
        app.vi_state.input_mode = app.vi_state.input_mode.NAVIGATION

    fin = Button(
        text="finish",
        left_symbol="<",
        right_symbol=">",
        handler=lambda: app.exit(result={
            "theme": theme.text.strip(),
            "title": title.text.strip(),
            "content": content.text.strip()
        })
    )

    layout = HSplit([Frame(body=theme, title="Theme"),
                     Frame(body=title, title="Title"),
                     Frame(body=content, title="Content"),
                     fin])

    kb = keybinds_template()
    app = Application(layout=Layout(layout), mouse_support=True, key_bindings=kb, editing_mode=EditingMode.VI)
    app.pre_run_callables.append(set_normal_mode)
    return app

#________Templates _______
def ttc_template(theme_content:str = "",
                 title_content:str = "",
                 content_content:str = "",
                 readonly = False)->tuple:

    theme = TextArea(text=theme_content, prompt=f"Theme: ", read_only=readonly, focus_on_click=True, height=1)
    title = TextArea(text=title_content, prompt=f"Title: ", read_only=readonly, focus_on_click=True, height=1)
    content = TextArea(text=content_content, prompt=f"Content: ", read_only=readonly, focus_on_click=True)
    return theme, title, content

def keybinds_template():
    kb = KeyBindings()

    @kb.add('tab')
    def _(event):
        event.app.layout.focus_next()

    @kb.add('s-tab')
    def _(event):
        event.app.layout.focus_previous()

    @kb.add('c-c')
    def _(event):
        raise KeyboardInterrupt
    return kb

