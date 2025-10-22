from utils.db_manager import get_notes_by_query, delete_note
from utils.config import search_not_by_only_one_char, edit_mode

from prompt_toolkit import Application
from prompt_toolkit.enums import EditingMode
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.vi_state import InputMode
from prompt_toolkit.layout import Layout, HSplit, VSplit, Dimension, Window, FormattedTextControl
from prompt_toolkit.widgets import TextArea, Button, Frame, Label
from prompt_toolkit.layout.containers import ConditionalContainer
from prompt_toolkit.filters import Condition

if edit_mode == "EMACS":
    conf_edit_mode = EditingMode.EMACS
else: conf_edit_mode = EditingMode.VI

def write_a_note_app(theme_content:str ="", title_content:str ="", content_content:str =""):
    def get_app():
        return app

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
    #________  Layout _____
    def get_curr_edit_mode():
        if edit_mode == "EMACS":
            text = edit_mode
        else:
            text = f"VI - {app.vi_state.input_mode.name}"
        return text
    tail_line = VSplit([
        Label(text=f"Mode: {(lambda: get_curr_edit_mode())}", width=Dimension.exact(16)),
        submit_button,
    ])

    root = HSplit([
        Frame(body=theme),
        Frame(body=title),
        Frame(body=content),
        tail_line,
    ])
    kb = keybinds_template(lambda: get_app())

    app = Application(layout=Layout(root), mouse_support=True, key_bindings=kb, editing_mode=conf_edit_mode)
    return app

def edit_a_note_app(theme_content:str, title_content:str, content_content:str):
    theme, title, content = ttc_template(theme_content, title_content, content_content)
    def get_app():
        return app
    def set_normal_mode():
        app.vi_state.input_mode = app.vi_state.input_mode.NAVIGATION

    save_changes = Button(
        text="save changes",
        left_symbol="<",
        right_symbol=">",
        handler=lambda: app.exit(result={
            "theme": theme.text.strip(),
            "title": title.text.strip(),
            "content": content.text.strip()
        })
    )
    # _______ layout _____
    def get_curr_edit_mode():
        if edit_mode == "EMACS": text = edit_mode
        else: text = f"VI - {app.vi_state.input_mode.name}"
        return text
    tail_line = VSplit([
        Label(text=f"Mode: {(lambda: get_curr_edit_mode())}", width=Dimension.exact(16)),
        save_changes
    ])

    root = HSplit([Frame(body=theme),
                     Frame(body=title),
                     Frame(body=content),
                     tail_line,])

    kb = keybinds_template(lambda: get_app())
    app = Application(layout=Layout(root), mouse_support=True, key_bindings=kb, editing_mode=conf_edit_mode)
    app.pre_run_callables.append(set_normal_mode)
    return app

def live_note_search_app():
    def get_app():
        return app
    kb = keybinds_template(lambda: get_app())
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

    current_position = [-1]
    result_notes_list = []

    result_container = HSplit([])
    def search_text(buffer):
        result_container.children.clear()
        query = search_text_area.text
        if len(query) <= 1 and search_not_by_only_one_char:
            return
        opt = current_opt
        if query:
            result_list = get_notes_by_query(query, opt[0])
        else: result_list = []
        result_notes_list.clear()
        result_notes_list.append(result_list)

        for i, note in enumerate(result_list):
            mark_lines(i, note)
        app.invalidate()

    def mark_lines(i, note):
        id, theme, title, content = note
        if i == current_position[0]: position_marker = "   > "
        else: position_marker = "    "
        theme_label = Label(text=f"{position_marker}Theme: {theme}", width=Dimension.exact(20))  # theme, title still neet a max length
        title_label = Label(text=f"Title: {title}", width=Dimension.exact(25))
        content_label = Label(text=f"content: {content}", width=Dimension.exact(35))
        note_line = VSplit([theme_label, title_label, content_label])
        result_container.children.append(note_line)

    search_text_area.buffer.on_text_changed += search_text

# _______ key binds____
    @kb.add("enter")
    def _(event):
        if current_position[0] in range(0, len(result_container.children)):
            id, theme, title, content = result_notes_list[0][current_position[0]]
            app.exit(result={
                "id":id,
                "theme":theme,
                "title":title,
                "content":content,
            })
        else:
            if not dropdown_open[0]:
                toggle_dropdown()
            else:
                select_option()
    @kb.add("c-e")
    def _(event):
        app.exit()
    @kb.add("c-d")
    def _(event):
        if current_position[0] in range(0, len(result_container.children)):
            id, _, _, _ = result_notes_list[0][current_position[0]]
            del result_notes_list[0][current_position[0]]
            result_container.children.clear()
            for i, note in enumerate(result_notes_list[0]):
                mark_lines(i, note)
            app.invalidate()
            delete_note(id)
    @kb.add("up")
    def _(event):
        if dropdown_open[0]:
            selected_index[0] = (selected_index[0] - 1) % len(options)
        else:
            if len(result_container.children) == 0:
                current_position[0] = 0
            else:
                current_position[0] = (current_position[0] - 1) % (len(result_container.children)+1)
                result_container.children.clear()
                for i, note in enumerate(result_notes_list[0]):
                    mark_lines(i, note)
                app.invalidate()
    @kb.add("down")
    def _(event):
        if dropdown_open[0]:
            selected_index[0] = (selected_index[0] + 1) % len(options)
        else:
            if len(result_container.children) == 0:
                current_position[0] = 0
            else:
                current_position[0] = (current_position[0] + 1) % (len(result_container.children)+1)
                result_container.children.clear()
                for i, note in enumerate(result_notes_list[0]):
                    mark_lines(i, note)
                app.invalidate()

    # __________ root _____
    root = HSplit([
        Label("", width=Dimension.exact(10)),           # dummy container
        edit_title,
        dropdown_label,
        dropdown_menu_line,
        Label("", width=Dimension.exact(10)),           # dummy container
        search_line,
        Label("", width=Dimension.exact(10)),           # dummy container
        Label("Results:", width=Dimension.exact(10)),
        result_container,
    ])

    app = Application(layout=Layout(root), key_bindings=kb , editing_mode=EditingMode.VI) # temporary false
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

def keybinds_template(app):      # app = app returning function
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
    @kb.add("c-e")
    def _(event):
        app().exit()
    return kb

