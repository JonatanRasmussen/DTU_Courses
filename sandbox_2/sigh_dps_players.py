# External modules
from typing import Dict, List
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup

# Custom imports
from web_scraping_tool import WebScrapingTool


#https://refactoring.guru/design-patterns/bridge

class Persistence:

    def exists_in_cache(scrape_key: str) -> bool:
        pass

    def exists_in_database(parse_key: str) -> bool:
        pass

    def exists_in_memory(deserialize_key: str) -> bool:
        pass


    def read_from_cache(scrape_key: str) -> str:
        pass

    def read_from_database(parse_key: str) -> dict[str:str]:
        pass

    def read_from_memory(deserialize_key: str) -> 'BaseDataObject':
        pass


    def write_to_cache(scrape_key: str, scraped_data: str) -> None:
        pass

    def write_to_database(parse_key: str, parsed_data: dict[str:str]) -> None:
        pass

    def write_to_memory(deserialize_key: str, deserialized_data: 'BaseDataObject') -> None:
        pass


class DataStrategy(ABC):

    WEBDRIVER = WebScrapingTool()

    def __init__(self) -> None:
        self._custom_object: BaseDataObject | None = None
        self._scraped_data: str = ""
        self._parsed_data: dict[str:str] = {}
        self._deserialized_data: BaseDataObject | None = None
        self._scrape_key: str = self._generate_scrape_name()
        self._parse_key: str = self._generate_parse_name()
        self._deserialize_key: str = self._generate_deserialize_name()

    def get_deserialized_data(self) -> 'BaseDataObject':
        return self._deserialized_data
    def set_deserialized_data(self, data_object: 'BaseDataObject') -> None:
        self._deserialized_data = data_object

    def access_data(self, custom_object: 'BaseDataObject'):
        self._custom_object = custom_object
        if self._deserialized_data_exists():
            self._deserialized_data = self._load_deserialized_data()
        elif self._parsed_data_exists():
            self._parsed_data = self._load_parsed_data()
            self._deserialized_data = self._deserialize_data()
        elif self._scraped_data_exists():
            self._scraped_data = self._load_scraped_data()
            self._parsed_data = self._parse_data()
            self._deserialized_data = self._deserialize_data()
        else:
            self._scraped_data = self._scrape_data()
            self._parsed_data = self._parse_data()
            self._deserialized_data = self._deserialize_data()
        self._store_data()
        return self.get_deserialized_data()

    def _store_data(self):
        if len(self._scraped_data) != 0:
            self._store_scraped_data()
        if len(self._parsed_data) != 0:
            self._store_parsed_data()
        if self._deserialized_data is not None:
            self._store_deserialized_data()

    def _scraped_data_exists(self) -> bool:
        return Persistence.exists_in_cache(self._scrape_key)
    def _parsed_data_exists(self) -> bool:
        return Persistence.exists_in_database(self._parse_key)
    def _deserialized_data_exists(self) -> bool:
        return Persistence.exists_in_memory(self._deserialize_key)

    def _load_scraped_data(self) -> str:
        return Persistence.read_from_cache(self._scrape_key)
    def _load_parsed_data(self) -> dict[str:str]:
        return Persistence.read_from_database(self._parse_key)
    def _load_deserialized_data(self) -> 'BaseDataObject' | None:
        return Persistence.read_from_memory(self._deserialize_key)

    def _store_scraped_data(self) -> None:
        Persistence.write_to_cache(self._scraped_data, self._scrape_key)
    def _store_parsed_data(self) -> None:
        Persistence.write_to_database(self._parsed_data, self._parse_key)
    def _store_deserialized_data(self) -> None:
        Persistence.write_to_memory(self._deserialized_data, self._deserialize_key)

    def _generate_scrape_name(self) -> str:
        SCRAPE_IDENTIFIER: str = "raw"
        return f"{self._generate_data_name()}_{SCRAPE_IDENTIFIER}"

    def _generate_parse_name(self) -> str:
        PARSE_IDENTIFIER: str = "map"
        return f"{self._generate_data_name()}_{PARSE_IDENTIFIER}"

    def _generate_deserialize_name(self) -> str:
        DESERIALIZE_IDENTIFIER: str = "obj"
        return f"{self._generate_data_name()}_{DESERIALIZE_IDENTIFIER}"

    @abstractmethod
    def _scrape_data(self) -> str:
        pass

    @abstractmethod
    def _parse_data(self) -> dict[str:str]:
        pass

    @abstractmethod
    def _deserialize_data(self) -> 'BaseDataObject':
        pass

    @abstractmethod
    def _generate_data_name(self) -> str:
        pass

    @abstractmethod
    def _returns_list(self) -> bool:
        pass

