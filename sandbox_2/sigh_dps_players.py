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


    def read_from_cache(scrape_key: str) -> str | dict[str:str]:
        pass

    def read_from_database(parse_key: str | dict[str:str]) -> dict[str:str]:
        pass

    def read_from_memory(deserialize_key: str) -> 'BaseDataObject':
        pass


    def write_to_cache(scraped_data, scrape_key: str) -> None:
        pass

    def write_to_database(parsed_data, parse_key: str) -> None:
        pass

    def write_to_memory(deserialized_data, deserialize_key: str) -> None:
        pass


class DataStrategy(ABC):

    WEBDRIVER = WebScrapingTool()

    def __init__(self) -> None:
        self._scraped_data: str = ""
        self._parsed_data: str | dict[str:str] = {}
        self._deserialized_data: BaseDataObject | None = None
        self._scrape_key: str = self._generate_scrape_name()
        self._parse_key: str = self._generate_parse_name()
        self._deserialize_key: str = self._generate_deserialize_name()

    def get_deserialized_data(self) -> 'BaseDataObject':
        return self._deserialized_data
    def set_deserialized_data(self, data_object: 'BaseDataObject') -> None:
        self._deserialized_data = data_object

    def access_data(self):
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
    def _load_parsed_data(self) -> str | dict[str:str]:
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
    def _scrape_data(self) -> str | dict[str:str]:
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

class EvaluationStrategy(DataStrategy):

    @staticmethod
    def _scrape_data(evaluation_object: 'Evaluation') -> str:
        course: str = evaluation_object.get_course().name()
        term: str = evaluation_object.get_term().name()
        return EvaluationStrategy.scrape_evaluation(course, term)

    @staticmethod
    def _parse_data(unparsed_evaluation_str: str) -> dict[str:str]:
        pass

    @staticmethod
    @abstractmethod
    def scrape_evaluation() -> str:
        pass

    @staticmethod
    @abstractmethod
    def parse_evaluation() -> str:
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

class DtuEvaluation(DataStrategy):

    @staticmethod
    def _scrape_data() -> any:
        pass

    @staticmethod
    def _parse_data() -> any:
        pass

class DtuGradeSheet(DataStrategy):

    @staticmethod
    def _scrape_data() -> any:
        pass

    @staticmethod
    def _parse_data() -> any:
        pass

class DtuInfoPage(DataStrategy):

    @staticmethod
    def _scrape_data() -> any:
        pass

    @staticmethod
    def _parse_data() -> any:
        pass


class DtuStudyLine(DataStrategy):

    @staticmethod
    def _scrape_data() -> any:
        pass

    @staticmethod
    def _parse_data() -> any:
        pass

class DtuTeacher(DataStrategy):

    @staticmethod
    def _scrape_data() -> any:
        pass

    @staticmethod
    def _parse_data() -> any:
        pass

class DtuTerm(DataStrategy):

    @staticmethod
    def _scrape_data() -> any:
        pass

    @staticmethod
    def _parse_data() -> any:
        pass

class DtuYear(DataStrategy):

    @staticmethod
    def _scrape_data() -> any:
        pass

    @staticmethod
    def _parse_data() -> any:
        pass

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
        self.data_object: BaseDataObject

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
    def add_dictionary_element(self, outer_key: str, inner_key: str, element: BaseDataObject) -> None:
        self.data_container[outer_key][inner_key] = element

    def cascade_build(self):
        if not self._has_children():
            strategy: DataStrategy = self.data_domain.get_data_strategy()
            data_object: BaseDataObject = strategy.access_data(self)
            key: str = self.get_class_name()
            item = strategy._generate_data_name(self)
            self.add_dictionary_element(key, item, data_object)
        else:
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

    def _has_children(self) -> bool:
        if len(self.get_child_classes()) is not 0:
            return True
        return False

    @staticmethod
    @abstractmethod
    def get_child_classes() -> list[type['BaseDataObject']]:
        pass


class DataContainer(BaseDataObject):
    def __init__(self) -> None:
        super().__init__()
        self.data_object: BaseDataObject

    def cascade_build(self):
        strategy: DataStrategy = self.data_domain.get_data_strategy()
        data_object: BaseDataObject = strategy.access_data(self)
        key: str = self.get_class_name()
        item = strategy._generate_data_name(self)
        self.add_dictionary_element(key, item, data_object)


    @classmethod
    def cascade_build(cls, data_domain) -> 'School':
        school: School = cls()
        school.set_data_domain(data_domain)
        year_strategy: DataStrategy = school.data_domain.year_strategy()
        for year_name in year_strategy.access_data():
            year: Year = Year.cascade_build(year_name, school)
            school.set_year(year_name, year)
        for teacher_name in year_strategy.access_data():
            year: Year = Year.cascade_build(teacher_name, school)
            school.set_teacher(teacher_name, year)
        return school

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

