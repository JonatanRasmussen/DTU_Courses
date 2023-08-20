from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Type, Callable, TypeVar, Generic
import json

T = TypeVar('T')

class DAO(Generic[T]):

    def __init__(self) -> None:
        self.dct: Dict[str, T] = {}

    def exists(self, key: str) -> bool:
        return key in self.dct

    def read(self, key: str) -> T:
        self._raise_error_if_key_missing(key)
        return self.dct[key]

    def write_unique_key(self, key: str, value: T) -> None:
        self._raise_error_if_key_exists(key)
        self._write(key, value)

    def write_if_key_missing(self, key: str, value: T) -> None:
        if not self.exists(key):
            self._write(key, value)

    def _write(self, key: str, value: T) -> None:
        self.dct[key] = value

    def _raise_error_if_key_exists(self, key: str) -> None:
        if not self.exists(key):
            raise KeyError(f"Key '{key}' doesn't exist.")

    def _raise_error_if_key_missing(self, key: str) -> None:
        if self.exists(key):
            raise KeyError(f"Key '{key}' already exists.")

class DiskAccess(DAO,Generic[T]):

    FILE_PATH: str = "json_files/"
    FILE_NAME: str = "parsed_data"

    def __init__(self) -> None:
        super().__init__()
        self.file_path: str = f"{DiskAccess.FILE_PATH}{DiskAccess.FILE_NAME}.json"
        self._load_from_disk()

    def _write(self, key: str, value: T) -> None:
        self.dct[key] = value
        self._save_to_disk()

    def _load_from_disk(self) -> None:
        try:
            with open(self.file_path, 'r', encoding='utf-8') as json_file:
                self.dct = json.load(json_file)
        except FileNotFoundError:
            self.dct = {}

    def _save_to_disk(self) -> None:
        with open(self.file_path, 'w', encoding='utf-8') as json_file:
            json.dump(self.dct, json_file, indent=4)

class TimePeriod:

    NAME_OF_EMPTY_TIME_PERIOD: str = "timeless"

    def __init__(self, term: str | None, year: int | None) -> None:
        self.term: str | None = term
        self.year: int | None = year

    def get_name(self) -> str:
        if (self.year is None) and (self.term is None):
            return self._get_empty_name()
        elif self.year is None:
            return self._get_yearless_name()
        elif self.term is None:
            return self._get_termless_name()
        else:
            return self._get_term_and_year_name()

    def get_term(self) -> str:
        return str(self.term)

    def get_year(self) -> int:
        numeric_year: int = self._ensure_year_is_numeric()
        return numeric_year

    def _get_empty_name(self) -> str:
        return TimePeriod.NAME_OF_EMPTY_TIME_PERIOD

    def _get_yearless_name(self) -> str:
        return str(self.term)

    def _get_termless_name(self) -> str:
        return str(self.year)

    def _get_term_and_year_name(self) -> str:
        numeric_year: int = self._ensure_year_is_numeric()
        return str(self.term) + str(numeric_year - 2000)

    def _ensure_year_is_numeric(self) -> int:
        if self.year is None:
            raise ValueError(f"Time period {self.get_name()} has no year")
        return self.year

class TimeUnitChecker(ABC):

    @staticmethod
    @abstractmethod
    def is_term_based(class_id: str) -> bool:
        pass

    @staticmethod
    @abstractmethod
    def is_time_based(class_id: str) -> bool:
        pass

class DefaultTimeUnitChecker(TimeUnitChecker):

    @staticmethod
    def is_term_based(class_id: str) -> bool:
        if class_id == "TODO: REMOVE":
            return True
        else:
            return False

    @staticmethod
    def is_time_based(class_id: str) -> bool:
        if class_id == School.get_class_id():
            return False
        else:
            return True

class DomainSpecificTimeConfig(ABC):

    @staticmethod
    def get_time_unit_checker() -> Type[TimeUnitChecker]:
        return DefaultTimeUnitChecker

    @staticmethod
    @abstractmethod
    def ordered_terms() -> List[str]:
        pass

    @staticmethod
    @abstractmethod
    def oldest_year() -> int:
        pass

    @staticmethod
    @abstractmethod
    def newest_year() -> int:
        pass

    @staticmethod
    @abstractmethod
    def oldest_term() -> str:
        pass

    @staticmethod
    @abstractmethod
    def newest_term() -> str:
        pass