class CourseStrategy(DataStrategy):

    @staticmethod
    def _scrape_data(course_object: 'Course') -> str:
        year: str = course_object.get_year().name()
        return CourseStrategy.scrape_course(year)

    @staticmethod
    def _parse_data(scraped_data: str) -> dict[str:str]:
        return CourseStrategy.parse_course(scraped_data)

    @staticmethod
    @abstractmethod
    def scrape_course() -> str:
        pass

    @staticmethod
    @abstractmethod
    def parse_course() -> dict[str:str]:
        pass

class DtuCourses(DataStrategy):

    @staticmethod
    def _scrape_data(academic_year) -> str:
        """ Deterministically generate a list of urls that covers the
            full course archive for a given academic year. The course
            list is split across several urls, one per starting letter
            https://kurser.dtu.dk/archive/2022-2023/letter/A
            https://kurser.dtu.dk/archive/2022-2023/letter/B
            ...
            https://kurser.dtu.dk/archive/2022-2023/letter/Z.
            Obtained the complete list by accessing each letter """
        URL_HOSTNAME: str = "https://kurser.dtu.dk"
        ALPHABET: list[str] = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
                                'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                                'U', 'V', 'W', 'X', 'Y', 'Z', 'Æ', 'Ø', 'Å']
        concatenated_html: str = ""
        for char in ALPHABET:
            url_path: str = f'/archive/{academic_year}/letter/{char}'
            url = URL_HOSTNAME + url_path
            concatenated_html += DtuCourses.WEBDRIVER.get_page_source(url)
        return concatenated_html

    @staticmethod
    def _parse_data(page_source) -> any:
        soup = BeautifulSoup(page_source, 'html.parser')
        all_tables: any = soup.find_all('table', {'class': 'table'})
        dct: dict[str,str] = {}
        for table in all_tables:
            rows: any = table.find_all('tr')[1:]
            for row in rows:
                course_id: str = row.find('td').text
                course_name: str = row.find_all('td')[1].text
                if course_id in dct:
                    print(f"ID {course_id} {course_name} already exists in dct: {dct[course_id]}")
                dct[course_id] = course_name
        sorted_dct: dict[str,str] = {key: dct[key] for key in sorted(dct)}
        return sorted_dct

class EvaluationStrategy(DataStrategy):

    @staticmethod
    def _scrape_data(evaluation_object: 'Evaluation') -> str:
        year: str = evaluation_object.get_year().name()
        course: str = evaluation_object.get_course().name()
        term: str = evaluation_object.get_term().name()
        return EvaluationStrategy.scrape_evaluation(year, course, term)

    @staticmethod
    def _parse_data(scraped_data: str) -> dict[str:str]:
        return EvaluationStrategy.parse_evaluation(scraped_data)

    @staticmethod
    @abstractmethod
    def scrape_evaluation() -> str:
        pass

    @staticmethod
    @abstractmethod
    def parse_evaluation() -> dict[str:str]:
        pass

class DtuEvaluation(DataStrategy):

    @staticmethod
    def _scrape_data() -> any:
        pass

    @staticmethod
    def _parse_data() -> any:
        pass

class GradeSheetStrategy(DataStrategy):

    @staticmethod
    def _scrape_data(grade_sheet_object: 'GradeSheet') -> str:
        year: str = grade_sheet_object.get_year().name()
        course: str = grade_sheet_object.get_course().name()
        term: str = grade_sheet_object.get_term().name()
        return GradeSheetStrategy.scrape_grade_sheet(year, course, term)

    @staticmethod
    def _parse_data(scraped_data: str) -> dict[str:str]:
        return GradeSheetStrategy.parse_grade_sheet(scraped_data)

    @staticmethod
    @abstractmethod
    def scrape_grade_sheet() -> str:
        pass

    @staticmethod
    @abstractmethod
    def parse_grade_sheet() -> dict[str:str]:
        pass

class DtuGradeSheet(DataStrategy):

    @staticmethod
    def _scrape_data() -> any:
        pass

    @staticmethod
    def _parse_data() -> any:
        pass

class InfoPageStrategy(DataStrategy):

    @staticmethod
    def _scrape_data(info_page_object: 'InfoPage') -> str:
        year: str = info_page_object.get_year().name()
        course: str = info_page_object.get_course().name()
        return InfoPageStrategy.scrape_info_page(year, course)

    @staticmethod
    def _parse_data(scraped_data: str) -> dict[str:str]:
        return InfoPageStrategy.parse_info_page(scraped_data)

    @staticmethod
    @abstractmethod
    def scrape_info_page() -> str:
        pass

    @staticmethod
    @abstractmethod
    def parse_info_page() -> dict[str:str]:
        pass

