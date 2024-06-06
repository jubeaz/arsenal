from textual.screen import ModalScreen
from textual.widgets import Input, TextArea
from textual.containers import Container
from textual import events, on

from .command import Command

class ArgsEditModal(ModalScreen[str]):
    cmd = None
    infobox = None

    def __init__(self, cheat, arsenalGlobalVars, name=None, id=None, classes=None):
        self.infobox = TextArea.code_editor(id="infobox", text="")
        self.infobox.cursor_blink = False
        self.infobox.read_only = True
        self.inputs = {}
        self.cmd = Command(cheat, arsenalGlobalVars)
              
        super().__init__(name=name, id=id, classes=classes)



    def compose(self):
        with Container():
            yield self.infobox
            for arg_name, arg_data in self.cmd.args.items():
                self.inputs[arg_name] = Input(id=arg_name, placeholder=arg_name, type="text", value=arg_data["value"])
                yield self.inputs[arg_name]
        self.infobox.load_text(self.cmd.cmdline)

    def on_click(self, event: events.Click) -> None:
        """Prevent selection of the DataTable"""
        event.prevent_default()
        event.stop()
        return

    def on_mouse_down(self, event: events.MouseDown) -> None:
        """Prevent selection of the DataTable"""
        event.prevent_default()
        event.stop()
        return

    def on_key(self, event: events.Key) -> None:
        event.stop()
        if event.key == "tab":
            self.focus_next()
        if event.key == "enter":
            for name, i in self.inputs.items():
                value = i.value if i.value is not None else ""
                self.cmd.set_arg(name, value)
            if self.cmd.build():
                self.dismiss(self.cmd.cmdline)
        elif event.key == "escape":
            self.dismiss(None)
