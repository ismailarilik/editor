from gi.repository import Gtk, Adw, Gio
from notebook.notebook import Notebook

def read_ui_file(file_path):
    with open(file_path) as file:
        return file.read()

@Gtk.Template(string=read_ui_file("application_window.xml"))
class ApplicationWindow(Adw.ApplicationWindow):
    __gtype_name__ = "ApplicationWindow"

    tree_view: Gtk.TreeView = Gtk.Template.Child()
    notebook: Notebook = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_actions()

    def add_actions(self):
        self.create_action("new-file", self.on_new_file)
        self.create_action("open-file", self.on_open_file)
        self.create_action("save", self.on_save)
        self.create_action("save-as", self.on_save_as)

    def create_action(self, name, callback):
        action = Gio.SimpleAction.new(name)
        action.connect("activate", callback)
        self.add_action(action)

    def on_new_file(self, *_):
        self.notebook.add_text_view()

    def on_open_file(self, *_):
        pass

    def on_save(self, *_):
        pass

    def on_save_as(self, *_):
        pass
