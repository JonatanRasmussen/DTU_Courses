from abc import ABC, abstractmethod
from typing import Dict, List, Type


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
        return School(key)

    def _write(self, key: str, value: 'DataObject') -> None:
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

class DataObject(ABC):

    KEY_SEPARATOR = "__"
    ROOT_NAME: str = "root"
    _registry: Registry = Registry()

    def __init__(self, key) -> None:
        self.name = key
        self.register()

    def get_name(self) -> str:
        return self.name

    def _get_class_name(self) -> str:
        return self.__class__.__name__

    def register(self) -> None:
        key = self.generate_general_key()
        DataObject._registry.set_unique_key(key, self)

    def generate_general_key(self) -> str:
        separator: str = DataObject.KEY_SEPARATOR
        class_and_separator: str = self._get_class_name() + separator
        key_modifier: str = self._key_modifier()
        name: str = self.name
        if self._key_modifier() != "":
            return class_and_separator + key_modifier + separator + name
        else:
            return class_and_separator + name

    def _key_modifier(self) -> str:
        return ""

class Domain(DataObject):

    def __init__(self, name: str) -> None:
        self.domain: Domain

    def get_strategy_switch(self) -> Type[StrategySwitch]:
        if self.name != "":
            return DtuStrategySwitch
        return DtuStrategySwitch

    @staticmethod
    def extract_domain_from_key(unparsed_domain: str) -> 'DataObject':
        key: str = unparsed_domain
        if unparsed_domain != "":
            key = "dtu"
        return DataObject._registry.get(key)

class TimePeriod(DataObject):

    def __init__(self, name: str) -> None:
        self.domain: Domain
        super().__init__(name)

    @staticmethod
    def extract_year_from_key(unparsed_year: str) -> 'DataObject':
        key: str = unparsed_year
        if unparsed_year != "":
            key = "2069"
        return DataObject._registry.get(key)

    @abstractmethod
    def initialize_domain(self):
        domain = DtuStrategySwitch

class DtuAcademicYear(DtuTimePeriod):

    @staticmethod
    def extract_year_from_key(unparsed_year: str) -> 'DataObject':
        key: str = unparsed_year
        if unparsed_year != "":
            key = "2069"
        return DataObject._registry.get(key)

class DtuAcademicTerm(DtuTimePeriod):

    @staticmethod
    def extract_year_from_key(unparsed_year: str) -> 'DataObject':
        key: str = unparsed_year
        if unparsed_year != "":
            key = "2069"
        return DataObject._registry.get(key)

class Composite(DataObject):

    KEY_SEPARATOR = "__"

    def __init__(self, name: str) -> None:
        self.domain: Domain
        self.time: TimePeriod
        self.children: List[Composite]
        super().__init__(name)

    def add_child(self, child: 'Composite') -> None:
        self.children.append(child)

    def get_children(self) -> List['Composite']:
        return self.children

    def generate_key(self) -> str:
        key: str = self.domain.name
        key += self.KEY_SEPARATOR + self._get_class_name()
        key += self.KEY_SEPARATOR + self.time.name
        key += self.KEY_SEPARATOR + self.name
        return key

    @abstractmethod
    def get_data_strategy(self) -> DataStrategy:
        pass

class EndPoint(Composite):
    pass

class Container(Composite):
    pass
class DataManager:
    def __init__(self) -> None:
        self._memory: DAO = Registry()
        self._disk: DAO = FileAccess()
        self._construction_strategy = ()

    def get(self, key: str) -> DataObject:
        data_object: DataObject
        if self._memory.exists(key):
            data_object = self._memory.get(key)
        elif self._disk.exists(key):
            data_object = self._disk.get(key)
        else:
            pass
        return data_object

    def set(self):
        pass

class School(Composite):
    def get_data_strategy(self) -> DataStrategy:
        return self.domain.get_strategy_switch().school_strategy()
class Year(Composite):
    def get_data_strategy(self) -> DataStrategy:
        return self.domain.get_strategy_switch().year_strategy()
class Course(Composite):
    def get_data_strategy(self) -> DataStrategy:
        return self.domain.get_strategy_switch().course_strategy()
class Term(Composite):
    def get_data_strategy(self) -> DataStrategy:
        return self.domain.get_strategy_switch().term_strategy()
class Teacher(Composite):
    def get_data_strategy(self) -> DataStrategy:
        return self.domain.get_strategy_switch().teacher_strategy()
class StudyLine(Composite):
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