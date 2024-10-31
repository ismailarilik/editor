from gi.repository import Gtk
from application_window import ApplicationWindow

class Application(Gtk.Application):
    def do_activate(self):
        application_window = ApplicationWindow(application=self)
        application_window.present()