from persistence import Persistence
from html_parser import HtmlParser
from data_extractor import DataExtractor
from term import Term

terms = []
terms.append(Term.in_spring(2017))
terms.append(Term.in_autumn(2017))
terms.append(Term.in_spring(2018))
terms.append(Term.in_autumn(2018))
terms.append(Term.in_spring(2019))
terms.append(Term.in_autumn(2019))
terms.append(Term.in_spring(2020))
terms.append(Term.in_autumn(2020))
terms.append(Term.in_spring(2021))
terms.append(Term.in_autumn(2021))
terms.append(Term.in_spring(2022))
terms.append(Term.in_autumn(2022))
terms.append(Term.in_spring(2023))


engine = DataExtractor()
for term in terms:
    page_source = engine.access_course_archive(term)
    course_list = HtmlParser.parse_course_archive(page_source)
    dct_evaluations = {}
    dct_grades = {}
    dct_information = {}
    for course_id in course_list:
        dct_evaluations[course_id] = engine.access_evaluations(course_id, term)
        dct_grades[course_id] = engine.access_grades(course_id, term)
        dct_information[course_id] = engine.access_information(course_id, term)
    evaluations_filename = term.get_term_name()+'_evaluations'
    grades_filename = term.get_term_name()+'_grades'
    informations_filename = term.get_term_name()+'_information'
    Persistence.save_json(dct_evaluations, evaluations_filename)
    Persistence.save_json(dct_grades, grades_filename)
    Persistence.save_json(dct_information, informations_filename)
