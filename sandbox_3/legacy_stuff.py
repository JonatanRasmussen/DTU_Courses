from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Type, Callable

import json
from choose_love import DataObject

class DAO(ABC):

    def exists(self, key: str) -> bool:
        return self._is_accessible(key)

    def get(self, key: str) -> 'DataObject':
        self._raise_error_if_key_missing(key)
        return self._read(key)

    def set_unique_key(self, key: str, value: 'DataObject') -> None:
        self._raise_error_if_key_exists(key)
        self._set(key, value)

    def set_if_key_missing(self, key: str, value: 'DataObject') -> None:
        if not self.exists(key):
            self._set(key, value)

    def _set(self, key: str, value: 'DataObject') -> None:
        self._write(key, value)

    def _raise_error_if_key_exists(self, key: str) -> None:
        if not self.exists(key):
            raise KeyError(f"Key '{key}' doesn't exist.")

    def _raise_error_if_key_missing(self, key: str) -> None:
        if self.exists(key):
            raise KeyError(f"Key '{key}' already exists.")

    @abstractmethod
    def _is_accessible(self, key: str) -> bool:
        pass

    @abstractmethod
    def _read(self, key: str) -> 'DataObject':
        pass

    @abstractmethod
    def _write(self, key: str, value: 'DataObject') -> None:
        pass

class Registry(DAO):
    def __init__(self) -> None:
        self.dct: Dict[str, DataObject] = {}

    def _is_accessible(self, key: str) -> bool:
        return key in self.dct

    def _read(self, key: str) -> 'DataObject':
        return self.dct[key]

    def _write(self, key: str, value: 'DataObject') -> None:
        self.dct[key] = value

class DiskAccess(DAO):

    FILE_PATH: str = "json_files/"
    FILE_NAME: str = "parsed_data"

    def __init__(self) -> None:
        self.file_path: str = f"{DiskAccess.FILE_PATH}{DiskAccess.FILE_NAME}.json"
        self.dct: Dict[str, DataObject] = {}
        self._load_data()

    def _is_accessible(self, key: str) -> bool:
        return key in self.dct

    def _read(self, key: str) -> 'DataObject':
        return self.dct[key]

    def _write(self, key: str, value: 'DataObject') -> None:
        self.dct[key] = value
        self._save_data()

    def _load_data(self) -> None:
        try:
            with open(self.file_path, 'r', encoding='utf-8') as json_file:
                self.dct = json.load(json_file)
        except FileNotFoundError:
            self.dct = {}

    def _save_data(self) -> None:
        with open(self.file_path, 'w', encoding='utf-8') as json_file:
            json.dump(self.dct, json_file, indent=4)