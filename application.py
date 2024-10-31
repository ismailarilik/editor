from gi.repository import Adw, Gio
from application_window import ApplicationWindow

class Application(Adw.Application):
    def __init__(self):
        super().__init__()
        self.add_actions()

    def do_activate(self):
        application_window = ApplicationWindow(application=self)
        application_window.present()

    def add_actions(self):
        self.create_action("quit", self.on_quit, ["<primary>q"])

    def create_action(self, name, callback, accels=None):
        action = Gio.SimpleAction.new(name)
        action.connect("activate", callback)
        self.add_action(action)
        if accels:
            self.set_accels_for_action(f"app.{name}", accels)

    def on_quit(self, *args):
        self.quit()
