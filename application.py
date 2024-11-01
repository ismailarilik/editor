import gi
gi.require_version("Adw", "1")
from gi.repository import Adw, Gio
from application_window import ApplicationWindow

class Application(Adw.Application):
    def __init__(self):
        super().__init__()
        self.add_actions()
        self.set_accels_for_app_actions()
        self.set_accels_for_win_actions()

    def do_activate(self):
        application_window = ApplicationWindow(application=self)
        application_window.present()

    def add_actions(self):
        self.create_action("quit", self.on_quit)

    def create_action(self, name, callback):
        action = Gio.SimpleAction.new(name)
        action.connect("activate", callback)
        self.add_action(action)

    def set_accels_for_app_actions(self):
        self.set_accels_for_action("app.quit", ["<primary>q"])

    def set_accels_for_win_actions(self):
        self.set_accels_for_action("win.new-file", ["<primary>n"])
        self.set_accels_for_action("win.open-file", ["<primary>o"])
        self.set_accels_for_action("win.save", ["<primary>s"])
        self.set_accels_for_action("win.save-as", ["<primary><shift>s"])

    def on_quit(self, *_):
        self.quit()

application = Application()
application.run()
