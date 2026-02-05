from gi.repository import Gtk

class TabLabel(Gtk.Label):
    """
    Represents tab_labels of the EditBook.
    It is responsible to add/remove the modified specifier to/from the label.
    """
    def __init__(self, label, **kwargs):
        super().__init__(label=label, **kwargs)
        # Keep a reference to the initial label
        # so we can revert it to this original state after updates.
        self._original_label = self.props.label

    def add_modified_specifier(self):
        """It is an asterisk(*)."""
        new_label_text = f"{self._original_label}*"
        self.set_label(new_label_text)

    def remove_modified_specifier(self):
        """It is an asterisk(*)."""
        new_label_text = self._original_label
        self.set_label(new_label_text)