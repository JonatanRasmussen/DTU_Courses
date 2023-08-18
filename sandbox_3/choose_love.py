from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Type, Callable

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

class DataStrategy(ABC):
    @staticmethod
    def assign_data(time: str, name: str) -> Dict[str,str]:
        if time == name:
            return {}
        return {}

class DtuSchoolStrategy(DataStrategy):
    @staticmethod
    def assign_data(time: str, name: str) -> Dict[str,str]:
        if time == name:
            return {}
        return {}

class DtuYearStrategy(DataStrategy):
    @staticmethod
    def assign_data(time: str, name: str) -> Dict[str,str]:
        if time == name:
            return {}
        return {}

class DtuCourseStrategy(DataStrategy):
    @staticmethod
    def assign_data(time: str, name: str) -> Dict[str,str]:
        if time == name:
            return {}
        return {}

class DtuTermStrategy(DataStrategy):
    @staticmethod
    def assign_data(time: str, name: str) -> Dict[str,str]:
        if time == name:
            return {}
        return {}

class DtuEvaluationStrategy(DataStrategy):
    @staticmethod
    def assign_data(time: str, name: str) -> Dict[str,str]:
        if time == name:
            return {}
        return {}

class DtuGradeSheetStrategy(DataStrategy):
    @staticmethod
    def assign_data(time: str, name: str) -> Dict[str,str]:
        if time == name:
            return {}
        return {}

class DtuInfoPageStrategy(DataStrategy):
    @staticmethod
    def assign_data(time: str, name: str) -> Dict[str,str]:
        if time == name:
            return {}
        return {}

class DtuTeacherStrategy(DataStrategy):
    @staticmethod
    def assign_data(time: str, name: str) -> Dict[str,str]:
        if time == name:
            return {}
        return {}

class DtuStudyLineStrategy(DataStrategy):
    @staticmethod
    def assign_data(time: str, name: str) -> Dict[str,str]:
        if time == name:
            return {}
        return {}


class StrategyCollection(ABC):
    @abstractmethod
    def get_domain_name(self) -> str:
        pass
    @abstractmethod
    def get_time_manager(self) -> TimeManager:
        pass
    @abstractmethod
    def school_strategy(self) -> Type[DataStrategy]:
        pass
    @abstractmethod
    def year_strategy(self) -> Type[DataStrategy]:
        pass
    @abstractmethod
    def course_strategy(self) -> Type[DataStrategy]:
        pass
    @abstractmethod
    def term_strategy(self) -> Type[DataStrategy]:
        pass
    @abstractmethod
    def evaluation_strategy(self) -> Type[DataStrategy]:
        pass
    @abstractmethod
    def grade_sheet_strategy(self) -> Type[DataStrategy]:
        pass
    @abstractmethod
    def info_page_strategy(self) -> Type[DataStrategy]:
        pass
    @abstractmethod
    def study_line_strategy(self) -> Type[DataStrategy]:
        pass
    @abstractmethod
    def teacher_strategy(self) -> Type[DataStrategy]:
        pass

