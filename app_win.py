from gi.repository import Gtk
from funcs.read_ui_file import read_ui_file

ui = read_ui_file("app_win.ui")

@Gtk.Template(string=ui)
class AppWin(Gtk.ApplicationWindow):
    __gtype_name__ = "AppWin"
