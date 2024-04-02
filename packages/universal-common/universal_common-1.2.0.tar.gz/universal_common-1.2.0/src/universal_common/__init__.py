from __future__ import annotations

from typing import Any, Callable, Iterable, Optional

def coalesce(*arguments: Any) -> Any:
    """Returns the first value in the argument list that is not null."""
    for argument in arguments:
        if argument is not None:
            return argument
        
    return None

def first(self: Iterable, predicate: Callable[[Any], bool] = None) -> Any:
    """Returns the first element in an iterable."""
    return next((x for x in self if predicate is None or predicate(x)))

def first_or_default(self: Iterable, predicate: Callable[[Any], bool] = None) -> Optional[Any]:
    """Returns the first element in an iterable or a default value."""
    return next((x for x in self if predicate is None or predicate(x)), None)

def last(self: Iterable, predicate: Callable[[Any], bool] = None) -> Any:
    """Returns the last element in an iterable."""
    return next(reversed((x for x in self if predicate is None or predicate(x))))

def last_or_default(self: Iterable, predicate: Callable[[Any], bool] = None) -> Optional[Any]:
    """Returns the last element in an iterable or a default value."""
    return next(reversed((x for x in self if predicate is None or predicate(x))), None)

class Dictionary(dict):
    """A dictionary built for a dynamic language which allows access to items either by attributes or items."""
    def __init__(self, *args, **kwargs):
        super(Dictionary, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.items():
                    self[k] = v

        if kwargs:
            for k, v in kwargs.items():
                self[k] = v

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(Dictionary, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(Dictionary, self).__delitem__(key)
        del self.__dict__[key]

class List(list):
    """A list subclass that is mutable."""
    def __init__(self, *args, **kwargs):
        super(List, self).__init__(*args, **kwargs)

class SqlConnectionStringBuilder:
    """A connection string builder for SQL connections."""
    dictionary: Dictionary

    def __init__(self: SqlConnectionStringBuilder):
        self.dictionary = Dictionary()

    @property
    def driver(self: SqlConnectionStringBuilder) -> str:
        return self.get("Driver")
    
    @driver.setter
    def driver(self: SqlConnectionStringBuilder, value: str) -> None:
        self.set("Driver", value)

    @property
    def server(self: SqlConnectionStringBuilder) -> str:
        return self.get("Server")
    
    @server.setter
    def server(self: SqlConnectionStringBuilder, value: str) -> None:
        self.set("Server", value)

    @property
    def database(self: SqlConnectionStringBuilder) -> str:
        return self.get("Database")
    
    @database.setter
    def database(self: SqlConnectionStringBuilder, value: str) -> None:
        self.set("Database", value)

    @property
    def user_id(self: SqlConnectionStringBuilder) -> str:
        return self.get("Uid")
    
    @user_id.setter
    def user_id(self: SqlConnectionStringBuilder, value: str) -> None:
        self.set("Uid", value)

    @property
    def password(self: SqlConnectionStringBuilder) -> str:
        return self.get("Pwd")
    
    @password.setter
    def password(self: SqlConnectionStringBuilder, value: str) -> None:
        self.set("Pwd", value)

    def get(self: SqlConnectionStringBuilder, key: str) -> str:
        if key in self.dictionary:
            return self.dictionary[key]
        else:
            return None

    def set(self: SqlConnectionStringBuilder, key: str, value: str) -> None:
        if value is None:
            self.remove(key)
        else:
            self.dictionary[key] = value
    
    def remove(self: SqlConnectionStringBuilder, key: str) -> None:
        if key in self.dictionary:
            del self.dictionary[key]

    def clear(self: SqlConnectionStringBuilder):
        """Removes all keys and values from the SqlConnectionStringBuilder."""
        self.dictionary.clear()

    def __str__(self: SqlConnectionStringBuilder):
        return ";".join([f"{key}={value}" for key, value in self.dictionary.items()])

    def __repr__(self: SqlConnectionStringBuilder):
        return self.__str__()

    @staticmethod
    def parse(connection_string: str) -> SqlConnectionStringBuilder:
        """Parses the connection string and returns a new connection string builder."""
        sql_connection_string_builder: SqlConnectionStringBuilder = SqlConnectionStringBuilder()
        for keyValuePairString in connection_string.split(";"):
            parts: list[str] = keyValuePairString.split("=")
            if len(parts) < 2:
                continue
            key: str = parts[0]
            key = key.lower().title()
            value: str = parts[1]
            sql_connection_string_builder.set(key, value)

        return sql_connection_string_builder

for iterable_type in [Dictionary, List]:
    iterable_type.first = first
    iterable_type.first_or_default = first_or_default
    iterable_type.last = last
    iterable_type.last_or_default = last_or_default