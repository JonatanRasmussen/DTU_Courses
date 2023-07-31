# External modules
from typing import Dict, List
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup

# Custom imports
from web_scraping_tool import WebScrapingTool


#https://refactoring.guru/design-patterns/bridge

class Persistence:

    def data_exists():
        pass
    def cached_data_exists():
        pass

    def read_data():
        pass
    def write_data():
        pass

    def read_cache():
        pass
    def write_cache():
        pass


class DataAccess:
    def __init__(self, custom_object: 'DataContainer') -> None:
        self.retrieval_strategy: DataStrategy = custom_object.get_data_strategy()

    def access_data(self):
        if self.retrieval_strategy.data_exists(self.custom_object):
            return self.retrieval_strategy.read_data(self.custom_object)
        elif self.retrieval_strategy.cached_data_exists(self.custom_object):
            self.retrieval_strategy.set_unparsed_data(Persistence.read_cache(self.custom_object))
        else:
            self.retrieval_strategy.scrape_and_store_raw_data(self.custom_object)
        self.retrieval_strategy.parse_and_store_data_map(self.custom_object)
        return self.retrieval_strategy.get_parsed_data()


class DataStrategy(ABC):

    WEBDRIVER = WebScrapingTool()

    def __init__(self) -> None:
        self.scraped_data: str = ""
        self.parsed_data: dict[str:str] = {}
        self.deserialized_data: DataContainer = None
        self.scrape_key: str = self._generate_scrape_key()
        self.parse_key: str = self._generate_parse_key()
        self.deserialize_key: str = self._generate_deserialize_key()

    @abstractmethod
    def scrape_data(self) -> str:
        pass

    @abstractmethod
    def parse_data(self) -> dict[str:str]:
        pass

    @abstractmethod
    def deserialize_data(self) -> 'DataContainer':
        pass

    @abstractmethod
    def generate_data_key(self) -> 'str':
        pass

    def retrieve_data(self) -> 'DataContainer':
        return self.deserialized_data

    def scraped_data_exists(self) -> bool:
        return Persistence.exists_in_cache(self.scrape_key)
    def parsed_data_exists(self) -> bool:
        return Persistence.exists_in_database(self.parse_key)
    def deserialized_data_exists(self) -> bool:
        return Persistence.exists_in_memory(self.deserialize_key)

    def load_scraped_data(self) -> None:
        self.scraped_data = Persistence.read_from_cache(self.scrape_key)
    def load_parsed_data(self) -> None:
        self.parsed_data = Persistence.read_from_database(self.parse_key)
    def load_deserialized_data(self) -> None:
        self.deserialized_data = Persistence.read_from_memory(self.deserialize_key)

    def store_scraped_data(self) -> 'None':
        Persistence.write_to_cache(self.scraped_data, self.scrape_key)
    def store_parsed_data(self) -> None:
        Persistence.write_to_database(self.parsed_data, self.parse_key)
    def store_deserialized_data(self) -> None:
        Persistence.write_to_memory(self.deserialized_data, self.deserialize_key)

    def _generate_scrape_key(self) -> str:
        SCRAPE_IDENTIFIER: str = "raw"
        return f"{self.generate_data_key()}_{SCRAPE_IDENTIFIER}"

    def _generate_parse_key(self) -> str:
        PARSE_IDENTIFIER: str = "map"
        return f"{self.generate_data_key()}_{PARSE_IDENTIFIER}"

    def _generate_deserialize_key(self) -> str:
        DESERIALIZE_IDENTIFIER: str = "obj"
        return f"{self.generate_data_key()}_{DESERIALIZE_IDENTIFIER}"

class EvaluationStrategy(DataStrategy):

    @staticmethod
    def scrape_data(evaluation_object: 'Evaluation') -> str:
        course: str = evaluation_object.get_course().name()
        term: str = evaluation_object.get_term().name()
        return EvaluationStrategy.scrape_evaluation(course, term)

    @staticmethod
    def parse_data(unparsed_evaluation_str: str) -> dict[str:str]:
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
    def scrape_data(academic_year) -> str:
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
    def parse_data(page_source) -> any:
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
    def scrape_data() -> any:
        pass

    @staticmethod
    def parse_data() -> any:
        pass

