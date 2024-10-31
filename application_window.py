from gi.repository import Gtk
from functions.read_ui_file import read_ui_file

@Gtk.Template(string=read_ui_file('application_window.xml'))
class ApplicationWindow(Gtk.ApplicationWindow):
    __gtype_name__ = "ApplicationWindow"
