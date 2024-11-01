from gi.repository import Gtk, GObject

class Notebook(Gtk.Notebook):
    __gtype_name__ = "Notebook"

    _default_title = "new-file.txt"

    @GObject.Property(type=str)
    def default_title(self):
        return self._default_title

    @default_title.setter
    def default_title(self, value):
        self._default_title = value

    def add_text_view(self, title=None, text=''):
        page_label = Gtk.Label()
        if title:
            page_label.set_text(title)
        else:
            page_label.set_text(self.props.default_title)
        page = Gtk.TextView()
        page.get_buffer().set_text(text)
        self.append_page(page, page_label)
