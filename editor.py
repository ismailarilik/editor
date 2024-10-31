import gi
gi.require_version('Gtk', '4.0')
gi.require_version("Adw", "1")
from application import Application

class Editor:
    def __init__(self):
        self.application = Application()

    def start(self):
        self.application.run()

editor = Editor()
editor.start()