class DataContainer:

    def __init__(self, parent_object: BaseDataObject, class_type: type['BaseDataObject']) -> None:
        self.parent_object: BaseDataObject = parent_object
        self.class_type: str = class_type
        self.container: Dict[str, BaseDataObject] = {}

    def get_full_dictionary(self, dct_key: str) -> Dict[str, BaseDataObject]:
        return self.container[dct_key]
    def get_dictionary_element(self, outer_key: str, inner_key: str) -> any:
        return self.container[outer_key][inner_key]

    def add_new_dictionary(self, dct_key: str) -> None:
        self.container[dct_key] = {}
    def add_dictionary_element(self, outer_key: str, inner_key: str, element: BaseDataObject) -> None:
        self.container[outer_key][inner_key] = element

class ContainerContainer:
    def __init__(self) -> None:
        self.unique_data: bool = False
        self.dictionaries: Dict[str, Dict[str, BaseDataObject]] = {}

    def get_full_dictionary(self, dct_key: str) -> Dict[str, BaseDataObject]:
        return self.dictionaries[dct_key]
    def get_dictionary_element(self, outer_key: str, inner_key: str) -> any:
        return self.dictionaries[outer_key][inner_key]

    def add_new_dictionary(self, dct_key: str) -> None:
        self.dictionaries[dct_key] = {}
    def add_dictionary_element(self, outer_key: str, inner_key: str, element: BaseDataObject) -> None:
        self.dictionaries[outer_key][inner_key] = element

    def build_container(self):
        strategy.get_child_containers()
        for child_strategy in strategy.get_child_data():
            for key in strategy.access_data():
                child_container = child_strategy.cascade_build(key, self)
                self.add_element(key, child_container)
        return

    def fill_dictionaries(self, data_domain) -> 'School':
        for dct in self.dictionaries:

        school: School = 12
        school.set_data_domain(data_domain)
        year_strategy: DataStrategy = school.data_domain.year_strategy()
        for year_name in year_strategy.access_data():
            year: Year = Year.cascade_build(year_name, school)
            school.set_year(year_name, year)
        for teacher_name in year_strategy.access_data():
            year: Year = Year.cascade_build(teacher_name, school)
            school.set_teacher(teacher_name, year)
        return school

class School(BaseDataObject):

    def __init__(self) -> None:
        super().__init__()
        self.years: Dict[str, 'Year'] = {}
        self.teachers: Dict[str, 'Teacher'] = {}

    @classmethod
    def cascade_build(cls, data_domain) -> 'School':
        school: School = cls()
        school.set_data_domain(data_domain)
        year_strategy: DataStrategy = school.data_domain.year_strategy()
        for year_name in year_strategy.access_data():
            year: Year = Year.cascade_build(year_name, school)
            school.set_year(year_name, year)
        for teacher_name in year_strategy.access_data():
            year: Year = Year.cascade_build(teacher_name, school)
            school.set_teacher(teacher_name, year)
        return school

    @staticmethod
    def get_child_classes() -> list[type['BaseDataObject']]:
        return [Year, Teacher]

    def initialize_data_strategy(self) -> DataStrategy:
        return None

    def get_contained_courses(self) -> any:
        pass

    def get_all_teachers(self) -> Dict[str, 'Teacher']:
        return self.teachers
    def get_teacher(self, name: str) -> 'Teacher':
        return self.teachers[name]
    def set_teacher(self, name: str, teacher: 'Teacher') -> None:
        self.teachers[name] = teacher

    def get_all_years(self) -> Dict[str, 'Year']:
        return self.years
    def get_year(self, name: str) -> 'Year':
        return self.years[name]
    def set_year(self, name: str, year: 'Year') -> None:
        self.years[name] = year


