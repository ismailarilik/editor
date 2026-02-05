from gi.repository import Gtk
from .edit_view import EditView
from .tab_label import TabLabel
from model.file import File

class Editbook(Gtk.Notebook):
    """
    A Gtk.Notebook implementation to keep EditViews which are modified versions of Gtk.TextView.
    Editbook doesn't keep EditViews as its children directly,
    instead it wraps them with ScrolledWindows and insert them as its children.
    """
    def __init__(self):
        super().__init__(enable_popup=True, scrollable=True)
        self.connect("map", self._on_map)
        # At least an empty EditView should exist in the beginning
        # so the user can immediately start to use the application.
        self._create_initial_edit_view()

    @property
    def _current_child(self):
        """Returns the current child which is a Gtk.ScrolledWindow or None if there isn't any."""
        current_tab_number = self.get_current_page()
        if current_tab_number != -1:
            return self.get_nth_page(current_tab_number)
        else:
            return None

    @property
    def _current_edit_view(self):
        """Returns the current EditView or None if there isn't any."""
        if self._current_child:
            return self._current_child.get_child()
        else:
            return None

    @property
    def childs(self):
        """Returns all childs (ScrolledWindows)."""
        return [page.get_child() for page in self.get_pages()]

    @property
    def edit_views(self):
        """Returns all edit views."""
        return [child.get_child() for child in self.childs]

    @property
    def modified_edit_views(self):
        """Return modified edit views."""
        return [edit_view for edit_view in self.edit_views if edit_view.is_modified()]

    def get_child_for_edit_view(self, edit_view):
        """Get child (a ScrolledWindow) for given edit view."""
        return next((child for child in self.childs if child.get_child() == edit_view))

    def _create_initial_edit_view(self):
        self._create_edit_view()

    def _create_edit_view(self, file=None):
        """
        Create and append an edit view to this notebook.
        Edit views are actually wrapped with ScrolledWindows so childs would be that type.
        Also switch to this edit view, focus on it, and make it reorderable.
        """
        if not file:
            file = File()
        scroll_layout = Gtk.ScrolledWindow()
        edit_view = EditView(file)
        edit_view.connect("modified_changed", self._on_edit_view_modified_changed)
        scroll_layout.set_child(edit_view)
        self.append_page(scroll_layout, TabLabel(label=file.name))
        self.set_current_page(-1)
        edit_view.grab_focus()
        self.set_tab_reorderable(scroll_layout, True)

    def _grab_focus_for_current_edit_view(self):
        if self._current_edit_view:
            self._current_edit_view.grab_focus()

    def _on_map(self, editbook):
        if self._current_edit_view:
            self._current_edit_view.grab_focus()

    def on_new_file(self):
        self._create_edit_view()

    def on_open_file(self, file):
        self._create_edit_view(file)

    def on_save_file(self):
        if self._current_edit_view:
            self._current_edit_view.on_save_file()

    def on_save_edit_view(self, edit_view):
        """Ask given edit view to do whatever required to save changes to file system."""
        edit_view.on_save_file()

    def on_save_file_as(self, file):
        if self._current_edit_view:
            self._current_edit_view.on_save_file_as(file)
            self.set_tab_label(self._current_child, TabLabel(label=file.name))

    def on_save_edit_view_as(self, edit_view, file):
        """Ask given edit view to do whatever required to save changes as another file."""
        edit_view.on_save_file_as(file)
        self.set_tab_label(self.get_child_for_edit_view(edit_view), TabLabel(label=file.name))

    def on_next_tab(self):
        # Switch to the next editbook tab.
        # If the current one is the last one, switch to the first tab.
        next_tab_number = self.get_current_page() + 1
        if next_tab_number >= self.get_n_pages():
            next_tab_number = 0
        self.set_current_page(next_tab_number)
        self._grab_focus_for_current_edit_view()

    def on_previous_tab(self):
        # Switch to the previous editbook tab.
        # If the current one is the first one, switch to the last tab.
        previous_tab_number = self.get_current_page() - 1
        self.set_current_page(previous_tab_number)
        self._grab_focus_for_current_edit_view()

    def on_close_current_tab(self):
        self.remove_page(self.get_current_page())
        self._grab_focus_for_current_edit_view()

    def _on_edit_view_modified_changed(self, edit_view, modified):
        tab_label = self.get_tab_label(edit_view.props.parent)
        # If the text of this edit view is modified,
        # add a modified specifier to the tab title of this edit_view
        # so the user can be notified about that it is in the modified state.
        if modified:
            tab_label.add_modified_specifier()
        # Otherwise, it means the file bound to this edit view is saved to the file system
        # so remove modified specifier from the tab title.
        else:
            tab_label.remove_modified_specifier()

    def empty(self):
        """Return if this notebook has no page."""
        return self.get_n_pages() == 0

    def is_current_edit_view_modified(self):
        """
        Return True if current edit view is modified,
        return False otherwise or there isn't any edit view in editbook.
        """
        if self._current_edit_view:
            return self._current_edit_view.is_modified()
        else:
            return False