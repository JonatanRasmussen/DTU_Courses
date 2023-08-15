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
        if class_id == Evaluation.get_class_id():
            return True
        elif class_id == GradeSheet.get_class_id():
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

class DataStrategy(ABC):

    @staticmethod
    def generate_data_object(time_period: TimePeriod, name: str) -> 'Composite':
        return School(name, Domain(DtuStrategyCollection()), time_period)

    @staticmethod
    def generate_children(time_period: TimePeriod, name: str) -> List[str]:
        return [time_period.get_name(), name]

class SchoolStrategy(DataStrategy):
    @staticmethod
    def generate_data_object(time_period: TimePeriod, name: str) -> 'Composite':
        return School(name, Domain(DtuStrategyCollection()), time_period)

    @staticmethod
    def generate_children(time_period: TimePeriod, name: str) -> List[str]:
        return [time_period.get_name(), name]

class YearStrategy(DataStrategy):
    @staticmethod
    def generate_data_object(time_period: TimePeriod, name: str) -> 'Composite':
        return School(name, Domain(DtuStrategyCollection()), time_period)

    @staticmethod
    def generate_children(time_period: TimePeriod, name: str) -> List[str]:
        return [time_period.get_name(), name]

class CourseStrategy(DataStrategy):
    @staticmethod
    def generate_data_object(time_period: TimePeriod, name: str) -> 'Composite':
        return School(name, Domain(DtuStrategyCollection()), time_period)

    @staticmethod
    def generate_children(time_period: TimePeriod, name: str) -> List[str]:
        return [time_period.get_name(), name]

class TermStrategy(DataStrategy):
    @staticmethod
    def generate_data_object(time_period: TimePeriod, name: str) -> 'Composite':
        return School(name, Domain(DtuStrategyCollection()), time_period)

    @staticmethod
    def generate_children(time_period: TimePeriod, name: str) -> List[str]:
        return [time_period.get_name(), name]

class EvaluationStrategy(DataStrategy):
    @staticmethod
    def generate_data_object(time_period: TimePeriod, name: str) -> 'Composite':
        return School(name, Domain(DtuStrategyCollection()), time_period)

    @staticmethod
    def generate_children(time_period: TimePeriod, name: str) -> List[str]:
        return [time_period.get_name(), name]

class GradeSheetStrategy(DataStrategy):
    @staticmethod
    def generate_data_object(time_period: TimePeriod, name: str) -> 'Composite':
        return School(name, Domain(DtuStrategyCollection()), time_period)

    @staticmethod
    def generate_children(time_period: TimePeriod, name: str) -> List[str]:
        return [time_period.get_name(), name]

class InfoPageStrategy(DataStrategy):
    @staticmethod
    def generate_data_object(time_period: TimePeriod, name: str) -> 'Composite':
        return School(name, Domain(DtuStrategyCollection()), time_period)

    @staticmethod
    def generate_children(time_period: TimePeriod, name: str) -> List[str]:
        return [time_period.get_name(), name]

class TeacherStrategy(DataStrategy):
    @staticmethod
    def generate_data_object(time_period: TimePeriod, name: str) -> 'Composite':
        return School(name, Domain(DtuStrategyCollection()), time_period)

    @staticmethod
    def generate_children(time_period: TimePeriod, name: str) -> List[str]:
        return [time_period.get_name(), name]

class StudyLineStrategy(DataStrategy):
    @staticmethod
    def generate_data_object(time_period: TimePeriod, name: str) -> 'Composite':
        return School(name, Domain(DtuStrategyCollection()), time_period)

    @staticmethod
    def generate_children(time_period: TimePeriod, name: str) -> List[str]:
        return [time_period.get_name(), name]

class DtuSchoolStrategy(SchoolStrategy):
    @staticmethod
    def generate_data_object(time_period: TimePeriod, name: str) -> 'Composite':
        return School(name, Domain(DtuStrategyCollection()), time_period)

    @staticmethod
    def generate_children(time_period: TimePeriod, name: str) -> List[str]:
        return [time_period.get_name(), name]

class DtuYearStrategy(YearStrategy):
    @staticmethod
    def generate_data_object(time_period: TimePeriod, name: str) -> 'Composite':
        return School(name, Domain(DtuStrategyCollection()), time_period)

    @staticmethod
    def generate_children(time_period: TimePeriod, name: str) -> List[str]:
        return [time_period.get_name(), name]

