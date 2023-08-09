from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Type, Callable


class DAO(ABC):

    def exists(self, key: str) -> bool:
        return self._is_accessible(key)

    def get(self, key: str) -> 'Composite':
        self._raise_error_if_key_missing(key)
        return self._read(key)

    def set_unique_key(self, key: str, value: 'Composite') -> None:
        self._raise_error_if_key_exists(key)
        self._set(key, value)

    def set_if_key_missing(self, key: str, value: 'Composite') -> None:
        if not self.exists(key):
            self._set(key, value)

    def _set(self, key: str, value: 'Composite') -> None:
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
    def _read(self, key: str) -> 'Composite':
        pass

    @abstractmethod
    def _write(self, key: str, value: 'Composite') -> None:
        pass

class Registry(DAO):
    def __init__(self) -> None:
        self.dct: Dict[str, Composite] = {}

    def _is_accessible(self, key: str) -> bool:
        return key in self.dct

    def _read(self, key: str) -> 'Composite':
        return self.dct[key]

    def _write(self, key: str, value: 'Composite') -> None:
        self.dct[key] = value

class DataStrategy:

    @staticmethod
    def generate_data_object(time_period: 'TimePeriod', name: str) -> 'Composite':
        return EndPoint(name, Domain("test"), time_period)

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

class Domain:

    def __init__(self, key) -> None:
        self.name = key
        self.strategy: DomainStrategy = DtuStrategy()

    def get_name(self) -> str:
        return self.name

    def get_data_strategy(self, class_id: str) -> Type[DataStrategy]:
        if class_id == Composite.CLASS_ID:
            pass
        return DataStrategy

class TimePeriod:

    def __init__(self, key) -> None:
        self.name = key

    def get_name(self) -> str:
        return self.name

class Serializer:

    KEY_SEPARATOR: str = "__"

    @staticmethod
    def serialize_data(data: Tuple[Domain,TimePeriod,str,str]) -> str:
        domain = data[0].get_name()
        time = data[1].get_name()
        class_id = data[2]
        name = data[3]
        sep: str = Serializer.KEY_SEPARATOR
        return domain + sep + time + sep + class_id + sep + name

    @staticmethod
    def deserialize_key(key: str) -> Tuple[Domain,TimePeriod,str,str]:
        data_list: List[str] = key.split(Serializer.KEY_SEPARATOR)
        domain: Domain = Domain(data_list[0])
        time: TimePeriod = TimePeriod(data_list[1])
        class_id: str = data_list[2]
        name: str = data_list[3]
        return (domain, time, class_id, name)

    @staticmethod
    def deserialize_domain(key: str) -> Domain:
        return Serializer.deserialize_key(key)[0]

    @staticmethod
    def deserialize_time_period(key: str) -> TimePeriod:
        return Serializer.deserialize_key(key)[1]

    @staticmethod
    def deserialize_class_id(key: str) -> str:
        return Serializer.deserialize_key(key)[2]

    @staticmethod
    def deserialize_name(key: str) -> str:
        return Serializer.deserialize_key(key)[3]

class DataManager:
    def __init__(self) -> None:
        self.serializer: Serializer
        self._memory: DAO = Registry()
        self._construction_strategy = ()

    def get(self, key: str) -> 'Composite':
        if self._memory.exists(key):
            data_object = self._memory.get(key)
        else:
            domain: Domain = self.serializer.deserialize_domain(key)
            time_period: TimePeriod = self.serializer.deserialize_time_period(key)
            class_id: str = self.serializer.deserialize_class_id(key)
            name: str = self.serializer.deserialize_name(key)
            strategy: Type[DataStrategy] = DataStrategy
            strategy = domain.get_data_strategy(class_id)
            data_object = strategy.generate_data_object(time_period, name)
            self.register(key, data_object)
        return data_object

    def register(self, key: str, data_object: 'Composite') -> None:
        self._memory.set_unique_key(key, data_object)

    def serialize_data(self, data: Tuple[Domain,TimePeriod,str,str]):
        return self.serializer.serialize_data(data)

