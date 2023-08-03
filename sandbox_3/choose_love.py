from abc import ABC, abstractmethod
from typing import Dict, List

class DataDomain:
    def __init__(self, name: str) -> None:
        self.name = name

class TimePeriod:
    def __init__(self, name: str) -> None:
        self.name = name

    def get_string(self) -> str:
        return self.name

class AbstractDataClass(ABC):
    def __init__(self) -> None:
        self.domain: DataDomain
        self.time: TimePeriod
        self.name = ""


class DataObject(ABC):
    def __init__(self) -> None:
        self.name: DataObject
        self.children: List[DataObject]

    def generate_key(self) -> str:
        return "key"


class EndPoint(DataObject):
    pass


class Container(DataObject):
    def __init__(self) -> None:
        super().__init__()
        self.children: List[DataObject]

    def add(self, child: DataObject) -> None:
        self.children.append(child)

    def get_children(self) -> List[DataObject]:
        return self.children

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


class FileAccess(DAO):

    def _is_accessible(self, key: str) -> bool:
        if key == "str":
            return True
        return False

    def _read(self, key: str) -> 'DataObject':
        assert key == "hey"
        return DataObject()

    def _write(self, key: str, value: 'DataObject') -> None:
        pass

class DataManager:
    def __init__(self) -> None:
        self._data_access_objects: List[DAO] = []
        self._initialize_dao_list()

    def get(self, key: str) -> DataObject:
        daos_with_missing_key: List[DAO] = []
        for dao in self._data_access_objects:
            if dao.exists(key):
                data_object: DataObject = dao.get(key)
            else:
                daos_with_missing_key.insert(0, dao)
        for dao in daos_with_missing_key:
            dao.set_unique_key(key, data_object)
        return data_object

    def _initialize_dao_list(self) -> None:
        self._data_access_objects.append(Registry())
        self._data_access_objects.append(FileAccess())
        if self._data_access_objects[-1].exists is not True:
            raise ValueError("Data access must exist via last DAO in DAO-list")

#School
#Year
#Course
#Term
#Teacher
#StudyLine
#Evaluation
#GradeSheet
#InfoPage