import pdfplumber
import re

def cgpa_calculator(filename, course_code=None, cgpa=None):
    course_name = re.compile(r'[A-z]{3}\d{3}')
    grade_expression = re.compile(r'[A-Z]{1}[+-]?')

    non_credit_courses = ['ENG091', 'MAT091', 'MAT092']

    course_and_grade = {}

    title = []
    sum_of_grade_earned = 0

    with pdfplumber.open(f'app/static/files/{filename}') as pdf:
        for page in pdf.pages:
            text = page.extract_text()

            for line in text.split('\n'):
                if course_name.match(line):
                    if line.split(' ')[0] not in non_credit_courses:
                        line_split = line.rsplit(' ', 1)[1]

                        if line.split(' ')[0] in course_and_grade:
                            print(line.split(' ')[0])
                            sum_of_grade_earned -= float(course_and_grade[line.split(' ')[0]])
                            course_and_grade[line.split(' ')[0]] = line.rsplit(' ', 1)[1]
                            sum_of_grade_earned += float(line.rsplit(' ', 1)[1])
                        else:
                            title.append(line.split(' ')[0])
                            course_and_grade[line.split(' ')[0]] = line.rsplit(' ', 1)[1]
                            sum_of_grade_earned += float(line.rsplit(' ', 1)[1])

                if course_code != None:
                    if course_code in course_and_grade:
                        print(course_code)
                        sum_of_grade_earned -= float(course_and_grade[course_code])
                        course_and_grade[course_code] = cgpa
                        sum_of_grade_earned += float(cgpa)

    number_of_attempted_courses = len(title)
    CGPA = sum_of_grade_earned/number_of_attempted_courses
    print(course_and_grade)
    print("%.2f" % CGPA)
    return "%.2f" % CGPA


    