class DtuTimeConfig(DomainSpecificTimeConfig):

    SEMESTERS: List[str] = ['F', 'E']
    OLDEST_TIME_PERIOD: TimePeriod = TimePeriod('F', 2018)
    NEWEST_TIME_PERIOD: TimePeriod = TimePeriod('E', 2023)

    @staticmethod
    def ordered_terms() -> List[str]:
        return DtuTimeConfig.SEMESTERS

    @staticmethod
    def oldest_year() -> int:
        return DtuTimeConfig.OLDEST_TIME_PERIOD.get_year()

    @staticmethod
    def newest_year() -> int:
        return DtuTimeConfig.NEWEST_TIME_PERIOD.get_year()

    @staticmethod
    def oldest_term() -> str:
        return DtuTimeConfig.OLDEST_TIME_PERIOD.get_term()

    @staticmethod
    def newest_term() -> str:
        return DtuTimeConfig.NEWEST_TIME_PERIOD.get_term()


class TimeRegistry:

    def __init__(self) -> None:
        self.time_dict: Dict[str, TimePeriod] = {}

    def get_time_from_registry(self, keyname: str) -> TimePeriod:
        if keyname not in self.time_dict:
            raise KeyError(f"{keyname} not found in {TimeRegistry.__name__} dict")
        return self.time_dict[keyname]

    def register_time(self, time_period: TimePeriod) -> None:
        self.time_dict[time_period.get_name()] = time_period

class TimePeriodGenerator:

    def __init__(self, config: Type[DomainSpecificTimeConfig]) -> None:
        self.ordered_terms: List[str] = config.ordered_terms()
        self.oldest_year: int = config.oldest_year()
        self.newest_year: int = config.newest_year()
        self.oldest_term: str = config.oldest_term()
        self.newest_term: str = config.newest_term()
        self.initialized_time_periods: TimeRegistry = TimeRegistry()

    def create_years(self) -> List[TimePeriod]:
        lst: List[TimePeriod] = []
        for year in self._calculate_years():
            time_period: TimePeriod = TimePeriod(None, year)
            self._add_to_registry(time_period)
            lst.append(time_period)
        return lst

    def create_all(self) -> List[TimePeriod]:
        lst: List[TimePeriod] = []
        for year in self._calculate_years():
            lst = lst + self.create_single_year(year)
        return lst

    def create_single_year(self, year: int) -> List[TimePeriod]:
        lst: List[TimePeriod] = []
        for term in self.ordered_terms:
            time_period: TimePeriod = TimePeriod(term, year)
            self._add_to_registry(time_period)
            lst.append(time_period)
        updated_lst: List[TimePeriod] = self._remove_invalid_terms(lst)
        return updated_lst

    def create_empty(self) -> TimePeriod:
        time_period: TimePeriod = TimePeriod(None, None)
        self._add_to_registry(time_period)
        return time_period

    def fetch_time_from_registry(self, name: str) -> TimePeriod:
        return self.initialized_time_periods.get_time_from_registry(name)

    def _add_to_registry(self, time_period: TimePeriod):
        self.initialized_time_periods.register_time(time_period)

    def _calculate_years(self) -> List[int]:
        year_lst: List[int] = []
        for year in range(self.oldest_year, self.newest_year + 1):
            year_lst.append(year)
        return year_lst

    def _remove_invalid_terms(self, lst: List[TimePeriod]) -> List[TimePeriod]:
        oldest: TimePeriod = TimePeriod(self.oldest_term, self.oldest_year)
        if oldest in lst:
            oldest_time_index = lst.index(oldest)
        else:
            oldest_time_index = 0
        newest: TimePeriod = TimePeriod(self.newest_term, self.newest_year)
        if newest in lst:
            newest_time_index = lst.index(newest)
        else:
            newest_time_index = len(lst) - 1
        return lst[oldest_time_index : newest_time_index + 1]

