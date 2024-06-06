from textual.app import App, ComposeResult
from textual.widgets import Label, Input, TextArea
from textual.containers import Container
from textual import events, on
from os.path import exists
from . import config
from .command import Command
from .mouselessdatatable import MouseLessDataTable
from .argseditmodal import ArgsEditModal
import json
import math


class FakeCommand:
    def __init__(self, cmdline):
        self.cmdline = cmdline

            
class ArsenalNGGui(App):
    CSS_PATH = "arsrnalgui.tcss"
    AUTO_FOCUS = "Input"
    global_cheats = []  # all cheats
    filtered_cheats = []  # cheats after search
    input_buffer = ""
    savefile = config.savevarfile
    arg_edit_modal = None
    cmd = ""

    table = None
    input = None 

    def __init__(self, driver_class=None, css_path=None, watch_css=False, cheatsheets=None, has_prefix=False):
        super().__init__(driver_class=None, css_path=None, watch_css=False)
        self.arg_edit_modal = None
        for value in cheatsheets.values():
            self.global_cheats.append(value)
        if exists(self.savefile):
            with open(self.savefile) as f:
                self.arsenalGlobalVars = json.load(f)
        self.filtered_cheats = self.search()
        #wrapper(self.filtered_cheats_menu.run)
        #if Gui.cmd != None and Gui.cmd.cmdline[0] != '>' and has_prefix:
        #    self.prefix_cmdline_with_prefix()


    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        self.infobox = TextArea.code_editor(id="infobox", text="")
        self.cursor_blink = False
        self.infobox.cursor_blink = False
        self.infobox.read_only = True

        self.table = MouseLessDataTable(id="table")
        self.table.cursor_type = "row"
        self.table.zebra_stripes = True
        self.input = Input(id="search", placeholder="Search", type="text")
        yield self.infobox
        yield self.input
        yield Container(self.table)
        yield Label("count")


    def on_mount(self) -> None:
        win_width = self.size.width
        prompt = "> "
        max_width = win_width - len(prompt) - len("\n")
        self.col2_size = math.floor(max_width * 14 / 100)
        self.col1_size = math.floor(max_width * 8 / 100)
        self.col3_size = math.floor(max_width * 23 / 100)
        self.col4_size = math.floor(max_width * 55 / 100)
        self.compute_table()
        self.set_focus(self.input)

    def on_mouse_down(self) -> None:
        """Reset focus on input"""
        self.set_focus(self.input)

    def action_focus_previous(self):
        return

    def action_focus_next(self):
        return

    @on(Input.Changed)
    def recompute_tabe(self, event: Input.Changed):
        self.input_buffer = self.input.value
        self.table.clear(columns=True)
        self.compute_table()

    def on_key(self, event: events.Key) -> None:
        def check_cmd(cmdline: str) -> None:
            """Called when QuitScreen is dismissed."""
            if cmdline:
                self.exit(result=FakeCommand(cmdline))
            else:
                self.arg_edit_modal.cmd = None
                self.arg_edit_modal = None
 
        # https://github.com/Textualize/textual/blob/main/src/textual/keys.py
        if event.key == "down":
            r = self.table.cursor_row
            self.table.move_cursor(row=r + 1)
            self.infobox.load_text(f"{self.filtered_cheats[self.table.cursor_row].name} \n {self.filtered_cheats[self.table.cursor_row].printable_command}")
            
        elif event.key == "up":
            r = self.table.cursor_row
            self.table.move_cursor(row=r - 1)
            self.infobox.load_text(f"{self.filtered_cheats[self.table.cursor_row].name} \n {self.filtered_cheats[self.table.cursor_row].printable_command}")

        elif event.key == "pageup":
            self.table.action_page_up()
            self.infobox.load_text(f"{self.filtered_cheats[self.table.cursor_row].name} \n {self.filtered_cheats[self.table.cursor_row].printable_command}")

        elif event.key == "pagedown":
            self.table.action_page_down()
            self.infobox.load_text(f"{self.filtered_cheats[self.table.cursor_row].name} \n {self.filtered_cheats[self.table.cursor_row].printable_command}")

        elif event.key == "enter":
            self.arg_edit_modal = ArgsEditModal(self.filtered_cheats[self.table.cursor_row], self.arsenalGlobalVars)
            self.push_screen(self.arg_edit_modal, check_cmd)

        elif event.key == "escape":
            self.exit()      



    def search(self):
        """
        Return the list of cheatsheet who match the searched term
        :return: list of cheatsheet to show
        """
        return list(filter(self.match, self.global_cheats)) if self.input_buffer != "" else self.global_cheats

    def compute_table(self):
        self.filtered_cheats = self.search()
        self.table.add_column("tags", width=self.col1_size)
        self.table.add_column("title", width=self.col2_size)
        self.table.add_column("name", width=self.col3_size)
        self.table.add_column("command", width=self.col4_size)
        for i, cheat in enumerate(self.filtered_cheats):
            tags = cheat.get_tags()
            self.table.add_row(tags, cheat.str_title, cheat.name, cheat.printable_command, key=i)

    def match(self, cheat):
        """
        Function called by the iterator to verify if the cheatsheet match the entered values
        :param cheat: cheat to check
        :return: boolean
        """
        # if search begin with '>' print only internal CMD
        if self.input_buffer.startswith(">") and not cheat.command.startswith(">"):
            return False

        for value in self.input_buffer.lower().split(" "):
            is_value_excluded = False
            if value.startswith("!") and len(value) > 1:
                value = value[1:]
                is_value_excluded = True

            if (value in cheat.str_title.lower()
                    or value in cheat.name.lower()
                    or value in cheat.tags.lower()
                    or value in "".join(cheat.command_tags.values()).lower()
                    or value in cheat.command.lower()):
                if is_value_excluded:
                    return False

            elif not is_value_excluded:
                return False
        return True

    def is_main_screen_active(self):
        return self.arg_edit_modal is None