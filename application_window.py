from gi.repository import Gtk, Gio, GLib, GObject
from edit.editbook import Editbook
from model.file import File

class ApplicationWindow(Gtk.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._create_child()
        self._add_actions()

    @property
    def save_file_action(self):
        return self._save_file_action

    @GObject.Signal(name="quit_confirmed")
    def _quit_confirmed(self):
        pass

    def _create_child(self):
        self._editbook = Editbook()
        self.set_child(self._editbook)

    def _add_actions(self):
        self._new_file_action = self._create_action("new_file", self._on_new_file)
        self._open_file_action = self._create_action("open_file", self._on_open_file)
        self._save_file_by_user_action = self._create_action("save_file_by_user", self._on_save_file_by_user)
        self._save_file_action = self._create_action("save_file", self._on_save_file, GLib.VariantType.new("b"))
        self._save_file_as_by_user_action = self._create_action("save_file_as_by_user", self._on_save_file_as_by_user)
        self._save_file_as_action = self._create_action("save_file_as", self._on_save_file_as, GLib.VariantType.new("b"))
        self._save_first_modified_action = self._create_action("save_first_modified", self._on_save_first_modified, GLib.VariantType.new("b"))
        self._next_editbook_tab_action = self._create_action("next_editbook_tab", self._on_next_editbook_tab)
        self._previous_editbook_tab_action = self._create_action("previous_editbook_tab", self._on_previous_editbook_tab)
        self._close_current_editbook_tab_action =  self._create_action("close_current_editbook_tab", self._on_close_current_editbook_tab)

    def _create_action(self, name, handler, parameter_type=None):
        """
        Create, add and return an action
        which is named as `name`,
        has a parameter of `parameter_type` which will be passed to handlers,
        and handled by `handler` callable.
        """
        action = Gio.SimpleAction(name=name, parameter_type=parameter_type)
        action.connect("activate", handler)
        self.add_action(action)
        return action

    def _on_new_file(self, action, _):
        self._editbook.on_new_file()

    def _on_open_file(self, action, _):
        file_dialog = Gtk.FileDialog()
        file = file_dialog.open(self, None, self._on_open_file_dialog_response)

    def _on_open_file_dialog_response(self, dialog, result):
        file = dialog.open_finish(result)
        if file:
            self._editbook.on_open_file(File(file.get_path()))

    def _on_save_file_by_user(self, action, _):
        self._save_file_action.activate(GLib.Variant.new_boolean(False))

    def _on_save_file(self, action, close_tab):
        """
        Called when the save file action was activated.
        `close_tab` argument specifies if related editbook tab should be closed after saving.
        """
        if not self._editbook.empty():
            # If on_save_file raise FileNotFoundError, that means the file is not exist in the file system.
            # Use on_save_file_as instead to save the file.
            try:
                self._editbook.on_save_file()
                if close_tab:
                    self._editbook.on_close_current_tab()
            except FileNotFoundError:
                self._save_file_as_action.activate(close_tab)

    def _on_save_file_as_by_user(self, action, _):
        self._save_file_as_action.activate(GLib.Variant.new_boolean(False))

    def _on_save_file_as(self, action, close_tab):
        """
        Called when the "save file as" action was activated.
        `close_tab` argument specifies if related editbook tab should be closed after saving.
        """
        if not self._editbook.empty():
            file_dialog = Gtk.FileDialog()
            file = file_dialog.save(self, None, self._on_save_file_dialog_response, close_tab)

    def _on_save_file_dialog_response(self, dialog, result, close_tab):
        file = dialog.save_finish(result)
        if file:
            self._editbook.on_save_file_as(File(file.get_path()))
            if close_tab:
                self._editbook.on_close_current_tab()

    def _on_save_first_modified(self, action, quit):
        """
        Saves the first edit view modified it found.
        `quit` argument specifies if application should quit if there is no modified edit view.
        """
        if self._editbook.modified_edit_views:
            first_modified_edit_view = self._editbook.modified_edit_views[0]
            # If "save" raises FileNotFoundError, that means the file is not exist in the file system.
            # Use "save as" instead to save the file.
            try:
                self._editbook.on_save_edit_view(first_modified_edit_view)
            except FileNotFoundError:
                file_dialog = Gtk.FileDialog()
                file = file_dialog.save(self, None, self._on_save_first_modified_dialog_response, first_modified_edit_view, quit)
        elif quit:
            self.emit("quit_confirmed")

    def _on_save_first_modified_dialog_response(self, dialog, result, edit_view, quit):
        """
        Saves the file of given edit view,
        then call "save_first_modified" action again to recursively save all modified files.
        """
        file = dialog.save_finish(result)
        if file:
            self._editbook.on_save_edit_view_as(edit_view, File(file.get_path()))
            self._save_first_modified_action.activate(quit)

    def _on_next_editbook_tab(self, action, _):
        self._editbook.on_next_tab()

    def _on_previous_editbook_tab(self, action, _):
        self._editbook.on_previous_tab()

    def _on_close_current_editbook_tab(self, action, _):
        """
        Callback to be called when user want to close a tab with a key press or mouse click.
        It calls related method of editbook to close the current tab if related edit view is not modified.
        Otherwise, it shows an alert dialog which asks user to save the changes before closing, close tab without saving or cancel closing.
        """
        if not self._editbook.is_current_edit_view_modified():
            self._editbook.on_close_current_tab()
        else:
            save_unsaved_changes_dialog = Gtk.AlertDialog(
                buttons=("Yes", "No", "Cancel"),
                default_button=0,
                cancel_button=2,
                message="Save unsaved changes?",
                detail="If you don't save now, they will be lost!",
                modal=True
            )
            save_unsaved_changes_dialog.choose(self, None, self._on_save_unsaved_changes_dialog_response)

    def _on_save_unsaved_changes_dialog_response(self, dialog, result):
        clicked_button_index = dialog.choose_finish(result)
        if clicked_button_index == 0:
            # Means "Yes" so save changes to file system, then close the tab.
            self._save_file_action.activate(GLib.Variant.new_boolean(True))
        elif clicked_button_index == 1:
            # Means "No" so close the tab without saving.
            self._editbook.on_close_current_tab()
        else:
            # Means "Cancel" so do nothing.
            pass

    def on_quit(self):
        """
        It emits `quit_confirmed` signal to notify subscribers (possibly application).
        Otherwise, it shows an alert dialog which asks user to save changes before quit, quit without saving or cancel quit.
        """
        if not self._editbook.modified_edit_views:
            self.emit("quit_confirmed")
        else:
            save_unsaved_changes_before_quit_dialog = Gtk.AlertDialog(
                buttons=("Yes", "No", "Cancel"),
                default_button=0,
                cancel_button=2,
                message="Save unsaved changes?",
                detail="If you don't save now, they will be lost!",
                modal=True
            )
            save_unsaved_changes_before_quit_dialog.choose(self, None, self._on_save_unsaved_changes_before_quit_dialog_response)

    def _on_save_unsaved_changes_before_quit_dialog_response(self, dialog, result):
        """
        If user cancels quit, nothing is done.
        If user chooses to save changes before quit, `save_all_before_quit` action is activated.
        If user chooses not to save changes, only `quit_confirmed` is emitted.
        """
        clicked_button_index = dialog.choose_finish(result)
        if clicked_button_index == 0:
            # Means "Yes" so save all and quit.
            # The action below recursively saves all modified edit views, then quits.
            self._save_first_modified_action.activate(GLib.Variant.new_boolean(True))
        elif clicked_button_index == 1:
            # Means "No" so return True without saving.
            self.emit("quit_confirmed")
        else:
            # Means "Cancel" so return False.
            pass