class TimeManager:

    def __init__(self, domain_config: Type[DomainSpecificTimeConfig]) -> None:
        self.domain_config: Type[DomainSpecificTimeConfig] = domain_config
        self.generator: TimePeriodGenerator = TimePeriodGenerator(self.domain_config)
        self.time_units_checker: Type[TimeUnitChecker] = self.domain_config.get_time_unit_checker()

    def read_time_from_keyname(self, keyname: str) -> TimePeriod:
        return self.generator.fetch_time_from_registry(keyname)

    def generate_all_time_periods(self) -> List[TimePeriod]:
        return self.generator.create_all()

    def generate_years(self) -> List[TimePeriod]:
        return self.generator.create_years()

    def generate_specific_year(self, year: int) -> List[TimePeriod]:
        return self.generator.create_single_year(year)

    def generate_empty_time_period(self) -> TimePeriod:
        return self.generator.create_empty()

    def data_class_is_term_based(self, class_id: str) -> bool:
        return self.time_units_checker.is_term_based(class_id)

    def data_class_is_time_based(self, class_id: str) -> bool:
        return self.time_units_checker.is_time_based(class_id)

    def number_of_terms(self) -> int:
        return len(self.domain_config.ordered_terms())

class DataObjectStrategy(ABC):
    pass

class ContainerStrategy(DataObjectStrategy):

    @staticmethod
    def get_child_list(time: str, name: str) -> List[str]:
        if time == name:
            return []
        return []

class DataPointStrategy(DataObjectStrategy):
    @staticmethod
    def get_data_dictionary(time: str, name: str) -> Dict[str,str]:
        if time == name:
            return {}
        return {}

class StrategyManager(ABC):

    @staticmethod
    def get_child_list(container: 'Container', child_id: str) -> List[str]:
        container_strategy: Type[ContainerStrategy] = StrategyManager.get_container_strategy(container, child_id)
        time: str = container.time_period.get_name()
        name: str = container.get_name()
        return container_strategy.get_child_list(time, name)

    @staticmethod
    def get_data_dictionary(data_point: 'DataPoint') -> Dict[str,str]:
        data_point_strategy: Type[DataPointStrategy] = StrategyManager.get_data_point_strategy(data_point)
        time: str = data_point.time_period.get_name()
        name: str = data_point.get_name()
        return data_point_strategy.get_data_dictionary(time, name)

    @staticmethod
    @abstractmethod
    def get_container_strategy(container: 'Container', child_id: str) -> Type[ContainerStrategy]:
        pass

    @staticmethod
    @abstractmethod
    def get_data_point_strategy(data_point: 'DataPoint') -> Type[DataPointStrategy]:
        pass

class DtuStrategyManager(StrategyManager):
    @staticmethod
    def get_container_strategy(container: 'Container', child_id: str) -> Type[ContainerStrategy]:
        if container.get_class_id() == child_id:
            return ContainerStrategy
        return ContainerStrategy

    @staticmethod
    def get_data_point_strategy(data_point: 'DataPoint') -> Type[DataPointStrategy]:
        if data_point.get_class_id() == "0":
            return DataPointStrategy
        return DataPointStrategy

class DomainConfig(ABC):
    @staticmethod
    @abstractmethod
    def get_domain_name() -> str:
        pass
    @staticmethod
    @abstractmethod
    def get_time_manager() -> TimeManager:
        pass
    @staticmethod
    @abstractmethod
    def get_strategy_manager() -> Type[StrategyManager]:
        pass

class DtuDomainConfig(DomainConfig):

    DOMAIN_NAME: str = "dtu"
    TIME_MANAGER: TimeManager = TimeManager(DtuTimeConfig)
    STRATEGY_MANAGER: Type[StrategyManager] = DtuStrategyManager

    @staticmethod
    def get_domain_name() -> str:
        return DtuDomainConfig.DOMAIN_NAME

    @staticmethod
    def get_time_manager() -> TimeManager:
        return DtuDomainConfig.TIME_MANAGER

    @staticmethod
    def get_strategy_manager() -> Type[StrategyManager]:
        return DtuDomainConfig.STRATEGY_MANAGER