class DtuStrategyCollection(StrategyCollection):

    DOMAIN_NAME: str = "dtu"

    def __init__(self) -> None:
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

    def get_strategy_collection(self) -> StrategyCollection:
        return self.strategy_collection

    def get_time_manager(self) -> TimeManager:
        return self.time_manager

    def get_name(self) -> str:
        return self.name

    def get_time_unit(self, key: str) -> TimePeriod:
        print(key)
        return self.time_manager.generate_empty_time_period()

    def get_school_strategy(self) -> Type[DataStrategy]:
        return self.strategy_collection.school_strategy()
    def get_year_strategy(self) -> Type[DataStrategy]:
        return self.strategy_collection.year_strategy()
    def get_course_strategy(self) -> Type[DataStrategy]:
        return self.strategy_collection.course_strategy()
    def get_term_strategy(self) -> Type[DataStrategy]:
        return self.strategy_collection.term_strategy()
    def get_evaluation_strategy(self) -> Type[DataStrategy]:
        return self.strategy_collection.evaluation_strategy()
    def get_grade_sheet_strategy(self) -> Type[DataStrategy]:
        return self.strategy_collection.grade_sheet_strategy()
    def get_info_page_strategy(self) -> Type[DataStrategy]:
        return self.strategy_collection.info_page_strategy()
    def get_study_line_strategy(self) -> Type[DataStrategy]:
        return self.strategy_collection.study_line_strategy()
    def get_teacher_strategy(self) -> Type[DataStrategy]:
        return self.strategy_collection.teacher_strategy()

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
    def serialize_object(data_obj: 'DataPoint') -> str:
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

    DEFAULT_SERIALIZER: Serializer = Serializer()

    def __init__(self) -> None:
        self.serializer: Serializer = DataManager.DEFAULT_SERIALIZER
        self._class_table: Type[ClassTable] = ClassTable
        self._data_points: Dict[str, DataPoint] = {}
        self._child_lists: Dict[str,List[str]] = {}

    def cascade_build_children(self, data_obj: 'Container') -> None:
        child_classes: List[Type[DataPoint]] = data_obj.get_child_classes()
        for child_class in child_classes:
            strategy: Type[DataStrategy] = child_class.get_strategy(data_obj.domain)
            time: str = data_obj.time_period.get_name()
            name: str = data_obj.name
            data: Dict[str,str] = strategy.assign_data(time, name)
            time_period: TimePeriod = data_obj.domain.get_time_unit(child_class.get_class_id())
            if issubclass(child_class, Container):
                child_name = data["name"]
                child_dp: DataPoint = child_class(data_obj.domain, time_period, child_name)
                key: str = self.serialize(child_dp)
                if key in self._data_points:
                    child_dp = self._data_points[key]
                else:
                    data_obj.initialize_data(data)
                    self._register_data_point(key, child_dp)
            else:
                child_names = list(data.keys())
                for name in child_names:
                    child_c: Container = child_class(data_obj.domain, time_period, name)
                    data_obj.add_child(child_c)
                    self.cascade_build_children(child_c)
                key = self.serialize(child_c)
                if key in self._data_points:
                    child_c = self._data_points[key]
                else:
                    self._register_data_point(key, child_c)

    def _register_data_point(self, key: str, data_object: 'DataPoint') -> None:
        self._data_points[key] = data_object

    def _register_child_list(self, key: str, lst: List[str]) -> None:
        self._child_lists[key] = lst

    def serialize_data(self, data: Tuple[Domain,TimePeriod,str,str]):
        return self.serializer.serialize_object_data(data)

    def serialize(self, data_obj: 'DataPoint') -> str:
        return self.serializer.serialize_object(data_obj)


class DataPoint(ABC):

    def __init__(self, domain: Domain, time_period: TimePeriod, name: str) -> None:
        self.domain: Domain = domain
        self.time_period: TimePeriod = time_period
        self.class_id: str = self.get_class_id()
        self.name: str = name
        self.data: Dict[str,str] = {}

    def get_name(self) -> str:
        return self.name

    def initialize_data(self, data: Dict[str,str]) -> None:
        self.data = data

    @staticmethod
    @abstractmethod
    def get_strategy(domain: Domain) -> Type[DataStrategy]:
        pass

    @staticmethod
    @abstractmethod
    def get_class_id() -> str:
        pass


class Container(DataPoint):

    def __init__(self, domain: Domain, time_period: TimePeriod, name: str) -> None:
        super().__init__(domain, time_period, name)
        self.children: Dict[str,List[DataPoint]] = {}

    def cascade_perform_action(self, key: str, action: Callable[['DataPoint'], float]) -> float:
        if key in self.children:
            child_list: List[DataPoint] = self.children[key]
            if len(child_list) != 1:
                raise ValueError(f"There should be exactly 1 child in {self.time_period.get_name()} {self.name}, not {len(child_list)}")
            else:
                return action(child_list[0])
        elif len(self._get_main_children()) > 0:
            return self._perform_action_on_children(key, action)
        else:
            raise ValueError(f"Key {key} not found in {self.time_period.get_name()} {self.name}")

    def _perform_action_on_children(self, key: str, action: Callable[['DataPoint'], float]) -> float:
        child_sum: float = 0.0
        for child in self._get_main_children():
            child_sum += child.cascade_perform_action(key, action)
        return child_sum / len(self._get_main_children())

    def add_child(self, child: 'DataPoint') -> None:
        key: str = child.get_class_id()
        self.children[key].append(child)

    def _get_children(self, key) -> List['DataPoint']:
        return self.children[key]

    def _get_main_children(self) -> List['Container']:
        key: str = self.get_class_id()
        return self._get_children(key)

    @staticmethod
    @abstractmethod
    def get_child_classes() -> List[Type[DataPoint]]:
        pass

    @staticmethod
    @abstractmethod
    def get_main_child_classes() -> List['Container']:
        pass