class DtuGradeSheet(DataStrategy):

    @staticmethod
    def scrape_data() -> any:
        pass

    @staticmethod
    def parse_data() -> any:
        pass

class DtuInfoPage(DataStrategy):

    @staticmethod
    def scrape_data() -> any:
        pass

    @staticmethod
    def parse_data() -> any:
        pass

class DtuStudyLine(DataStrategy):

    @staticmethod
    def scrape_data() -> any:
        pass

    @staticmethod
    def parse_data() -> any:
        pass

class DtuTeacher(DataStrategy):

    @staticmethod
    def scrape_data() -> any:
        pass

    @staticmethod
    def parse_data() -> any:
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

class DataContainer(ABC):
    def __init__(self) -> None:
        self.data_strategy: DataStrategy = self.initialize_data_strategy()
        self.data_domain: DataDomain = None
        self.name: str = ""
        self.parent: any = None

    @abstractmethod
    def initialize_data_strategy(self) -> str:
        pass
    def get_data_strategy(self) -> str:
        self.data_strategy
    def set_data_strategy(self, data_strategy: DataStrategy) -> str:
        self.data_strategy = data_strategy

    def get_data_domain(self) -> DataDomain:
        return self.data_domain
    def set_data_domain(self, data_domain: DataDomain) -> None:
        self.data_domain = data_domain

    def get_name(self) -> str:
        return self.name
    def set_name(self, name: str) -> None:
        self.name = name

    def get_parent(self) -> any:
        return self.parent
    def set_parent(self, parent: any) -> None:
        self.parent = parent

    def retrieve_data(self):
        if self.data_strategy.data_exists(self):
            return self.data_strategy.read_data(self)
        elif self.data_strategy.cached_data_exists(self):
            self.data_strategy.set_unparsed_data(Persistence.read_cache(self))
        else:
            self.data_strategy.scrape_and_store_raw_data(self)
        self.data_strategy.parse_and_store_data_map(self)
        return self.data_strategy.get_parsed_data()

class School(DataContainer):
    def __init__(self) -> None:
        self.teachers: Dict[str, 'Teacher'] = {}
        self.years: Dict[str, 'Year'] = {}

    def get_name(self) -> str:
        return self.name
    def set_name(self, name: str) -> None:
        self.name = name

    def get_teachers(self) -> Dict[str, 'Teacher']:
        return self.teachers
    def set_teacher(self, name: str, teacher: 'Teacher') -> None:
        self.teachers[name] = teacher

    def get_all_years(self) -> Dict[str, 'Year']:
        return self.years
    def get_year(self, name: str) -> 'Year':
        return self.years[name]
    def set_year(self, name: str, year: 'Year') -> None:
        self.years[name] = year

    def get_all_courses(self,) -> Dict[str, 'Course']:
        return self.years
    def get_course(self, name: str) -> 'Course':
        return self.years[name]
    def set_course(self, name: str, course: 'Course') -> None:
        self.years[name] = course


