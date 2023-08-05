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

class DomainStrategy(ABC):

    @staticmethod
    @abstractmethod
    def get_key():
        pass

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
    def time_strategy():
        pass


class DtuStrategy(DomainStrategy):

    DOMAIN_NAME = "dtu"

    @staticmethod
    def get_key():
        return DtuStrategy.DOMAIN_NAME

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
    def time_strategy():
        return DataStrategy#DtuTerm


class DataObject(ABC):

    KEY_SEPARATOR = "__"
    ROOT_NAME: str = "root"
    registry: Registry = Registry()

    def __init__(self, key) -> None:
        self.name = key
        self.register()

    def get_name(self) -> str:
        return self.name

    def _get_class_name(self) -> str:
        return self.__class__.__name__

    def get_key_separator(self):
        return DataObject.KEY_SEPARATOR

    def register(self) -> None:
        key = self.generate_general_key()
        DataObject.registry.set_unique_key(key, self)

    def generate_general_key(self) -> str:
        separator: str = self.get_key_separator()
        class_and_separator: str = self._get_class_name() + separator
        key_modifier: str = self._key_modifier()
        name: str = self.name
        if self._key_modifier() != "":
            return class_and_separator + key_modifier + separator + name
        else:
            return class_and_separator + name

    def _key_modifier(self) -> str:
        return ""


class Composite(DataObject):

    KEY_SEPARATOR = "__"

    def __init__(self, name: str) -> None:
        self.children: List[Composite]
        super().__init__(name)

    def add_child(self, child: 'Composite') -> None:
        self.children.append(child)

    def get_children(self) -> List['Composite']:
        return self.children

class Domain(Composite):

    def get_data_strategy(self) -> Type[DomainStrategy]:
        return DtuStrategy

class DomainSpecificObject(Composite):

    def __init__(self, name: str) -> None:
        self.domain: Domain
        super().__init__(name)

    def get_domain_name(self) -> str:
        return self.domain.get_name()

    def _key_modifier(self) -> str:
        domain_name: str = self.get_domain_name()
        separator: str = self.get_key_separator()
        extra_key_mod: str = self._extra_key_modifier()
        if extra_key_mod != "":
            return domain_name + separator + extra_key_mod
        else:
            return domain_name

    def _extra_key_modifier(self) -> str:
        return ""


class TimePeriod(Composite):

    def test(self):
        pass

class DtuTimePeriod(TimePeriod):

    @staticmethod
    def parse_time_from_key(unparsed_time: str) -> 'DataObject':
        key: str = unparsed_time
        if unparsed_time != "":
            key = "2069"
        return DataObject.registry.get(key)

class DtuAcademicYear(DtuTimePeriod):

    @staticmethod
    def extract_year_from_key(unparsed_year: str) -> 'DataObject':
        key: str = unparsed_year
        if unparsed_year != "":
            key = "2069"
        return DataObject.registry.get(key)

class DtuAcademicTerm(DtuTimePeriod):

    @staticmethod
    def extract_year_from_key(unparsed_year: str) -> 'DataObject':
        key: str = unparsed_year
        if unparsed_year != "":
            key = "2069"
        return DataObject.registry.get(key)


class TimeSpecificObject(DomainSpecificObject):

    def __init__(self, name: str) -> None:
        self.time_period: TimePeriod
        super().__init__(name)


    def get_time_period_name(self) -> str:
        return self.time_period.get_name()

    def _extra_key_modifier(self) -> str:
        return self.get_time_period_name()

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

class School(DomainSpecificObject):
    def get_data_strategy(self) -> DataStrategy:
        return self.domain.get_data_strategy().school_strategy()
class Year(DomainSpecificObject):
    def get_data_strategy(self) -> DataStrategy:
        return self.domain.get_data_strategy().time_strategy()
class Course(TimeSpecificObject):
    def get_data_strategy(self) -> DataStrategy:
        return self.domain.get_data_strategy().course_strategy()
class Term(DomainSpecificObject):
    def get_data_strategy(self) -> DataStrategy:
        return self.domain.get_data_strategy().time_strategy()
class Teacher(TimeSpecificObject):
    def get_data_strategy(self) -> DataStrategy:
        return self.domain.get_data_strategy().teacher_strategy()
class StudyLine(TimeSpecificObject):
    def get_data_strategy(self) -> DataStrategy:
        return self.domain.get_data_strategy().study_line_strategy()
class Evaluation(TimeSpecificObject):
    def get_data_strategy(self) -> DataStrategy:
        return self.domain.get_data_strategy().evaluation_strategy()
class GradeSheet(TimeSpecificObject):
    def get_data_strategy(self) -> DataStrategy:
        return self.domain.get_data_strategy().grade_sheet_strategy()
class InfoPage(TimeSpecificObject):
    def get_data_strategy(self) -> DataStrategy:
        return self.domain.get_data_strategy().info_page_strategy()

#School
#Year
#Course
#Term
#Teacher
#StudyLine
#Evaluation
#GradeSheet
#InfoPage