class DtuInfoPage(DataStrategy):

    @staticmethod
    def _scrape_data() -> any:
        pass

    @staticmethod
    def _parse_data() -> any:
        pass

class StudyLineStrategy(DataStrategy):

    @staticmethod
    def _scrape_data(study_line_object: 'StudyLine') -> str:
        year: str = study_line_object.get_year().name()
        course: str = study_line_object.get_course().name()
        return StudyLineStrategy.scrape_study_line(year, course)

    @staticmethod
    def _parse_data(scraped_data: str) -> dict[str:str]:
        return StudyLineStrategy.parse_study_line(scraped_data)

    @staticmethod
    @abstractmethod
    def scrape_study_line() -> str:
        pass

    @staticmethod
    @abstractmethod
    def parse_study_line() -> dict[str:str]:
        pass

class DtuStudyLine(DataStrategy):

    @staticmethod
    def _scrape_data() -> any:
        pass

    @staticmethod
    def _parse_data() -> any:
        pass

class TeacherStrategy(DataStrategy):

    @staticmethod
    def _scrape_data(teacher_object: 'Teacher') -> str:
        year: str = teacher_object.get_year().name()
        return TeacherStrategy.scrape_teacher(year)

    @staticmethod
    def _parse_data(scraped_data: str) -> dict[str:str]:
        return TeacherStrategy.parse_teacher(scraped_data)

    @staticmethod
    @abstractmethod
    def scrape_teacher() -> str:
        pass

    @staticmethod
    @abstractmethod
    def parse_teacher() -> dict[str:str]:
        pass

class DtuTeacher(DataStrategy):

    @staticmethod
    def _scrape_data() -> any:
        pass

    @staticmethod
    def _parse_data() -> any:
        pass

class TermStrategy(DataStrategy):

    @staticmethod
    def _scrape_data(term_object: 'Term') -> str:
        year: str = term_object.get_year().name()
        course: str = term_object.get_course().name()
        return TermStrategy.scrape_term(year, course)

    @staticmethod
    def _parse_data(scraped_data: str) -> dict[str:str]:
        return TermStrategy.parse_term(scraped_data)

    @staticmethod
    @abstractmethod
    def scrape_term() -> str:
        pass

    @staticmethod
    @abstractmethod
    def parse_term() -> dict[str:str]:
        pass

class DtuTerm(DataStrategy):

    @staticmethod
    def _scrape_data() -> any:
        pass

    @staticmethod
    def _parse_data() -> any:
        pass

class YearStrategy(DataStrategy):

    @staticmethod
    def _scrape_data(year_object: 'Year') -> str:
        return YearStrategy.scrape_year()

    @staticmethod
    def _parse_data(scraped_data: str) -> dict[str:str]:
        return YearStrategy.parse_year(scraped_data)

    @staticmethod
    @abstractmethod
    def scrape_year() -> str:
        pass

    @staticmethod
    @abstractmethod
    def parse_year() -> dict[str:str]:
        pass

class DtuYear(DataStrategy):

    @staticmethod
    def _scrape_data() -> any:
        pass

    @staticmethod
    def _parse_data() -> any:
        pass

class DtuYears:
    def __init__(self, oldest_year: int, newest_year: int) -> None:
        self.oldest_year: int = oldest_year
        self.newest_year: int = newest_year

    @classmethod
    def predefined_year_interval(cls) -> None:
        oldest_year: int = 2017
        newest_year: int = 2023
        return cls(oldest_year, newest_year)

    def generate_year_names(self) -> List[str]:
        year_names: List[str] = []
        for year in range(self.oldest_year, self.newest_year):
            year_names.append(f"{str(year)}'-'{str(1+year)}")
        return year_names

class DataDomain(ABC):

    @staticmethod
    def get_data_retrieval_strategy(custom_object: any) -> DataStrategy:
        if isinstance(custom_object, 'Course'):
            return DataDomain.course_strategy()
        elif isinstance(custom_object, 'Evaluation'):
            return DataDomain.evaluation_strategy()
        elif isinstance(custom_object, 'GradeSheet'):
            return DataDomain.grade_sheet_strategy()
        elif isinstance(custom_object, 'InfoPage'):
            return DataDomain.info_page_strategy()
        elif isinstance(custom_object, 'StudyLine'):
            return DataDomain.study_line_strategy()
        elif isinstance(custom_object, 'Teacher'):
            return DataDomain.teacher_strategy()
        else:
            raise ValueError("Custom_object is of an unsupported type")

    @staticmethod
    @abstractmethod
    def get_domain_name(cls) -> str:
        return cls.__name__

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
    def year_strategy():
        pass