class SchoolBuilder:
    def __init__(self, school: School):
        self.school: School = school
        self.data_domain: DataDomain = self.school.get_data_domain()
        self.most_recent_built_year: Year = None
        self.most_recent_built_course: Course = None
        self.most_recent_built_term: Term = None
        self.build()

    def build(self) -> School:
        self.build_years()
        self.build_teachers()
        return self.school

    def build_years(self) -> None:
        year_strategy: DataStrategy = self.data_domain.year_strategy()
        for name in year_strategy.access_data():
            self.school.set_year(Year(name))
            self.most_recent_built_year = self.school.get_year(name)
            self.build_courses()
            self.build_study_lines()

    def build_courses(self) -> None:
        year: Year = self.most_recent_built_year
        course_strategy: DataStrategy = self.data_domain.course_strategy()
        for name in course_strategy.access_data(year):
            year.set_course(name, Course(name))
            self.most_recent_built_course = year.get_course(name)
            self.build_terms()
            self.build_info_page()

    def build_terms(self) -> None:
        course: Course = self.most_recent_built_course
        for name in self.data_domain.term_strategy(course):
            course.set_term(name, Term(name))
            self.most_recent_built_term = course.get_term(name)
            self.build_evaluation()
            self.build_grade_sheet()

    def build_teachers(self):
        for teacher in self.data_domain.teacher_strategy():
            self.school.set_teacher(teacher.get_name(), teacher)

    def build_study_lines(self):
        year: Year = self.most_recent_built_year
        for study_line in self.data_domain.study_line_strategy():
            year.set_study_line(study_line.get_name(), study_line)

    def build_info_page(self):
        year: Year = self.most_recent_built_year
        course: Course = self.most_recent_built_course
        info_page: InfoPage = self.data_domain.info_page_strategy(year, course)
        course.set_info_page(info_page)

    def build_evaluation(self):
        year: Year = self.most_recent_built_year
        course: Course = self.most_recent_built_course
        term: Term = self.most_recent_built_term
        evaluation: Evaluation = self.data_domain.evaluation_strategy(year, course, term)
        term.set_evaluation(evaluation)

    def build_grade_sheet(self):
        year: Year = self.most_recent_built_year
        course: Course = self.most_recent_built_course
        term: Term = self.most_recent_built_term
        grade_sheet: GradeSheet = self.data_domain.grade_sheet_strategy(year, course, term)
        term.set_grade_sheet(grade_sheet)



class Dtu(SchoolBuilder):
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

class Year(BaseDataObject):

    def __init__(self) -> None:
        super().__init__()
        self.studylines: Dict[str, 'StudyLine'] = {}
        self.courses: Dict[str, 'Course'] = {}

    @staticmethod
    def get_child_classes() -> list[type['BaseDataObject']]:
        return [Course, StudyLine]

    def get_all_studylines(self) -> Dict[str, 'StudyLine']:
        return self.studylines
    def get_studyline(self, name: str) -> 'StudyLine':
        return self.studylines[name]
    def set_studyline(self, name: str, studyline: 'StudyLine') -> None:
        self.studylines[name] = studyline

    def get_all_courses(self) -> Dict[str, 'Course']:
        return self.courses
    def get_course(self, name: str) -> 'Course':
        return self.courses[name]
    def set_course(self, name: str, course: 'Course') -> None:
        self.courses[name] = course


class Course(BaseDataObject):
    def __init__(self) -> None:
        super().__init__()
        self.info_page: Dict[str, 'InfoPage'] = {}
        self.course_terms: Dict[str, 'Term'] = {}

    @staticmethod
    def get_child_classes() -> list[type['BaseDataObject']]:
        return [Term, InfoPage]

    def get_all_terms(self) -> Dict[str, 'Term']:
        return self.course_terms
    def get_term(self, name: str) -> 'Term':
        return self.course_terms[name]
    def set_term(self, name: str, course_term: 'Term') -> None:
        self.course_terms[name] = course_term

    def get_info_page(self) -> 'InfoPage':
        return self.info_page
    def set_info_page(self, info_page: 'InfoPage') -> None:
        self.info_page = info_page


class Term(BaseDataObject):
    def __init__(self) -> None:
        super().__init__()
        self.evaluation:'Evaluation' = None
        self.grade_sheet: 'GradeSheet' = None

    @staticmethod
    def get_child_classes() -> list[type['BaseDataObject']]:
        return [Evaluation, GradeSheet]

    def get_grade_sheet(self) -> 'GradeSheet':
        return self.grade_sheet
    def set_grade_sheet(self, grade_sheet: 'GradeSheet') -> None:
        self.grade_sheet = grade_sheet

    def get_evaluation(self) -> 'Evaluation':
        return self.evaluation
    def set_evaluation(self, evaluation: 'Evaluation') -> None:
        self.evaluation = evaluation


class Teacher(BaseDataObject):
    pass

class StudyLine(BaseDataObject):
    pass

class Evaluation(BaseDataObject):
    pass

class GradeSheet(BaseDataObject):
    pass

class InfoPage(BaseDataObject):
    pass