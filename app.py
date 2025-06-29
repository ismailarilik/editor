import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gio
from app_win import AppWin

class App(Gtk.Application):
    def __init__(self):
        super().__init__()
        self.add_actions()
        self.set_accels_for_app_actions()

    def do_activate(self):
        app_win = AppWin(application=self)
        app_win.present()

    def add_actions(self):
        self.create_action("quit", self.on_quit)

    def create_action(self, name, callback):
        action = Gio.SimpleAction.new(name)
        action.connect("activate", callback)
        self.add_action(action)

    def set_accels_for_app_actions(self):
        self.set_accels_for_action("app.quit", ["<primary>q"])

    def on_quit(self, *_):
        self.quit()

if __name__ == "__main__":
    App().run()
