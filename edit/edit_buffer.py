from gi.repository import Gtk
from model.file import File

class EditBuffer(Gtk.TextBuffer):
    """A Gtk.TextBuffer implementation to keep the text manipulation logic for EditViews."""
    def __init__(self, file=File(), **kwargs):
        super().__init__(**kwargs)
        self._file = file
        self._open_file()

    def _open_file(self):
        try:
            file_content = self._file.read()
            self.props.text = file_content
            # Set the modified flag to False to notify the subscribers of the `modified_changed` signal.
            self.set_modified(False)
        except FileNotFoundError:
            # If a file isn't exist, there is nothing to do.
            # Just leave the new edit buffer empty.
            pass

    def on_save_file(self):
        """
        Write the text to the file if the file is exist in the file system.
        Raise FileNotFoundError otherwise.
        """
        if self._file.exists():
            self._file.write(self.props.text)
            # Set the modified flag to False to notify the subscribers of the `modified_changed` signal.
            self.set_modified(False)
        else:
            raise FileNotFoundError

    def on_save_file_as(self, file):
        # Update the file of this edit buffer with the new one.
        self._file = file
        self._file.write(self.props.text)
        # Set the modified flag to False to notify the subscribers of the `modified_changed` signal.
        self.set_modified(False)