class SchoolBuilder:
    def __init__(self):
        self.school: School = School()
        self.most_recent_built_year: Year = None
        self.most_recent_built_course: Course = None
        self.most_recent_built_term: CourseTerm = None
        self.build()

    def build(self) -> None:
        self.build_years()
        self.build_teachers()

    def generate_year_names() -> List[str]:
        pass

    def build_years(self) -> None:
        for name in self.generate_year_names():
            self.school.set_year(Year(name))
            self.most_recent_built_year = self.school.get_year(name)
            self.build_courses()
            self.build_study_lines()

    def fetch_course_names(year_name: str) -> List[str]:
        pass

    def build_courses(self) -> None:
        year: Year = self.most_recent_built_year
        for name in self.fetch_course_names(year):
            year.set_course(name, Course(name))
            self.most_recent_built_course = year.get_course(name)
            self.build_terms()
            self.build_info_page()

    def fetch_term_names() -> List[str]:
        pass

    def build_terms(self) -> None:
        course: Course = self.most_recent_built_course
        for name in self.course_term_names(course):
            course.set_term(name, CourseTerm(name))
            self.most_recent_built_term = course.get_term(name)
            self.build_evaluation()
            self.build_grade_sheet()

    def fetch_teachers():
        pass

    def build_teachers(self):
        for teacher in self.fetch_teachers():
            self.school.set_teacher(teacher.get_name(), teacher)

    def fetch_study_lines(year):
        pass

    def build_study_lines(self):
        year: Year = self.most_recent_built_year
        for study_line in self.fetch_study_lines():
            year.set_study_line(study_line.get_name(), study_line)

    def fetch_info_page(year, course):
        pass

    def build_info_page(self):
        year: Year = self.most_recent_built_year
        course: Course = self.most_recent_built_course
        info_page: InfoPage = self.fetch_info_page(year, course)
        course.set_info_page(info_page)
        pass

    def fetch_evaluation(year, course, term):
        pass

    def build_evaluation(self):
        year: Year = self.most_recent_built_year
        course: Course = self.most_recent_built_course
        term: CourseTerm = self.most_recent_built_term
        evaluation: Evaluation = self.fetch_evaluation(year, course, term)
        term.set_evaluation(evaluation)
        pass

    def fetch_grade_sheet(year, course, term):
        pass

    def build_grade_sheet(self):
        year: Year = self.most_recent_built_year
        course: Course = self.most_recent_built_course
        term: CourseTerm = self.most_recent_built_term
        grade_sheet: GradeSheet = self.fetch_grade_sheet(year, course, term)
        term.set_grade_sheet(grade_sheet)
        pass



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



class Year(DataContainer):
    def __init__(self) -> None:
        self.name: str = ""
        self.studylines: Dict[str, 'StudyLine'] = {}
        self.courses: Dict[str, 'Course'] = {}

    def get_school(self) -> School:
        return self.name

    def get_name(self) -> str:
        return self.name
    def set_name(self, name: str) -> None:
        self.name = name

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


class Course(DataContainer):
    def __init__(self) -> None:
        self.name: str = ""
        self.info_page: Dict[str, 'InfoPage'] = {}
        self.course_terms: Dict[str, 'CourseTerm'] = {}

    def get_name(self) -> str:
        return self.name
    def set_name(self, name: str) -> None:
        self.name = name

    def get_all_terms(self) -> Dict[str, 'CourseTerm']:
        return self.course_terms
    def get_term(self, name: str) -> 'CourseTerm':
        return self.course_terms[name]
    def set_term(self, name: str, course_term: 'CourseTerm') -> None:
        self.course_terms[name] = course_term

    def get_info_page(self) -> 'InfoPage':
        return self.info_page
    def set_info_page(self, info_page: 'InfoPage') -> None:
        self.info_page = info_page


class CourseTerm(DataContainer):
    def __init__(self) -> None:
        self.name: str = ""
        self.evaluation:'Evaluation' = None
        self.grade_sheet: 'GradeSheet' = None

    def get_name(self) -> str:
        return self.name
    def set_name(self, name: str) -> None:
        self.name = name

    def get_grade_sheet(self) -> 'GradeSheet':
        return self.grade_sheet
    def set_grade_sheet(self, grade_sheet: 'GradeSheet') -> None:
        self.grade_sheet = grade_sheet

    def get_evaluation(self) -> 'Evaluation':
        return self.evaluation
    def set_evaluation(self, evaluation: 'Evaluation') -> None:
        self.evaluation = evaluation


class Teacher(DataContainer):
    pass

class StudyLine(DataContainer):
    pass

class Evaluation(DataContainer):
    pass

class GradeSheet(DataContainer):
    pass

class InfoPage(DataContainer):
    pass