class DtuData(DataDomain):

    @staticmethod
    def course_strategy():
        return DtuCourses

    @staticmethod
    def evaluation_strategy():
        return DtuEvaluation

    @staticmethod
    def grade_sheet_strategy():
        return DtuGradeSheet

    @staticmethod
    def info_page_strategy():
        return DtuInfoPage

    @staticmethod
    def study_line_strategy():
        return DtuStudyLine

    @staticmethod
    def teacher_strategy():
        return DtuTeacher

    @staticmethod
    def term_strategy():
        return DtuTerm

    @staticmethod
    def year_strategy():
        return DtuYear


class BaseDataObject(ABC):

    def __init__(self) -> None:
        self.name: str = ""
        self.parent: BaseDataObject | None = None
        self.data_domain: DataDomain | None = None
        self.data_container: Dict[str, Dict[str, BaseDataObject]] = {}

    @staticmethod
    def get_child_classes() -> list[type['BaseDataObject']]:
        return []

    @staticmethod
    def get_data_strategy() -> DataStrategy | None:
        return None

    def get_class_name(self) -> str:
        return self.__class__.__name__

    def get_name(self) -> str:
        return self.name
    def set_name(self, name: str) -> None:
        self.name = name

    def get_parent(self) -> 'BaseDataObject':
        return self.parent
    def set_parent(self, parent: 'BaseDataObject') -> None:
        self.parent = parent

    def get_data_domain(self) -> DataDomain:
        return self.data_domain
    def set_data_domain(self, data_domain: DataDomain) -> None:
        self.data_domain = data_domain

    def get_full_dictionary(self, dct_key: str) -> Dict[str, 'BaseDataObject']:
        return self.data_container[dct_key]
    def get_dictionary_element(self, outer_key: str, inner_key: str) -> any:
        return self.data_container[outer_key][inner_key]

    def add_new_dictionary(self, dct_key: str) -> None:
        self.data_container[dct_key] = {}
    def add_dictionary_element(self, outer_key: str, inner_key: str, element: 'BaseDataObject') -> None:
        self.data_container[outer_key][inner_key] = element

    def cascade_build(self):
        if self._has_children():
            self._build_children()
        else:
            self._build_self()

    def _has_children(self) -> bool:
        if len(self.get_child_classes()) is not 0:
            return True
        return False

    def _build_children(self) -> None:
        for child_class in self.get_child_classes():
            key: str = child_class.get_class_name()
            self.add_new_dictionary(key)
            strategy: DataStrategy = child_class.data_domain.get_data_strategy()
            for item in strategy.access_data(self):
                child_object = child_class()
                child_object.name = item
                child_object.parent = self
                child_object.data_domain = self.data_domain
                child_object.cascade_build()
                self.add_dictionary_element(key, item, child_object)

    def _build_self(self) -> None:
        strategy: DataStrategy = self.data_domain.get_data_strategy()
        data_object: BaseDataObject = strategy.access_data(self)
        key: str = self.get_class_name()
        item = strategy._generate_data_name(self)
        self.add_dictionary_element(key, item, data_object)

    @staticmethod
    @abstractmethod
    def get_child_classes() -> list[type['BaseDataObject']]:
        pass

class School(BaseDataObject):

    @staticmethod
    def get_child_classes() -> list[type['BaseDataObject']]:
        return [Year, Teacher]

    def initialize_data_strategy(self) -> DataStrategy:
        return None

class Year(BaseDataObject):

    @staticmethod
    def get_child_classes() -> list[type['BaseDataObject']]:
        return [Course, StudyLine]

    def initialize_data_strategy(self) -> DataStrategy:
        #TODO
        return "TODO"

class Course(BaseDataObject):

    @staticmethod
    def get_child_classes() -> list[type['BaseDataObject']]:
        return [Term, InfoPage]

    def initialize_data_strategy(self) -> DataStrategy:
        #TODO
        return "TODO"

class Term(BaseDataObject):

    @staticmethod
    def get_child_classes() -> list[type['BaseDataObject']]:
        return [Evaluation, GradeSheet]

    def initialize_data_strategy(self) -> DataStrategy:
        #TODO
        return "TODO"


class Teacher(BaseDataObject):

    def initialize_data_strategy(self) -> DataStrategy:
        #TODO
        return "TODO"

class StudyLine(BaseDataObject):

    def initialize_data_strategy(self) -> DataStrategy:
        #TODO
        return "TODO"
class Evaluation(BaseDataObject):

    def initialize_data_strategy(self) -> DataStrategy:
        #TODO
        return "TODO"

class GradeSheet(BaseDataObject):

    def initialize_data_strategy(self) -> DataStrategy:
        #TODO
        return "TODO"

class InfoPage(BaseDataObject):

    def initialize_data_strategy(self) -> DataStrategy:
        #TODO
        return "TODO"