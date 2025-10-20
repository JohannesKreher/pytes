from utils.db_manager import get_notes_by_query

from prompt_toolkit import Application
from prompt_toolkit.enums import EditingMode
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout, HSplit, VSplit, Dimension, Window, FormattedTextControl
from prompt_toolkit.widgets import TextArea, Button, Frame, Label
from prompt_toolkit.layout.containers import ConditionalContainer
from prompt_toolkit.filters import Condition

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

def read_a_note_app(theme_content:str, title_content:str, content_content:str):
    theme, title, content = ttc_template(theme_content, title_content, content_content)

    def set_normal_mode():
        app.vi_state.input_mode = app.vi_state.input_mode.NAVIGATION #set textareas in vim-normal mode

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

def live_note_search_app():
    kb = keybinds_template()
    edit_title = VSplit([
        Label("", width=Dimension.exact(10)),         # dummy container
        Frame(body=Label(" Live Note Search"), width=Dimension.exact(20)),
    ])
# _________  dropdown menu_________
    options = ["Theme", "Title", "Content"]
    selected_index = [0]
    current_opt = [options[selected_index[0]]]
    dropdown_label = Label(text=f"Filter: [{current_opt[0]}]▼", width=Dimension.exact(20))
    dropdown_open = [False]

    def opt_lines():
        lines = []
        for i, opt in enumerate(options):
            line = "        > " if i == selected_index[0] else "         "
            lines.append(line + opt)
        return "\n".join(lines)
    def toggle_dropdown():
        dropdown_open[0] = not dropdown_open[0]
        app.invalidate()
    def select_option():
        current_opt[0] = options[selected_index[0]]
        dropdown_label.text = f"Filter: [{current_opt[0]}]▼"
        dropdown_open[0] = False
        app.invalidate()

    dropdown_window = Window(content=FormattedTextControl(text=lambda: opt_lines()), height=len(options))
    dropdown_menu = ConditionalContainer(content=dropdown_window, filter=Condition(lambda: dropdown_open[0]))

    dropdown_menu_line = VSplit([
        dropdown_menu,
    ])
#__________ search logic __________
    search_text_area = TextArea(text="",width=Dimension.exact(20))

    search_line = VSplit([
        Label("Search: [", width=Dimension.exact(9)),
        search_text_area,
        Label("]", width=Dimension.exact(10))
    ], height=1)

    result_container = HSplit([])
    def search_text(buffer):
        result_container.children.clear()
        query = search_text_area.text
        if len(query) <= 1:
            return
        opt = current_opt
        result_list = get_notes_by_query(query, opt[0])
        i=0

        for theme, title, content in result_list:
            if i+1 == current_position: position_marker = "   > "
            elif current_position == 0: position_marker = ""
            else: position_marker = "    "
            theme_label = Label(text=f"{position_marker}Theme: {theme}", width=Dimension.exact(20))              # theme, title still neet a max length
            title_label = Label(text=f"Title: {title}", width=Dimension.exact(25))
            content_label = Label(text=f"content: {content}", width=Dimension.exact(35))
            note_line = VSplit([theme_label, title_label, content_label])
            result_container.children.append(note_line)
        app.invalidate()
    search_text_area.buffer.on_text_changed += search_text

    # ________  key control / selecting the note _________
    current_position = 1

# _______ key binds____
    @kb.add("enter")
    def _(event):
        if not dropdown_open[0]:
            toggle_dropdown()
        else:
            select_option()

    @kb.add("up")
    def _(event):
        selected_index[0] = (selected_index[0] - 1) % len(options)
    @kb.add("down")
    def _(event):
        selected_index[0] = (selected_index[0] + 1) % len(options)

    # __________ root _____
    root = HSplit([
        Label("", width=Dimension.exact(10)),           # dummy container
        edit_title,
        dropdown_label,
        dropdown_menu_line,
        search_line,
        Label("", width=Dimension.exact(10)),           # dummy container
        result_container,
    ])

    app = Application(layout=Layout(root), key_bindings=kb , mouse_support=False) # temporary false
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