class DtuCourseStrategy(CourseStrategy):
    @staticmethod
    def generate_data_object(time_period: TimePeriod, name: str) -> 'Composite':
        return School(name, Domain(DtuStrategyCollection()), time_period)

    @staticmethod
    def generate_children(time_period: TimePeriod, name: str) -> List[str]:
        return [time_period.get_name(), name]

class DtuTermStrategy(TermStrategy):
    @staticmethod
    def generate_data_object(time_period: TimePeriod, name: str) -> 'Composite':
        return School(name, Domain(DtuStrategyCollection()), time_period)

    @staticmethod
    def generate_children(time_period: TimePeriod, name: str) -> List[str]:
        return [time_period.get_name(), name]

class DtuEvaluationStrategy(EvaluationStrategy):
    @staticmethod
    def generate_data_object(time_period: TimePeriod, name: str) -> 'Composite':
        return School(name, Domain(DtuStrategyCollection()), time_period)

    @staticmethod
    def generate_children(time_period: TimePeriod, name: str) -> List[str]:
        return [time_period.get_name(), name]

class DtuGradeSheetStrategy(GradeSheetStrategy):
    @staticmethod
    def generate_data_object(time_period: TimePeriod, name: str) -> 'Composite':
        return School(name, Domain(DtuStrategyCollection()), time_period)

    @staticmethod
    def generate_children(time_period: TimePeriod, name: str) -> List[str]:
        return [time_period.get_name(), name]

class DtuInfoPageStrategy(InfoPageStrategy):
    @staticmethod
    def generate_data_object(time_period: TimePeriod, name: str) -> 'Composite':
        return School(name, Domain(DtuStrategyCollection()), time_period)

    @staticmethod
    def generate_children(time_period: TimePeriod, name: str) -> List[str]:
        return [time_period.get_name(), name]

class DtuTeacherStrategy(TeacherStrategy):
    @staticmethod
    def generate_data_object(time_period: TimePeriod, name: str) -> 'Composite':
        return School(name, Domain(DtuStrategyCollection()), time_period)

    @staticmethod
    def generate_children(time_period: TimePeriod, name: str) -> List[str]:
        return [time_period.get_name(), name]

class DtuStudyLineStrategy(StudyLineStrategy):
    @staticmethod
    def generate_data_object(time_period: TimePeriod, name: str) -> 'Composite':
        return School(name, Domain(DtuStrategyCollection()), time_period)

    @staticmethod
    def generate_children(time_period: TimePeriod, name: str) -> List[str]:
        return [time_period.get_name(), name]

class StrategyCollection(ABC):

    def __init__(self) -> None:
        self.switch_dct: Dict[str,Type[DataStrategy]] = self._initialize_switch_dct()

    def strategy_switch(self, class_id) -> Type[DataStrategy]:
        if class_id in self.switch_dct:
            return self.switch_dct[class_id]
        else:
            raise ValueError(f"Class id {class_id} does not exist in {self.__class__.__name__}")

    def _initialize_switch_dct(self) -> Dict[str,Type[DataStrategy]]:
        dct = {}
        dct[School.get_class_id()] = self.school_strategy()
        dct[Year.get_class_id()] = self.year_strategy()
        dct[Course.get_class_id()] = self.course_strategy()
        dct[Term.get_class_id()] = self.term_strategy()
        dct[Evaluation.get_class_id()] = self.evaluation_strategy()
        dct[GradeSheet.get_class_id()] = self.grade_sheet_strategy()
        dct[InfoPage.get_class_id()] = self.info_page_strategy()
        dct[Teacher.get_class_id()] = self.teacher_strategy()
        dct[StudyLine.get_class_id()] = self.study_line_strategy()
        return dct

    @abstractmethod
    def get_domain_name(self) -> str:
        pass

    @abstractmethod
    def get_time_manager(self) -> TimeManager:
        pass

    @abstractmethod
    def school_strategy(self) -> Type[DataStrategy]:
        return SchoolStrategy

    @abstractmethod
    def year_strategy(self) -> Type[DataStrategy]:
        return YearStrategy

    @abstractmethod
    def course_strategy(self) -> Type[DataStrategy]:
        return CourseStrategy

    @abstractmethod
    def term_strategy(self) -> Type[DataStrategy]:
        return TermStrategy

    @abstractmethod
    def evaluation_strategy(self) -> Type[DataStrategy]:
        return EvaluationStrategy

    @abstractmethod
    def grade_sheet_strategy(self) -> Type[DataStrategy]:
        return GradeSheetStrategy

    @abstractmethod
    def info_page_strategy(self) -> Type[DataStrategy]:
        return InfoPageStrategy

    @abstractmethod
    def study_line_strategy(self) -> Type[DataStrategy]:
        return StudyLineStrategy

    @abstractmethod
    def teacher_strategy(self) -> Type[DataStrategy]:
        return TeacherStrategy