class Composite:

    CLASS_ID: str = ""
    DEFAULT_DATA_MANAGER: DataManager = DataManager()

    def __init__(self, name: str, domain: Domain, time_period: TimePeriod) -> None:
        self.name: str = name
        self.domain: Domain = domain
        self.time_period: TimePeriod = time_period
        self.class_id: str = self.get_class_id()
        self.data_manager: DataManager = Composite.DEFAULT_DATA_MANAGER

    def serialize(self, name: str) -> str:
        domain: Domain = self.domain
        time: TimePeriod = self.time_period
        class_id: str = self.class_id
        return self.data_manager.serialize_data((domain, time, class_id, name))

    def get_name(self) -> str:
        return self.name

    def get_class_id(self) -> str:
        return self.CLASS_ID

    @abstractmethod
    def perform_action(self, action: Callable[['Composite'], float]) -> float:
        pass

    @abstractmethod
    def build(self) -> None:
        pass

class Container(Composite):
    def __init__(self, name: str, domain: Domain, time_period: TimePeriod) -> None:
        self.children: List[Composite]
        super().__init__(name, domain, time_period)

    def perform_action(self, action: Callable[[Composite], float]) -> float:
        child_sum: float = 0.0
        for child in self._get_children():
            child_sum += child.perform_action(action)
        return child_sum / len(self._get_children())

    def build(self) -> None:
        child_names: List[str] = self._get_children_to_be_created()
        for name in child_names:
            key: str = self.serialize(name)
            child: Composite = self.data_manager.get(key)
            self._add_child(child)

    def _add_child(self, child: 'Composite') -> None:
        self.children.append(child)

    def _get_children(self) -> List['Composite']:
        return self.children

    @abstractmethod
    def _get_children_to_be_created(self) -> List[str]:
        return []

class EndPoint(Composite):
    def __init__(self, name: str, domain: Domain, time_period: TimePeriod) -> None:
        self.data_instance: Composite
        super().__init__(name, domain, time_period)

    def perform_action(self, action: Callable[[Composite], float]) -> float:
        data_instance: Composite = self._get_data_instance()
        average = action(data_instance)
        return average

    def build(self) -> None:
        name: str = self.get_name()
        key: str = self.serialize(name)
        self.data_instance = self.data_manager.get(key)

    def _get_data_instance(self) -> Composite:
        return self.data_instance

"""
class School(Composite):
    def get_data_strategy(self) -> DataStrategy:
        return self.domain.get_data_strategy().school_strategy()
class Year(Composite):
    def get_data_strategy(self) -> DataStrategy:
        return self.domain.get_data_strategy().time_strategy()
class Course(Composite):
    def get_data_strategy(self) -> DataStrategy:
        return self.domain.get_data_strategy().course_strategy()
class Term(Composite):
    def get_data_strategy(self) -> DataStrategy:
        return self.domain.get_data_strategy().time_strategy()
class Teacher(Composite):
    def get_data_strategy(self) -> DataStrategy:
        return self.domain.get_data_strategy().teacher_strategy()
class StudyLine(Composite):
    def get_data_strategy(self) -> DataStrategy:
        return self.domain.get_data_strategy().study_line_strategy()
class Evaluation(EndPoint):
    def get_data_strategy(self) -> DataStrategy:
        return self.domain.get_data_strategy().evaluation_strategy()
class GradeSheet(EndPoint):
    def get_data_strategy(self) -> DataStrategy:
        return self.domain.get_data_strategy().grade_sheet_strategy()
class InfoPage(EndPoint):
    def get_data_strategy(self) -> DataStrategy:
        return self.domain.get_data_strategy().info_page_strategy()
"""

#School
#Year
#Course
#Term
#Teacher
#StudyLine
#Evaluation
#GradeSheet
#InfoPage