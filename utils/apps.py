from utils.db_manager import get_notes_by_query, delete_note
from utils.config import search_not_by_only_one_char, edit_mode, marker

from prompt_toolkit import Application
from prompt_toolkit.enums import EditingMode
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout, HSplit, VSplit, Dimension, Window, FormattedTextControl, ScrollablePane
from prompt_toolkit.widgets import TextArea, Button, Frame, Label, Checkbox
from prompt_toolkit.layout.containers import ConditionalContainer
from prompt_toolkit.filters import Condition
from os import get_terminal_size
import signal, os

if edit_mode == "EMACS":
    conf_edit_mode = EditingMode.EMACS
else: conf_edit_mode = EditingMode.VI
if len(marker) > 4: marker = ">"

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
        if edit_mode == "EMACS": text = edit_mode
        else: text = f"VI - {app.vi_state.input_mode.name}"
        return text
    curr_mode_info = VSplit([
        Label(text="Mode: ", width=Dimension.exact(6)),
        Window(content=FormattedTextControl(text=lambda: get_curr_edit_mode()), width=Dimension.exact(16))
    ])
    tail_line = VSplit([
        curr_mode_info,
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
    def set_navigation_mode():
        app.vi_state.input_mode = app.vi_state.input_mode.NAVIGATION

    save_changes = Button(
        text="save changes",
        left_symbol="<",
        right_symbol=">",
        handler=lambda: app.exit(result={
            "theme": theme.text.strip(),
            "title": title.text.strip(),
            "content": content.text.strip()
        }),
        width=16,
    )
    # _______ layout _____
    def get_curr_edit_mode():
        if edit_mode == "EMACS": text = edit_mode
        else: text = f"VI - {app.vi_state.input_mode.name}"
        return text
    curr_mode_info = VSplit([
        Label(text="Mode: ", width=Dimension.exact(6)),
        Window(content=FormattedTextControl(text=lambda: get_curr_edit_mode()), width=Dimension.exact(16))
    ])
    tail_line = VSplit([curr_mode_info, save_changes])

    root = HSplit([Frame(body=theme),
                     Frame(body=title),
                     Frame(body=content),
                     tail_line,])

    kb = keybinds_template(lambda: get_app())
    app = Application(layout=Layout(root), mouse_support=True, key_bindings=kb, editing_mode=conf_edit_mode)
    app.pre_run_callables.append(set_navigation_mode)
    return app

def live_note_search_app():
 #______ init-part ______
    def on_resize(useless, shit):
        nonlocal scroll_height
        result_container.children.clear()
        for i, note in enumerate(result_notes_list[0]):
            mark_lines(i, note)

        scroll_height = get_t_size()[1]-10 if get_t_size()[1]-10 > 0 else 0
        scrollable_result_container.height = scroll_height
        app.invalidate()
    def get_t_size():
        return get_terminal_size().columns, get_terminal_size().lines
    edit_title = VSplit([
        Label("", width=Dimension.exact(10)),         # dummy container
        Frame(body=Label(" Live Note Search"), width=Dimension.exact(20)),
    ])

    options = ["Theme", "Title", "Content"]
    selected_index = [0]
    current_opt = [options[selected_index[0]]]
    dropdown_label = Label(text=f"Filter: [{current_opt[0]}]▼", width=Dimension.exact(20))
    dropdown_open = [False]

    scroll_height = get_t_size()[1]-10
    snbn_condition = [False]
# _________  dropdown menu_________
    def opt_lines():
        lines = []
        for i, opt in enumerate(options):
            line = f"     {marker.rjust(4)} " if i == selected_index[0] else "         "
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

    dropdown_menu_line = VSplit([dropdown_menu])
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

    def mark_lines(i, note):
        id, theme, title, content = note
        if i == current_position[0]: position_marker = f"{marker.rjust(4)} "
        else: position_marker = "    "

        t_wid = get_t_size()[0] - 5
        th_wid = int(t_wid / 100 * 30)
        co_wid = int(t_wid / 100 * 38)

        th_len = th_wid - 15 # 15 = len(prompt)
        ti_len = th_wid - 11
        co_len = co_wid - 13

        s_theme, s_title, s_content = [
            (x[:l]+"..." if len(x)>l else x)
            for x, l in [(theme, th_len), (title, ti_len), (content, co_len)]
        ]

        theme_label = Label(text=f"{position_marker}Theme: {s_theme}", width=Dimension.exact(th_wid)) # 30.7692   28
        title_label = Label(text=f"Title: {s_title}", width=Dimension.exact(th_wid)) # 30.7692   28
        content_label = Label(text=f"Content: {s_content}", width=Dimension.exact(co_wid)) # 38.4615    35
        split_label = Label(text="|", width=Dimension.exact(1))
        note_line = VSplit([
            Label(text=f"{i+1}.", width=Dimension.exact(3)),
            theme_label,
            split_label,
            title_label,
            split_label,
            content_label
        ])
        result_container.children.append(note_line)
        signal.signal(signal.SIGWINCH, on_resize) # catch resize signals

    search_text_area.buffer.on_text_changed += search_text

# _______ key binds____
    kb = KeyBindings()
    @kb.add('c-c')
    def _(event):
        raise KeyboardInterrupt
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

        elif app.layout.current_window == sct_n_by_num_textarea.window:
            if sct_n_by_num_textarea.text.strip().isdigit():
                sct_n_by_num_textarea.text = sct_n_by_num_textarea.text.strip()
                for i, note in enumerate(result_notes_list[0]):
                    id, theme, title, content = note
                    print(f"id= {i+1} | text input= {sct_n_by_num_textarea.text}")
                    if str(i+1) == sct_n_by_num_textarea.text:
                        app.exit(result={
                            "id": id,
                            "theme": theme,
                            "title": title,
                            "content": content,
                        })
                sct_n_by_num_textarea.text = "NOT FOUND"
            else:
                sct_n_by_num_textarea.text = "DIGITS ONLY"

        else:
            nonlocal scroll_height
            if not dropdown_open[0]:
                scroll_height = scroll_height-len(options)
                scrollable_result_container.height = Dimension.exact(scroll_height)
                toggle_dropdown()
            else:
                select_option()
                scroll_height = scroll_height+len(options)
                scrollable_result_container.height = Dimension.exact(scroll_height)
                search_text("unnecessary")
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
    @kb.add("c-k")
    def _(event):
        scroll = scrollable_result_container
        scroll.vertical_scroll -= 1 if scroll.vertical_scroll > 0 else 0
    @kb.add("c-j")
    def _(event):
        scroll = scrollable_result_container
        scroll.vertical_scroll += 1 if not scroll.vertical_scroll + scroll_height  == len(
            result_container.children) else 0
    @kb.add("/")
    def _(event):
        nonlocal scroll_height, snbn_condition, scrollable_result_container
        if not snbn_condition[0]:
            scroll_height = scroll_height-1
            scrollable_result_container.height = Dimension.exact(scroll_height)
            snbn_condition[0] = True
            app.layout.focus(sct_n_by_num_textarea)
        else:
            snbn_condition[0] = False
            app.layout.focus_previous()

# ______________ select note by num. ___________
    sct_n_by_num_textarea = TextArea(prompt="/: ")
    sct_n_by_num_container = ConditionalContainer(content=sct_n_by_num_textarea, filter=Condition(lambda: snbn_condition[0]))
    # __________ root _____
    scrollable_result_container = ScrollablePane(result_container, height=Dimension.exact(scroll_height))
    free_line = Label("", width=Dimension.exact(10))         # dummy container
    root = HSplit([
        free_line,
        edit_title,
        dropdown_label,
        dropdown_menu_line,
        free_line,
        search_line,
        free_line,
        Label("Results:", width=Dimension.exact(10)),
        Label(text=lambda: "-"* get_t_size()[0]),
        scrollable_result_container,
        sct_n_by_num_container,
    ])

    app = Application(layout=Layout(root), key_bindings=kb, editing_mode=EditingMode.VI)
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

