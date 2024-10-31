from gi.repository import Gtk, Adw
from functions.read_ui_file import read_ui_file

@Gtk.Template(string=read_ui_file('application_window.xml'))
class ApplicationWindow(Adw.ApplicationWindow):
    __gtype_name__ = "ApplicationWindow"
