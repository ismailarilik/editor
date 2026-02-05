from gi.repository import Gtk, GObject
from model.file import File
from .edit_buffer import EditBuffer

class EditView(Gtk.TextView):
    """A Gtk.TextView implementation to keep the editing logic."""
    def __init__(self, file=None):
        super().__init__(monospace=True)
        if not file:
            file = File()
        self._create_buffer(file)

    @property
    def _buffer(self):
        return self.get_buffer()

    @GObject.Signal(name="modified_changed", arg_types=(bool,))
    def _on_modified_changed(self, modified):
        """A signal which is emitted after the buffer's modified flag is toggled."""
        pass

    def _create_buffer(self, file):
        buffer = EditBuffer(file)
        buffer.connect("modified_changed", self._on_buffer_modified_changed)
        self.set_buffer(buffer)
        # Place cursor to the top of the text.
        # The default is the end.
        buffer.place_cursor(buffer.get_start_iter())

    def is_modified(self):
        return self._buffer.get_modified()

    def _on_buffer_modified_changed(self, edit_buffer):
        # If the buffer's modified flag is toggled,
        # emit the custom signal "modified_changed" of this edit view
        # so subscribers can learn this and do whatever necessary.
        self.emit("modified_changed", self._buffer.get_modified())

    def on_save_file(self):
        self._buffer.on_save_file()

    def on_save_file_as(self, file):
        self._buffer.on_save_file_as(file)