class Domain:

    def __init__(self, domain_config: Type[DomainConfig], data_manager: 'DataManager') -> None:
        self.name: str = domain_config.get_domain_name()
        self.data_manager: DataManager = data_manager
        self.time_manager: TimeManager = domain_config.get_time_manager()
        self.strategy_manager: Type[StrategyManager] = domain_config.get_strategy_manager()

    def get_strategy_collection(self) -> Type[StrategyManager]:
        return self.strategy_manager

    def get_name(self) -> str:
        return self.name

    def fabricate_data_object(self, data_class: Type['DataObject'], name: str) -> 'DataObject':
        time_period = self.time_manager.generate_empty_time_period()
        fabricated_obj: DataObject = data_class(self, time_period, name)
        #key: str = self.data_manager.serialize(child)
        return fabricated_obj

    def get_child_list(self, container: 'Container', child_id: str) -> List[str]:
        return self.strategy_manager.get_child_list(container, child_id)

    def get_data_dictionary(self, data_point: 'DataPoint') -> Dict[str,str]:
        return self.strategy_manager.get_data_dictionary(data_point)

class DomainManager:

    DOMAIN_CONFIGS: List[Type[DomainConfig]] = [
        DtuDomainConfig
    ]

    def __init__(self) -> None:
        self.data_manager = DataManager()
        self.domains: Dict[str, Domain] = {}
        self._initialize_domains()

    initialized_domains: Dict[str, Domain] = {}

    def get_all_domains(self) -> List[Domain]:
        return list(self.domains.values())

    def _initialize_domains(self) -> None:
        for domain_config in DomainManager.DOMAIN_CONFIGS:
            dct_key = domain_config.get_domain_name()
            domain: Domain = Domain(domain_config, self.data_manager)
            self.domains[dct_key] = domain

    @staticmethod
    def read_domain_from_keyname(key_name: str) -> Domain:
        if key_name not in DomainManager.initialized_domains:
            raise KeyError(f"No domain with name '{key_name}' in domain dict")
        return DomainManager.initialized_domains[key_name]

class Serializer:

    KEY_SEPARATOR: str = "__"

    @staticmethod
    def serialize_object(data_obj: 'DataObject') -> str:
        domain_name: str = data_obj.domain.get_name()
        time_name: str = data_obj.time_period.get_name()
        class_id: str = data_obj.get_class_id()
        name: str = data_obj.get_name()
        sep: str = Serializer.KEY_SEPARATOR
        return domain_name + sep + time_name + sep + class_id + sep + name

    @staticmethod
    def serialize_object_data(data: Tuple[Domain,TimePeriod,str,str]) -> str:
        domain_name: str  = data[0].get_name()
        time_name: str  = data[1].get_name()
        class_id: str  = data[2]
        name: str  = data[3]
        sep: str = Serializer.KEY_SEPARATOR
        return domain_name + sep + time_name + sep + class_id + sep + name

    @staticmethod
    def deserialize_key(key: str) -> Tuple[Domain,TimePeriod,str,str]:
        data_list: List[str] = key.split(Serializer.KEY_SEPARATOR)
        domain: Domain = DomainManager.read_domain_from_keyname(data_list[0])
        time: TimePeriod = domain.time_manager.read_time_from_keyname(data_list[1])
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

    DEFAULT_SERIALIZER: Serializer = Serializer()

    def __init__(self) -> None:
        self.serializer: Serializer = DataManager.DEFAULT_SERIALIZER
        self._data_objects: DAO = DAO[DataObject]()
        self._data_dicts: DiskAccess = DiskAccess[Dict[str,str]]()
        self._child_lists: DiskAccess = DiskAccess[List[str]]()

    def data_object_exists(self, key: str) -> bool:
        return self._data_objects.exists(key)

    def data_dict_exists(self, key: str) -> bool:
        return self._data_dicts.exists(key)

    def child_list_exists(self, key: str) -> bool:
        return self._child_lists.exists(key)

    def get_data_object(self, data_obj: 'DataObject') -> 'DataObject':
        key: str = self.serialize(data_obj)
        return self._data_objects.read(key)

    def get_data_dict(self, key: str) -> Dict[str,str]:
        return self._data_dicts.read(key)

    def child_list_object(self, key: str) -> List[str]:
        return self._child_lists.read(key)

    def serialize_data(self, data: Tuple[Domain,TimePeriod,str,str]):
        return self.serializer.serialize_object_data(data)

    def serialize(self, data_obj: 'DataObject') -> str:
        return self.serializer.serialize_object(data_obj)


