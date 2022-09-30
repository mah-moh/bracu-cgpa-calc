from fileinput import filename
import pdfplumber
import re

class calculator:

    def __init__(self):
        self.course_name_expression = re.compile(r'[A-z]{3}\d{3}')
        self.grade_expression = re.compile(r'[A-Z]{1}[+-]?')

        self.non_credit_courses = ['ENG091', 'MAT091', 'MAT092', 'PHY101']

        self.course_and_grade = {}
        self.sum_of_grade_earned = 0

    def caluculate_cgpa(self, course_and_grade, course_code=None, cgpa=None):
        print(course_code, cgpa)
        for key, value in course_and_grade.items():
            self.sum_of_grade_earned += float(value)

        if course_code in self.course_and_grade:
            self.sum_of_grade_earned -= float(self.course_and_grade[course_code])
            self.course_and_grade[course_code] = cgpa

        number_of_attempted_courses = len(course_and_grade)

        print(self.sum_of_grade_earned, number_of_attempted_courses)

        CGPA = self.sum_of_grade_earned/number_of_attempted_courses

        print(CGPA)
        CGPA = "%.2f" % CGPA
        return CGPA

    def pdfToText(self, filename):
        with pdfplumber.open(f'app/static/files/{filename}') as pdf:
            for page in pdf.pages:
                text = page.extract_text()

                for line in text.split('\n'):
                    if self.course_name_expression.match(line):
                        if line.split(' ')[0] not in self.non_credit_courses:
                            self.course_and_grade[line.split(' ')[0]] = line.rsplit(' ', 1)[1]

        result = self.caluculate_cgpa(self.course_and_grade)

        return result, self.course_and_grade

    def update(self, course_code, cgpa, course_and_grade=None):
        self.course_and_grade = course_and_grade

        result = self.caluculate_cgpa(self.course_and_grade, course_code, cgpa)

        return result, self.course_and_grade

