import os.path

class File:
    def __init__(self, path=None):
        self._path = path

    @property
    def name(self):
        """
        Return the name of the file if it exists in the file system.
        Return the constant string "unsaved_file" otherwise.
        """
        return os.path.basename(self._path) if self._path else "unsaved_file"

    def exists(self):
        """Return if the file exist in the file system."""
        return self._path

    def read(self):
        """
        Read and return the file content if the file exist in the file system.
        Raise FileNotFoundError otherwise.
        """
        if self.exists():
            with open(self._path) as file:
                return file.read()
        else:
            raise FileNotFoundError

    def write(self, text):
        """
        Write given text to the file if the file is exist in the file system.
        It replaces all existing content with the new content.
        """
        if self.exists():
            with open(self._path, "w") as file:
                file.write(text)