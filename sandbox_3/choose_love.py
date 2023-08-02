from abc import ABC, abstractmethod
from typing import Dict, Type

class AbstractDataClass(ABC):
    def __init__(self, name: str) -> None:
        self.name = name

class Registry:
    def __init__(self, registry_class: Type[AbstractDataClass]) -> None:
        self.registry_class: Type[AbstractDataClass] = registry_class
        self.registry_dictionary: Dict[str, AbstractDataClass] = {}

    def exists(self, key: str) -> bool:
        return key in self.registry_dictionary

    def get(self, key: str) -> AbstractDataClass:
        if not self.exists(key):
            raise KeyError(f"Key '{key}' doesn't exists in {self._get_class_name()}.")
        return self.registry_dictionary[key]

    def register_unique(self, key: str) -> None:
        data_object: AbstractDataClass = self.registry_class(key)
        self._set(key, data_object)

    def register_and_get_unique(self, key: str) -> AbstractDataClass:
        self.register_unique(key)
        return self.get(key)

    def register_dupe(self, key: str) -> None:
        data_object: AbstractDataClass = self.registry_class(key)
        self._set_dupe(key, data_object)

    def register_and_get_dupe(self, key: str) -> AbstractDataClass:
        data_object: AbstractDataClass = self.registry_class(key)
        self._set_dupe(key, data_object)
        return self.get(key)

    def _set(self, key: str, value: AbstractDataClass) -> None:
        if self.exists(key):
            raise KeyError(f"Key '{key}' already exists in {self._get_class_name()}.")
        self.registry_dictionary[key] = value

    def _set_dupe(self, key: str, value: AbstractDataClass) -> None:
        if not self.exists(key):
            self.registry_dictionary[key] = value

    def _get_class_name(self) -> str:
        return self.__class__.__name__

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