class DataObject(ABC):

    def __init__(self, domain: Domain, time_period: TimePeriod, name: str) -> None:
        self.domain: Domain = domain
        self.time_period: TimePeriod = time_period
        self.name: str = name

    def get_name(self) -> str:
        return self.name

    @staticmethod
    @abstractmethod
    def get_class_id() -> str:
        pass

    @abstractmethod
    def cascade_build(self) -> None:
        pass

class DataPoint(DataObject):

    def __init__(self, domain: Domain, time_period: TimePeriod, name: str) -> None:
        super().__init__(domain, time_period, name)
        self.data: Dict[str,str] = {}

    def cascade_build(self) -> None:
        self.data = self.domain.get_data_dictionary(self)

class Container(DataObject):

    def __init__(self, domain: Domain, time_period: TimePeriod, name: str) -> None:
        super().__init__(domain, time_period, name)
        self.children: Dict[str,List[DataObject]] = {}

    def cascade_build(self) -> None:
        child_classes: List[Type[DataObject]] = self._get_all_child_classes()
        for child_class in child_classes:
            child_id: str = child_class.get_class_id()
            child_names: List[str] = self.domain.get_child_list(self, child_id)
            for name in child_names:
                child: DataObject = self.domain.fabricate_data_object(child_class, name)
                self._add_child(child)
                child.cascade_build()

    def cascade_perform_action(self, key: str, action: Callable[['DataObject'], float]) -> float:
        if key in self.children:
            return self._perform_action(key, action)
        elif len(self._get_primary_children()) > 0:
            return self._continue_action_cascade(key, action)
        else:
            raise ValueError(f"Key {key} not found in {self.time_period.get_name()} {self.name}")

    def _perform_action(self, key: str, action: Callable[['DataObject'], float]) -> float:
        child_list: List[DataObject] = self.children[key]
        if len(child_list) != 1:
            raise ValueError(f"There should be exactly 1 child in {self.time_period.get_name()} {self.name}, not {len(child_list)}")
        else:
            return action(child_list[0])

    def _continue_action_cascade(self, key: str, action: Callable[['DataObject'], float]) -> float:
        child_sum: float = 0.0
        for child in self._get_primary_children():
            child_sum += child.cascade_perform_action(key, action)
        return child_sum / len(self._get_primary_children())

    def _add_child(self, child: 'DataObject') -> None:
        key: str = child.get_class_id()
        self.children[key].append(child)

    def _get_children(self, key) -> List['DataObject']:
        return self.children[key]

    def _get_primary_children(self) -> List['Container']:
        lst_of_children: List['Container'] = []
        lst_of_keys = self._get_primary_child_class_keys()
        for key in lst_of_keys:
            if key in self.children:
                lst_of_children.extend(self._ensure_children_is_containers(self.children[key]))
        return lst_of_children

    def _get_primary_child_class_keys(self) -> List[str]:
        main_child_classes: List[Type[Container]] = self.get_primary_child_classes()
        lst_of_keys: List[str] = []
        for main_child_class in main_child_classes:
            lst_of_keys.append(main_child_class.get_class_id())
        return lst_of_keys

    def _error_unsupported_child_class(self, child_id: str) -> KeyError:
        return KeyError(f"Error, {child_id} is not a child of {self.get_class_id()}")

    def _ensure_children_is_containers(self, containers: List[DataObject]) -> List['Container']:
        container_list: List['Container'] = []
        for container in containers:
            if isinstance(container, Container):
                container_list.append(container)
            else:
                raise ValueError(f"Error: {self.time_period.get_name()} {self.name} has {container.time_period.get_name()} {container.name} as main child, even though {container.time_period.get_name()} {container.name} is not a container")
        return container_list

    @staticmethod
    def _get_all_child_classes() -> List[Type[DataObject]]:
        return Container.get_primary_child_classes() + Container.get_secondary_child_classes()

    @staticmethod
    def get_primary_child_classes() -> List[Type['Container']]:
        return []

    @staticmethod
    def get_secondary_child_classes() -> List[Type[DataObject]]:
        return []