class School(Container):

    CLASS_ID: str = "school"

    @staticmethod
    def get_class_id() -> str:
        return School.CLASS_ID

    @staticmethod
    def get_child_class() -> Type[Container]:
        return Year

    @staticmethod
    def get_strategy(domain: Domain) -> Type[DataStrategy]:
        return domain.get_school_strategy()

class Year(Container):

    CLASS_ID: str = "year"

    @staticmethod
    def get_class_id() -> str:
        return School.CLASS_ID

    @staticmethod
    def get_child_class() -> Type[Container]:
        return Course

    @staticmethod
    def get_strategy(domain: Domain) -> Type[DataStrategy]:
        return domain.get_year_strategy()

class Course(Container):

    CLASS_ID: str = "course"

    @staticmethod
    def get_class_id() -> str:
        return School.CLASS_ID

    @staticmethod
    def get_child_class() -> Type[Container]:
        return Term

    @staticmethod
    def get_strategy(domain: Domain) -> Type[DataStrategy]:
        return domain.get_course_strategy()

class Term(Container):

    CLASS_ID: str = "term"

    @staticmethod
    def get_class_id() -> str:
        return School.CLASS_ID

    @staticmethod
    def get_strategy(domain: Domain) -> Type[DataStrategy]:
        return domain.get_term_strategy()

class Teacher(Container):

    CLASS_ID: str = "teacher"

    @staticmethod
    def get_class_id() -> str:
        return School.CLASS_ID

    @staticmethod
    def get_child_class() -> Type[Container]:
        return Course

    @staticmethod
    def get_strategy(domain: Domain) -> Type[DataStrategy]:
        return domain.get_teacher_strategy()

class StudyLine(Container):

    CLASS_ID: str = "study_line"

    @staticmethod
    def get_class_id() -> str:
        return School.CLASS_ID

    @staticmethod
    def get_child_class() -> Type[Container]:
        return Course

    @staticmethod
    def get_strategy(domain: Domain) -> Type[DataStrategy]:
        return domain.get_study_line_strategy()

class Evaluation(DataPoint):

    CLASS_ID: str = "evaluation"

    @staticmethod
    def get_class_id() -> str:
        return School.CLASS_ID

    @staticmethod
    def get_strategy(domain: Domain) -> Type[DataStrategy]:
        return domain.get_evaluation_strategy()

class GradeSheet(DataPoint):

    CLASS_ID: str = "grade_sheet"

    @staticmethod
    def get_class_id() -> str:
        return School.CLASS_ID

    @staticmethod
    def get_strategy(domain: Domain) -> Type[DataStrategy]:
        return domain.get_grade_sheet_strategy()

class InfoPage(DataPoint):

    CLASS_ID: str = "info_page"

    @staticmethod
    def get_class_id() -> str:
        return School.CLASS_ID

    @staticmethod
    def get_strategy(domain: Domain) -> Type[DataStrategy]:
        return domain.get_info_page_strategy()

class ClassTable:

    @staticmethod
    def get_class_from_id(class_id: str) -> Type[DataPoint]:
        class_dct: Dict[str,Type[DataPoint]] = ClassTable._get_class_dct()
        if class_id in class_dct:
            return class_dct[class_id]
        else:
            raise ValueError(f"Class '{class_id}' not found in {__name__}")

    @staticmethod
    def _get_class_dct() -> Dict[str,Type[DataPoint]]:
        dct: Dict[str,Type[DataPoint]] = {
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
    domain_list: List[Domain] = DomainManager.get_all_domains()
    for domain in domain_list:
        time_manager: TimeManager = domain.get_time_manager()
        terms: List[TimePeriod] = time_manager.generate_all_time_periods()
        years: List[TimePeriod] = time_manager.generate_years()
        empty_time: TimePeriod = time_manager.generate_empty_time_period()
        print(terms)
        print(years)
        print(empty_time)

if __name__ == "__main__":
    main()