class DtuStrategyCollection(StrategyCollection):

    DOMAIN_NAME: str = "dtu"

    def __init__(self) -> None:
        super().__init__()
        self.name: str = DtuStrategyCollection.DOMAIN_NAME
        self.time_manager: TimeManager = TimeManager(DtuTimeConfig)

    def get_domain_name(self) -> str:
        return self.name

    def get_time_manager(self) -> TimeManager:
        return self.time_manager

    def school_strategy(self) -> Type[DataStrategy]:
        return DtuSchoolStrategy

    def year_strategy(self) -> Type[DataStrategy]:
        return DtuYearStrategy

    def course_strategy(self) -> Type[DataStrategy]:
        return DtuCourseStrategy

    def term_strategy(self) -> Type[DataStrategy]:
        return DtuTermStrategy

    def evaluation_strategy(self) -> Type[DataStrategy]:
        return DtuEvaluationStrategy

    def grade_sheet_strategy(self) -> Type[DataStrategy]:
        return DtuGradeSheetStrategy

    def info_page_strategy(self) -> Type[DataStrategy]:
        return DtuInfoPageStrategy

    def study_line_strategy(self) -> Type[DataStrategy]:
        return DtuStudyLineStrategy

    def teacher_strategy(self) -> Type[DataStrategy]:
        return DtuTeacherStrategy

class Domain:

    def __init__(self, strategy_collection: StrategyCollection) -> None:
        self.strategy_collection: StrategyCollection = strategy_collection
        self.time_manager: TimeManager = self.strategy_collection.get_time_manager()
        self.name: str = self.strategy_collection.get_domain_name()

    def get_strategy(self, class_id: str) -> Type[DataStrategy]:
        return self.strategy_collection.strategy_switch(class_id)

    def get_strategy_collection(self) -> StrategyCollection:
        return self.strategy_collection

    def get_time_manager(self) -> TimeManager:
        return self.time_manager

    def get_name(self) -> str:
        return self.name

class DomainManager:

    STRATEGY_COLLECTIONS: List[StrategyCollection] = [
        DtuStrategyCollection()
    ]

    initialized_domains: Dict[str, Domain] = {}

    @staticmethod
    def read_domain_from_keyname(key_name: str) -> Domain:
        if key_name not in DomainManager.initialized_domains:
            raise KeyError(f"No domain with name '{key_name}' in domain dict")
        return DomainManager.initialized_domains[key_name]

    @staticmethod
    def get_all_domains() -> List[Domain]:
        if len(DomainManager.initialized_domains) == 0:
            DomainManager._initialize_domains()
        return list(DomainManager.initialized_domains.values())

    @staticmethod
    def _initialize_domains() -> None:
        for strategy_collection in DomainManager.STRATEGY_COLLECTIONS:
            dct_key = strategy_collection.get_domain_name()
            domain: Domain = Domain(strategy_collection)
            DomainManager.initialized_domains[dct_key] = domain


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
        domain: Domain = DomainManager.read_domain_from_keyname(data_list[0])
        time: TimePeriod = domain.get_time_manager().read_time_from_keyname(data_list[1])
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
        self._lists: Dict[str,List[str]] = {}

    def fabricate_object(self, key: str) -> 'Composite':
        if self._memory.exists(key):
            data_object: Composite = self._memory.get(key)
        else:
            domain: Domain = self.serializer.deserialize_domain(key)
            class_id: str = self.serializer.deserialize_class_id(key)
            strategy: Type[DataStrategy] = domain.get_strategy(class_id)
            time_period: TimePeriod = self.serializer.deserialize_time_period(key)
            name: str = self.serializer.deserialize_name(key)
            data_object = strategy.generate_data_object(time_period, name)
            self.register(key, data_object)
        return data_object

    def generate_list(self, key: str) -> List[str]:
        if key in self._lists:
            lst: List[str] = self._lists[key]
        else:
            domain: Domain = self.serializer.deserialize_domain(key)
            class_id: str = self.serializer.deserialize_class_id(key)
            strategy: Type[DataStrategy] = domain.get_strategy(class_id)
            time_period: TimePeriod = self.serializer.deserialize_time_period(key)
            name: str = self.serializer.deserialize_name(key)
            lst = strategy.generate_children(time_period, name)
            self._lists[key] = lst
        return lst



    def register(self, key: str, data_object: 'Composite') -> None:
        self._memory.set_unique_key(key, data_object)

    def serialize_data(self, data: Tuple[Domain,TimePeriod,str,str]):
        return self.serializer.serialize_data(data)

