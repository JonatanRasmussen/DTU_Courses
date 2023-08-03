from abc import ABC, abstractmethod
from typing import Dict, Type

class AbstractDataClass(ABC):
    def __init__(self) -> None:
        self.name = ""

class TimePeriod:
    def __init__(self, name: str) -> None:
        self.name = name

    def get_string(self):
        return self.name

class Registry:
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

class CourseContainer(ABC):
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