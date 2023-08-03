from abc import ABC, abstractmethod
from typing import Dict, Type

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


class Component(ABC):
    def __init__(self) -> None:
        self.name: Component

    @abstractmethod
    def generate_key(self) -> str:
        pass


class Leaf(Component):

    def generate_key(self) -> str:
        return ""


class Composite(Component):

    def generate_key(self) -> str:
        return ""


class Registry:
    def __init__(self) -> None:
        self.dct: Dict[str, Component] = {}

    def exists(self, key: str) -> bool:
        return key in self.dct

    def get(self, key: str) -> 'Component':
        self._raise_error_if_key_missing(key)
        return self.dct[key]

    def set_unique(self, key: str, value: 'Component') -> None:
        self._raise_error_if_key_exists(key)
        self.set_dupe(key, value)

    def set_dupe(self, key: str, value: 'Component') -> None:
        if not self.exists(key):
            self.dct[key] = value

    def _raise_error_if_key_exists(self, key: str) -> None:
        if not self.exists(key):
            raise KeyError(f"Key '{key}' doesn't exist.")

    def _raise_error_if_key_missing(self, key: str) -> None:
        if self.exists(key):
            raise KeyError(f"Key '{key}' already exists.")

class LegacyRegistry:
    def __init__(self, registry_class: Type[AbstractDataClass]) -> None:
        self.registry_class: Type[AbstractDataClass] = registry_class
        self.time_key_dct: Dict[str, Dict[str, AbstractDataClass]] = {}

    def exists(self, key: str, time: TimePeriod) -> bool:
        dct = self._get_nested_dct(time)
        return key in dct

    def get(self, key: str, time: TimePeriod) -> AbstractDataClass:
        dct = self._get_nested_dct(time)
        if not key in dct:
            raise KeyError(f"Key '{key}' doesn't exists in {self._get_class_name()}.")
        return dct[key]

    def register_unique(self, key: str, time: TimePeriod) -> None:
        data_object: AbstractDataClass = self.registry_class()
        self._set(key, time, data_object)

    def register_dupe(self, key: str, time: TimePeriod) -> None:
        data_object: AbstractDataClass = self.registry_class()
        self._set_dupe(key, time, data_object)

    def register_and_return_unique(self, key: str, time: TimePeriod) -> AbstractDataClass:
        self.register_unique(key, time)
        return self.get(key, time)

    def register_and_return_dupe(self, key: str, time: TimePeriod) -> AbstractDataClass:
        data_object: AbstractDataClass = self.registry_class()
        self._set_dupe(key, time, data_object)
        return self.get(key, time)

    def _set(self, key: str, time: TimePeriod, value: AbstractDataClass) -> None:
        if self.exists(key, time):
            raise KeyError(f"Key '{key}' already exists in {self._get_class_name()}.")
        self._set_dupe(key, time, value)

    def _set_dupe(self, key: str, time: TimePeriod, value: AbstractDataClass) -> None:
        dct = self._get_nested_dct(time)
        if not self.exists(key, time):
            dct[key] = value

    def _get_nested_dct(self, time: TimePeriod) -> Dict[str, AbstractDataClass]:
        time_key: str = time.get_string()
        if not self._time_exists(time):
            raise KeyError(f"Time '{time_key}' doesn't exists in {self._get_class_name()}.")
        return self.time_key_dct[time_key]

    def _time_exists(self, time: TimePeriod) -> bool:
        time_key: str = time.get_string()
        return time_key in self.time_key_dct

    def _get_class_name(self) -> str:
        return self.registry_class.__name__

class DataManager:
    def __init__(self) -> None:
        self.registry: Registry = Registry()

    # Cache methods
    @staticmethod
    def exists_in_external_resource(key: str) -> bool:
        pass

    @staticmethod
    def read_from_external_resource(key: str) -> str:
        pass

    @staticmethod
    def write_to_external_resource(key: str, data: str) -> None:
        pass

    # Cache methods
    @staticmethod
    def exists_in_webscrape_cache(key: str) -> bool:
        pass

    @staticmethod
    def read_from_webscrape_cache(key: str) -> str:
        pass

    @staticmethod
    def write_to_webscrape_cache(key: str, data: str) -> None:
        pass

    # Database methods
    @staticmethod
    def exists_in_local_database(key: str) -> bool:
        pass

    @staticmethod
    def read_from_local_database(key: str) -> dict[str, str]:
        pass

    @staticmethod
    def write_to_local_database(key: str, data: dict[str, str]) -> None:
        pass

    # Memory methods
    @staticmethod
    def exists_in_memory(key: str) -> bool:
        pass

    @staticmethod
    def read_from_memory(key: str) -> 'BaseDataObject':
        pass

    @staticmethod
    def write_to_memory(key: str, data: 'Component') -> None:
        pass

#School
#Year
#Course
#Term
#Teacher
#StudyLine
#Evaluation
#GradeSheet
#InfoPage