class School(Container):

    CLASS_ID: str = "school"

    @staticmethod
    def get_class_id() -> str:
        return School.CLASS_ID

    @staticmethod
    def get_primary_child_classes() -> List[Type['Container']]:
        return [Year]

class Year(Container):

    CLASS_ID: str = "year"

    @staticmethod
    def get_class_id() -> str:
        return School.CLASS_ID

    @staticmethod
    def get_primary_child_classes() -> List[Type['Container']]:
        return [Course]

    @staticmethod
    def get_secondary_child_classes() -> List[Type[DataObject]]:
        return [StudyLine, Teacher]

class Course(Container):

    CLASS_ID: str = "course"

    @staticmethod
    def get_class_id() -> str:
        return School.CLASS_ID

    @staticmethod
    def get_primary_child_classes() -> List[Type['Container']]:
        return [Term]

    @staticmethod
    def get_secondary_child_classes() -> List[Type[DataObject]]:
        return [InfoPage]

class Term(Container):

    CLASS_ID: str = "term"

    @staticmethod
    def get_class_id() -> str:
        return School.CLASS_ID

    @staticmethod
    def get_secondary_child_classes() -> List[Type[DataObject]]:
        return [Evaluation, GradeSheet]

class Teacher(Container):

    CLASS_ID: str = "teacher"

    @staticmethod
    def get_class_id() -> str:
        return School.CLASS_ID

    @staticmethod
    def get_primary_child_classes() -> List[Type['Container']]:
        return [Course]

class StudyLine(Container):

    CLASS_ID: str = "study_line"

    @staticmethod
    def get_class_id() -> str:
        return School.CLASS_ID

    @staticmethod
    def get_primary_child_classes() -> List[Type['Container']]:
        return [Course]

class Evaluation(DataPoint):

    CLASS_ID: str = "evaluation"

    @staticmethod
    def get_class_id() -> str:
        return School.CLASS_ID

class GradeSheet(DataPoint):

    CLASS_ID: str = "grade_sheet"

    @staticmethod
    def get_class_id() -> str:
        return School.CLASS_ID

class InfoPage(DataPoint):

    CLASS_ID: str = "info_page"

    @staticmethod
    def get_class_id() -> str:
        return School.CLASS_ID

class ClassTable:

    @staticmethod
    def get_class_from_id(class_id: str) -> Type[DataObject]:
        class_dct: Dict[str,Type[DataObject]] = ClassTable._get_class_dct()
        if class_id in class_dct:
            return class_dct[class_id]
        else:
            raise ValueError(f"Class '{class_id}' not found in {__name__}")

    @staticmethod
    def _get_class_dct() -> Dict[str,Type[DataObject]]:
        dct: Dict[str,Type[DataObject]] = {
            School.get_class_id(): School,
            Year.get_class_id(): Year,
            Course.get_class_id(): Course,
            Term.get_class_id(): Term,
            Evaluation.get_class_id(): Evaluation,
            GradeSheet.get_class_id(): GradeSheet,
            InfoPage.get_class_id(): InfoPage,
            Teacher.get_class_id(): Teacher,
            StudyLine.get_class_id(): StudyLine,
        }
        return dct

#School
#Year
#Course
#Term
#Teacher
#StudyLine
#Evaluation
#GradeSheet
#InfoPage

def main() -> None:
    domain_manager: DomainManager = DomainManager()
    domain_list: List[Domain] = domain_manager.get_all_domains()
    for domain in domain_list:
        terms: List[TimePeriod] = domain.time_manager.generate_all_time_periods()
        years: List[TimePeriod] = domain.time_manager.generate_years()
        empty_time: TimePeriod = domain.time_manager.generate_empty_time_period()
        print(terms)
        print(years)
        print(empty_time)

if __name__ == "__main__":
    main()