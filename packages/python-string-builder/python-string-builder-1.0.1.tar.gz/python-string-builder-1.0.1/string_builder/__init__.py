"""
https://github.com/wimble3
python-string-builder library.
"""
import logging


class StringBuilder:
    """Class that allows you to change a string without creating a new object.

    For example, using StringBuilder can improve performance when connecting
    a large number of strings in a loop.
    """
    @property
    def data(self) -> list:
        """Getter for data list field."""
        return self._data

    def __init__(
            self,
            first_string: str | None = None,
            debug: bool = False
    ) -> None:
        """Initializes data list, debug level.

        If first_string param exists then appends it to builder.
        """
        self._data: list = []
        self.debug: bool = debug

        if first_string:
            self.append(first_string)

    def __str__(self) -> str:
        """Changing list representation to string."""
        return "".join(self._data)

    def append(self, string: str) -> None:
        """Appends string to data list."""
        self._data.append(string)

    def insert(self, index: int, string: str) -> None:
        """Inserts string by index to data list."""
        self._data.insert(index, string)

    def remove(self, index: int, raise_ex: bool = True):
        """Removes string by index from data list.

        Parameter raise_ex is responsible for whether to throw an exception
        in the case of IndexError or throw a warning.
        """
        try:
            del self._data[index]
        except IndexError as e:
            if raise_ex:
                raise IndexError() from e
            logging.warning(
                "String element has not been deleted: %s", e)

    def clear(self) -> None:
        """Clears data list.

        It is recommended to call each time a StringBuilder instance
        is no longer needed.
        """
        self._data = []
