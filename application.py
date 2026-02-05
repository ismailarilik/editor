import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gio, GLib
from application_window import ApplicationWindow

class Application(Gtk.Application):
    def __init__(self):
        super().__init__()
        self._application_name = "Editor"
        GLib.set_application_name(self._application_name)
        self._add_actions()
        self._set_accels_for_actions()

    def do_activate(self):
        self._application_window = ApplicationWindow(application=self, title=self._application_name)
        self._application_window.connect("quit_confirmed", self._on_quit_confirmed)
        self._application_window.present()

    def _add_actions(self):
        self._quit_action = Gio.SimpleAction(name="quit")
        self._quit_action.connect("activate", self._on_quit)
        self.add_action(self._quit_action)

    def _set_accels_for_actions(self):
        self.set_accels_for_action("win.new_file", ["<Primary>n"])
        self.set_accels_for_action("win.open_file", ["<Primary>o"])
        self.set_accels_for_action("win.save_file_by_user", ["<Primary>s"])
        self.set_accels_for_action("win.save_file_as_by_user", ["<Primary><Shift>s"])
        self.set_accels_for_action("win.next_editbook_tab", ["<Primary>Tab"])
        self.set_accels_for_action("win.previous_editbook_tab", ["<Primary><Shift>Tab"])
        self.set_accels_for_action("win.close_current_editbook_tab", ["<Primary>w"])
        self.set_accels_for_action("app.quit", ["<Ctrl>q"])

    def _on_quit(self, action, _):
        self._application_window.on_quit()

    def _on_quit_confirmed(self, application_window):
        self.quit()