class Composite:

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

    def get_strategy(self) -> Type[DataStrategy]:
        return self.domain.get_strategy(self.class_id)

    @staticmethod
    @abstractmethod
    def get_class_id() -> str:
        pass

    @abstractmethod
    def perform_action(self, action: Callable[['Composite'], float]) -> float:
        pass

    @abstractmethod
    def cascade_build(self) -> None:
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

    def cascade_build(self) -> None:
        child_names: List[str] = self._get_children_to_be_created()
        for name in child_names:
            key: str = self.serialize(name)
            child: Composite = self.data_manager.fabricate_object(key)
            child.cascade_build()
            self._add_child(child)

    def _add_child(self, child: 'Composite') -> None:
        self.children.append(child)

    def _get_children(self) -> List['Composite']:
        return self.children

    def _get_children_to_be_created(self) -> List[str]:
        key: str = self.serialize(self.name)
        return self.data_manager.generate_list(key)

    @staticmethod
    @abstractmethod
    def get_class_id() -> str:
        pass


class EndPoint(Composite):
    def __init__(self, name: str, domain: Domain, time_period: TimePeriod) -> None:
        self.data_instance: Composite
        super().__init__(name, domain, time_period)

    def perform_action(self, action: Callable[[Composite], float]) -> float:
        data_instance: Composite = self._get_data_instance()
        average = action(data_instance)
        return average

    def cascade_build(self) -> None:
        name: str = self.get_name()
        key: str = self.serialize(name)
        self.data_instance = self.data_manager.fabricate_object(key)

    def _get_data_instance(self) -> Composite:
        return self.data_instance

    @staticmethod
    @abstractmethod
    def get_class_id() -> str:
        pass

class School(Container):

    CLASS_ID: str = "school"

    @staticmethod
    def get_class_id() -> str:
        return School.CLASS_ID

class Year(Container):

    CLASS_ID: str = "year"

    @staticmethod
    def get_class_id() -> str:
        return School.CLASS_ID

class Course(Container):

    CLASS_ID: str = "course"

    @staticmethod
    def get_class_id() -> str:
        return School.CLASS_ID

class Term(Container):

    CLASS_ID: str = "term"

    @staticmethod
    def get_class_id() -> str:
        return School.CLASS_ID

class Teacher(Container):

    CLASS_ID: str = "teacher"

    @staticmethod
    def get_class_id() -> str:
        return School.CLASS_ID

class StudyLine(Container):

    CLASS_ID: str = "study_line"

    @staticmethod
    def get_class_id() -> str:
        return School.CLASS_ID

class Evaluation(EndPoint):

    CLASS_ID: str = "evaluation"

    @staticmethod
    def get_class_id() -> str:
        return School.CLASS_ID
class GradeSheet(EndPoint):

    CLASS_ID: str = "grade_sheet"

    @staticmethod
    def get_class_id() -> str:
        return School.CLASS_ID
class InfoPage(EndPoint):

    CLASS_ID: str = "info_page"

    @staticmethod
    def get_class_id() -> str:
        return School.CLASS_ID

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
    domain_list: List[Domain] = DomainManager.get_all_domains()
    for domain in domain_list:
        time_manager: TimeManager = domain.get_time_manager()
        terms: List[TimePeriod] = time_manager.generate_all_time_periods()
        years: List[TimePeriod] = time_manager.generate_years()
        empty_time: TimePeriod = time_manager.generate_empty_time_period()


if __name__ == "__main__":
    main()