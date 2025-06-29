import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk
from app_win import AppWin

class App(Gtk.Application):
    def do_activate(self):
        app_win = AppWin(application=self)
        app_win.present()

if __name__ == "__main__":
    App().run()
