from abc import ABC, abstractmethod
from typing import Dict, List, Type


class DAO(ABC):

    def exists(self, key: str) -> bool:
        return self._is_accessible(key)

    def get(self, key: str) -> 'RootObj':
        self._raise_error_if_key_missing(key)
        return self._read(key)

    def set_unique_key(self, key: str, value: 'RootObj') -> None:
        self._raise_error_if_key_exists(key)
        self._set(key, value)

    def set_if_key_missing(self, key: str, value: 'RootObj') -> None:
        if not self.exists(key):
            self._set(key, value)

    def _set(self, key: str, value: 'RootObj') -> None:
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
    def _read(self, key: str) -> 'RootObj':
        pass

    @abstractmethod
    def _write(self, key: str, value: 'RootObj') -> None:
        pass

class Registry(DAO):
    def __init__(self) -> None:
        self.dct: Dict[str, RootObj] = {}

    def _is_accessible(self, key: str) -> bool:
        return key in self.dct

    def _read(self, key: str) -> 'RootObj':
        return self.dct[key]

    def _write(self, key: str, value: 'RootObj') -> None:
        self.dct[key] = value

class FileAccess(DAO):

    def _is_accessible(self, key: str) -> bool:
        if key == "str":
            return True
        return False

    def _read(self, key: str) -> 'RootObj':
        assert key == "hey"
        return School()

    def _write(self, key: str, value: 'RootObj') -> None:
        pass

class DataStrategy:
    pass

class StrategySwitch(ABC):

    @staticmethod
    @abstractmethod
    def school_strategy():
        pass

    @staticmethod
    @abstractmethod
    def course_strategy():
        pass

    @staticmethod
    @abstractmethod
    def evaluation_strategy():
        pass

    @staticmethod
    @abstractmethod
    def grade_sheet_strategy():
        pass

    @staticmethod
    @abstractmethod
    def info_page_strategy():
        pass

    @staticmethod
    @abstractmethod
    def study_line_strategy():
        pass

    @staticmethod
    @abstractmethod
    def teacher_strategy():
        pass

    @staticmethod
    @abstractmethod
    def term_strategy():
        pass

    @staticmethod
    @abstractmethod
    def year_strategy():
        pass


class DtuStrategySwitch(StrategySwitch):

    @staticmethod
    def school_strategy():
        return DataStrategy#DtuSchool

    @staticmethod
    def course_strategy():
        return DataStrategy#DtuCourses

    @staticmethod
    def evaluation_strategy():
        return DataStrategy#DtuEvaluation

    @staticmethod
    def grade_sheet_strategy():
        return DataStrategy#DtuGradeSheet

    @staticmethod
    def info_page_strategy():
        return DataStrategy#DtuInfoPage

    @staticmethod
    def study_line_strategy():
        return DataStrategy#DtuStudyLine

    @staticmethod
    def teacher_strategy():
        return DataStrategy#DtuTeacher

    @staticmethod
    def term_strategy():
        return DataStrategy#DtuTerm

    @staticmethod
    def year_strategy():
        return DataStrategy#DtuYear

class RootObj(ABC):

    _registry: 'Registry' = Registry()

    def __init__(self) -> None:
        self.name = ""

    def get_name(self) -> str:
        return self.name

    @staticmethod
    def get(key: str) -> 'RootObj':
        return RootObj._registry.get(key)
    @classmethod
    def set(cls, key: str) -> None:
        RootObj._registry.set_unique_key(key, cls())

class Attribute(RootObj):
    pass


class Domain(Attribute):

    def get_strategy_switch(self) -> Type[StrategySwitch]:
        if self.name != "":
            return DtuStrategySwitch
        return DtuStrategySwitch

    @staticmethod
    def extract_domain_from_key(unparsed_domain: str) -> 'RootObj':
        key: str = unparsed_domain
        if unparsed_domain != "":
            key = "dtu"
        return Domain.get(key)

class TimePeriod(Attribute):
    pass

class DataObject(RootObj):

    KEY_SEPARATOR = "__"

    def __init__(self) -> None:
        super().__init__()
        self.domain: Domain
        self.time: TimePeriod
        self.name = ""
        self.children: List[DataObject]

    def add_child(self, child: 'DataObject') -> None:
        self.children.append(child)

    def get_children(self) -> List['DataObject']:
        return self.children

    def generate_key(self) -> str:
        key: str = self.domain.name
        key += self.KEY_SEPARATOR + self._get_class_name()
        key += self.KEY_SEPARATOR + self.time.name
        key += self.KEY_SEPARATOR + self.name
        return key

    def _get_class_name(self) -> str:
        return self.__class__.__name__

    @abstractmethod
    def get_data_strategy(self) -> DataStrategy:
        pass

class EndPoint(DataObject):
    pass

class Container(DataObject):
    pass
class DataManager:
    def __init__(self) -> None:
        self._memory: DAO = Registry()
        self._disk: DAO = FileAccess()
        self._construction_strategy = ()

    def get(self, key: str) -> RootObj:
        data_object: RootObj
        if self._memory.exists(key):
            data_object = self._memory.get(key)
        elif self._disk.exists(key):
            data_object = self._disk.get(key)
        else:
            pass
        return data_object

    def set(self):
        pass

class School(Container):
    def get_data_strategy(self) -> DataStrategy:
        return self.domain.get_strategy_switch().school_strategy()
class Year(Container):
    def get_data_strategy(self) -> DataStrategy:
        return self.domain.get_strategy_switch().year_strategy()
class Course(Container):
    def get_data_strategy(self) -> DataStrategy:
        return self.domain.get_strategy_switch().course_strategy()
class Term(Container):
    def get_data_strategy(self) -> DataStrategy:
        return self.domain.get_strategy_switch().term_strategy()
class Teacher(Container):
    def get_data_strategy(self) -> DataStrategy:
        return self.domain.get_strategy_switch().teacher_strategy()
class StudyLine(Container):
    def get_data_strategy(self) -> DataStrategy:
        return self.domain.get_strategy_switch().study_line_strategy()
class Evaluation(EndPoint):
    def get_data_strategy(self) -> DataStrategy:
        return self.domain.get_strategy_switch().evaluation_strategy()
class GradeSheet(EndPoint):
    def get_data_strategy(self) -> DataStrategy:
        return self.domain.get_strategy_switch().grade_sheet_strategy()
class InfoPage(EndPoint):
    def get_data_strategy(self) -> DataStrategy:
        return self.domain.get_strategy_switch().info_page_strategy()

#School
#Year
#Course
#Term
#Teacher
#StudyLine
#Evaluation
#GradeSheet
#InfoPage