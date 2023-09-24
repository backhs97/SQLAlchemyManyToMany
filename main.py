import logging
from pprint import pprint

from sqlalchemy import select

from menu_definitions import menu_main, add_menu, delete_menu, list_menu, debug_select
from db_connection import engine, Session
from orm_base import metadata
# Note that until you import your SQLAlchemy declarative classes, such as Student, Python
# will not execute that code, and SQLAlchemy will be unaware of the mapped table.
from Department import Department
from Course import Course
from Major import Major
from Student import Student
from StudentMajor import StudentMajor
from Section import Section
from Enrollment import Enrollment
from Option import Option
from Menu import Menu
from sqlalchemy import Time


def add(sess: Session):
    add_action: str = ''
    while add_action != add_menu.last_action():
        add_action = add_menu.menu_prompt()
        exec(add_action)


def delete(sess: Session):
    delete_action: str = ''
    while delete_action != delete_menu.last_action():
        delete_action = delete_menu.menu_prompt()
        exec(delete_action)


def list_objects(sess: Session):
    list_action: str = ''
    while list_action != list_menu.last_action():
        list_action = list_menu.menu_prompt()
        exec(list_action)


def add_department(session: Session):
    unique_name: bool = False
    unique_abbreviation: bool = False
    name: str = ''
    abbreviation: str = ''
    while not unique_abbreviation or not unique_name:
        name = input("Department full name--> ")
        abbreviation = input("Department abbreviation--> ")
        name_count: int = session.query(Department).filter(Department.name == name).count()
        unique_name = name_count == 0
        if not unique_name:
            print("We already have a department by that name.  Try again.")
        if unique_name:
            abbreviation_count = session.query(Department). \
                filter(Department.abbreviation == abbreviation).count()
            unique_abbreviation = abbreviation_count == 0
            if not unique_abbreviation:
                print("We already have a department with that abbreviation.  Try again.")
    new_department = Department(abbreviation, name)
    session.add(new_department)


def add_course(session: Session):
    print("Which department offers this course?")
    department: Department = select_department(sess)
    unique_number: bool = False
    unique_name: bool = False
    number: int = -1
    name: str = ''
    while not unique_number or not unique_name:
        name = input("Course full name--> ")
        number = int(input("Course number--> "))
        name_count: int = session.query(Course).filter(Course.department_abbreviation == department.abbreviation,
                                                       Course.name == name).count()
        unique_name = name_count == 0
        if not unique_name:
            print("We already have a course by that name in that department.  Try again.")
        if unique_name:
            number_count = session.query(Course). \
                filter(Course.department_abbreviation == department.abbreviation,
                       Course.courseNumber == number).count()
            unique_number = number_count == 0
            if not unique_number:
                print("We already have a course in this department with that number.  Try again.")
    description: str = input('Please enter the course description-->')
    units: int = int(input('How many units for this course-->'))
    course = Course(department, number, name, description, units)
    session.add(course)

def add_section(session: Session):
    print("Which course offers this section?")
    course: Course = select_course(sess)  # department abb, course #

    unique_location: bool = False  # year, semester, schedule, start time, building, room
    unique_professor: bool = False  # year, semester, schedule, start time, instructor

    section_number: int = -1
    semester: str = ''
    section_year: int = -1
    building: str = ''
    room: int = -1
    schedule: str = ''
    start_time: Time = None
    instructor: str = ''

    while not unique_location or not unique_professor:
        section_number = int(input("Section number--> "))
        semester = input("Semester full name--> ")
        while semester != "Fall" and semester != "Spring" and semester != "Winter" and semester != "Summer I" and semester != " Summer II":
            print("Invalid semester option. Try again.")
            semester = input("Semester full name--> ")

        section_year = int(input("Section year --> "))
        building = input("Section building--> ")
        room = int(input("Section room--> "))
        schedule = input("Section schedule--> ")
        while schedule != 'MW' and schedule != 'TuTh' and schedule != "MWF" and schedule != "F" and schedule != "S":
            print("Invalid schedule option. Try again.")
            schedule = input("Section schedule--> ")

        start_time = input("Section start time--> ")
        instructor = input("Section instructor--> ")

        unique_location_count: int = session.query(Section).filter(Section.section_year == section_year,
                                                                   Section.semester == semester,
                                                                   Section.schedule == schedule,
                                                                   Section.start_time == start_time,
                                                                   Section.building == building,
                                                                   Section.room == room).count()
        unique_location = unique_location_count == 0
        if not unique_location:
            print("We already have a section at that location.  Try again.")
        if unique_location:

            unique_professor_count: int = session.query(Section).filter(Section.section_year == section_year,
                                                                        Section.semester == semester,
                                                                        Section.schedule == schedule,
                                                                        Section.start_time == start_time,
                                                                        Section.instructor == instructor).count()
            unique_professor = unique_professor_count == 0
            if not unique_professor:
                print("An instructor is already teaching that section.  Try again.")

    section = Section(course, section_number, semester, section_year, building, room, schedule, start_time,
                      instructor)
    session.add(section)


def add_major(session: Session):
    print("Which department offers this major?")
    department: Department = select_department(sess)
    unique_name: bool = False
    name: str = ''
    while not unique_name:
        name = input("Major name--> ")
        name_count: int = session.query(Major).filter(Major.department_abbreviation == department.abbreviation,
                                                      ).count()
        unique_name = name_count == 0
        if not unique_name:
            print("We already have a major by that name in that department.  Try again.")
    description: str = input('Please give this major a description -->')
    major: Major = Major(department, name, description)
    session.add(major)


def add_student(session: Session):
    unique_name: bool = False
    unique_email: bool = False
    last_name: str = ''
    first_name: str = ''
    email: str = ''
    while not unique_email or not unique_name:
        last_name = input("Student last name--> ")
        first_name = input("Student first name-->")
        email = input("Student e-mail address--> ")
        name_count: int = session.query(Student).filter(Student.lastName == last_name,
                                                        Student.firstName == first_name).count()
        unique_name = name_count == 0
        if not unique_name:
            print("We already have a student by that name.  Try again.")
        if unique_name:
            email_count = session.query(Student).filter(Student.email == email).count()
            unique_email = email_count == 0
            if not unique_email:
                print("We already have a student with that email address.  Try again.")
    new_student = Student(last_name, first_name, email)
    session.add(new_student)


def add_student_major(sess):
    student: Student = select_student(sess)
    major: Major = select_major(sess)
    student_major_count: int = sess.query(StudentMajor).filter(StudentMajor.studentId == student.studentID,
                                                               StudentMajor.majorName == major.name).count()
    unique_student_major: bool = student_major_count == 0
    while not unique_student_major:
        print("That student already has that major.  Try again.")
        student = select_student(sess)
        major = select_major(sess)
    student.add_major(major)
    sess.add(student)
    sess.flush()


def add_major_student(sess):
    major: Major = select_major(sess)
    student: Student = select_student(sess)
    student_major_count: int = sess.query(StudentMajor).filter(StudentMajor.studentId == student.studentID,
                                                               StudentMajor.majorName == major.name).count()
    unique_student_major: bool = student_major_count == 0
    while not unique_student_major:
        print("That major already has that student.  Try again.")
        major = select_major(sess)
        student = select_student(sess)
    major.add_student(student)
    sess.add(major)
    sess.flush()


def select_section(sess: Session) -> Section:
    found: bool = False

    section_year: int = -1
    semester: str = ''
    schedule: str = ''
    start_time: str = ''
    instructor: str = ''

    while not found:
        section_year = int(input("Section Year--> "))
        semester = input("Semester--> ")
        schedule = input("Schedule--> ")
        start_time = input("Start Time--> ")
        instructor = input("Instructor--> ")

        professor_count: int = sess.query(Section).filter(Section.section_year == section_year,
                                                          Section.semester == semester, Section.schedule == schedule,
                                                          Section.start_time == start_time,
                                                          Section.instructor == instructor).count()
        found = professor_count == 1
        if not found:
            print("No section with that professor in that course.  Try again.")
    section = sess.query(Section).filter(Section.section_year == section_year, Section.semester == semester,
                                         Section.schedule == schedule, Section.start_time == start_time,
                                         Section.instructor == instructor).first()
    return section


def add_student_section(sess):
    student: Student = select_student(sess)
    section: Section = select_section(sess)
    student_section_count: int = sess.query(Enrollment).filter(Enrollment.studentId == student.studentID,
                                                               Enrollment.section_number == section.section_number).count()
    unique_student_section: bool = student_section_count == 0
    while not unique_student_section:
        print("That student already has that section.  Try again.")
        student = select_student(sess)
        section = select_section(sess)
    student.add_section(section)
    sess.add(student)
    sess.flush()


def add_section_student(sess):
    section: Section = select_section(sess)
    student: Student = select_student(sess)
    student_section_count: int = sess.query(Enrollment).filter(Enrollment.studentId == student.studentID,
                                                               Enrollment.section_number == section.section_number).count()
    unique_student_section: bool = student_section_count == 0
    while not unique_student_section:
        print("That section already has that student.  Try again.")
        section = select_section(sess)
        student = select_student(sess)
    section.add_student(student)
    sess.add(section)
    sess.flush()


def delete_student_section(sess):
    print("Prompting you for the student and the section that they no longer have.")
    student: Student = select_student(sess)
    section: Section = select_section(sess)
    student.remove_section(section)


def delete_section_student(sess):
    print("Prompting you for the section and the student who no longer has that section.")
    section: Section = select_section(sess)
    student: Student = select_student(sess)
    section.remove_student(student)


def select_department(sess: Session) -> Department:
    found: bool = False
    abbreviation: str = ''
    while not found:
        abbreviation = input("Enter the department abbreviation--> ")
        abbreviation_count: int = sess.query(Department). \
            filter(Department.abbreviation == abbreviation).count()
        found = abbreviation_count == 1
        if not found:
            print("No department with that abbreviation.  Try again.")
    return_department: Department = sess.query(Department). \
        filter(Department.abbreviation == abbreviation).first()
    return return_department


def select_course(sess: Session) -> Course:
    found: bool = False
    department_abbreviation: str = ''
    course_number: int = -1
    while not found:
        department_abbreviation = input("Department abbreviation--> ")
        course_number = int(input("Course Number--> "))
        name_count: int = sess.query(Course).filter(Course.department_abbreviation == department_abbreviation,
                                                    Course.courseNumber == course_number).count()
        found = name_count == 1
        if not found:
            print("No course by that number in that department.  Try again.")
    course = sess.query(Course).filter(Course.department_abbreviation == department_abbreviation,
                                       Course.courseNumber == course_number).first()
    return course


def select_student(sess) -> Student:
    found: bool = False
    last_name: str = ''
    first_name: str = ''
    while not found:
        last_name = input("Student's last name--> ")
        first_name = input("Student's first name--> ")
        name_count: int = sess.query(Student).filter(Student.lastName == last_name,
                                                     Student.firstName == first_name).count()
        found = name_count == 1
        if not found:
            print("No student found by that name.  Try again.")
    student: Student = sess.query(Student).filter(Student.lastName == last_name,
                                                  Student.firstName == first_name).first()
    return student


def select_major(sess) -> Major:
    found: bool = False
    name: str = ''
    while not found:
        name = input("Major's name--> ")
        name_count: int = sess.query(Major).filter(Major.name == name).count()
        found = name_count == 1
        if not found:
            print("No major found by that name.  Try again.")
    major: Major = sess.query(Major).filter(Major.name == name).first()
    return major


def delete_department(session: Session):
    print("deleting a department")
    department = select_department(session)
    n_courses = session.query(Course).filter(Course.department_abbreviation == department.abbreviation).count()
    if n_courses > 0:
        print(f"Sorry, there are {n_courses} courses in that department.  Delete them first, "
              "then come back here to delete the department.")
    else:
        session.delete(department)


def delete_student_major(sess):
    print("Prompting you for the student and the major that they no longer have.")
    student: Student = select_student(sess)
    major: Major = select_major(sess)
    student.remove_major(major)


def delete_major_student(sess):
    print("Prompting you for the major and the student who no longer has that major.")
    major: Major = select_major(sess)
    student: Student = select_student(sess)
    major.remove_student(student)


def list_courses_sections(sess):
    course = select_course(sess)
    cou_sections: [Section] = course.get_sections()
    print("Sections for course: " + str(course))
    for cou_section in cou_sections:
        print(cou_section)


def list_student_section(sess: Session):
    student: Student = select_student(sess)
    recs = sess.query(Student).join(Enrollment, Student.studentID == Enrollment.studentId).join(
        Section, Enrollment.section_number == Section.section_number).filter(
        Student.studentID == student.studentID).add_columns(
        Student.lastName, Student.firstName, Section.department_abbreviation, Section.courseNumber,
        Section.section_number, Section.building, Section.room, Section.instructor).all()
    for stu in recs:
        print(
            f"Student name: {stu.lastName}, {stu.firstName}, Department abbreviation: {stu.department_abbreviation}, Course number: {stu.courseNumber}, Section: {stu.section_number}, Location: {stu.building}-{stu.room}, Instructor: {stu.instructor}")


def list_section_student(sess: Session):
    section: Section = select_section(sess)
    recs = sess.query(Section).join(Enrollment, Enrollment.section_number == Section.section_number).join(
        Student, Enrollment.studentId == Student.studentID).filter(
        Section.section_number == section.section_number).add_columns(
        Student.lastName, Student.firstName, Section.department_abbreviation, Section.courseNumber,
        Section.section_number, Section.building, Section.room, Section.instructor).all()
    for stu in recs:
        print(
            f"Student name: {stu.lastName}, {stu.firstName}, Department abbreviation: {stu.department_abbreviation}, Course number: {stu.courseNumber}, Section: {stu.section_number}, Location: {stu.building}-{stu.room}, Instructor: {stu.instructor}")


def delete_course(session: Session):
    print("deleting a course")
    course = select_course(session)
    n_sections = session.query(Section).filter(Section.courseNumber == course.courseNumber).count()
    if n_sections > 0:
        print(f"Sorry, there are {n_sections} sections in that course.  Delete them first, "
              "then come back here to delete the course.")
    else:
        session.delete(course)


def delete_major(session: Session):
    print("deleting a major")
    major = select_major(session)
    n_student_major = session.query(StudentMajor).filter(StudentMajor.majorName == major.name).count()
    if n_student_major > 0:
        print(f"Sorry, there are {n_student_major} students in that major.  Delete them first, "
              "then come back here to delete the major.")
    else:
        session.delete(major)


def delete_section(session: Session):
    print("deleting a section")
    section = select_section(session)
    n_enrollments = session.query(Enrollment).filter(Enrollment.section_number == section.section_number).count()
    if n_enrollments > 0:
        print(f"Sorry, there are {n_enrollments} enrollments in that section.  Delete them first, "
              "then come back here to delete the section.")
    else:
        print("deleting a section")
        session.delete(section)


def delete_student(session: Session):
    print("deleting a student")
    student = select_student(session)
    n_enrollments = session.query(Enrollment).filter(Enrollment.studentId == student.studentID).count()
    if n_enrollments > 0:
        print(f"Sorry, the student is enrolled in {n_enrollments} sections.  Delete them first, "
              "then come back here to delete the student.")
    else:
        print("deleting a student")
        session.delete(student)


def list_department(session: Session):
    departments: [Department] = list(session.query(Department).order_by(Department.abbreviation))
    for department in departments:
        print(department)


def list_course(sess: Session):
    courses: [Course] = list(sess.query(Course).order_by(Course.courseNumber))
    for course in courses:
        print(course)


def list_student(sess: Session):
    students: [Student] = list(sess.query(Student).order_by(Student.lastName, Student.firstName))
    for student in students:
        print(student)


def list_major(sess: Session):
    majors: [Major] = list(sess.query(Major).order_by(Major.department_abbreviation))
    for major in majors:
        print(major)


def list_section(sess: Session):
    sections: [Section] = list(sess.query(Section).order_by(Section.department_abbreviation))
    for section in sections:
        print(section)


def list_student_major(sess: Session):
    student: Student = select_student(sess)
    recs = sess.query(Student).join(StudentMajor, Student.studentID == StudentMajor.studentId).join(
        Major, StudentMajor.majorName == Major.name).filter(
        Student.studentID == student.studentID).add_columns(
        Student.lastName, Student.firstName, Major.description, Major.name).all()
    for stu in recs:
        print(f"Student name: {stu.lastName}, {stu.firstName}, Major: {stu.name}, Description: {stu.description}")


def list_major_student(sess: Session):
    major: Major = select_major(sess)
    recs = sess.query(Major).join(StudentMajor, StudentMajor.majorName == Major.name).join(
        Student, StudentMajor.studentId == Student.studentID).filter(
        Major.name == major.name).add_columns(
        Student.lastName, Student.firstName, Major.description, Major.name).all()
    for stu in recs:
        print(f"Student name: {stu.lastName}, {stu.firstName}, Major: {stu.name}, Description: {stu.description}")


def move_course_to_new_department(sess: Session):
    print("Input the course to move to a new department.")
    course = select_course(sess)
    old_department = course.department
    print("Input the department to move that course to.")
    new_department = select_department(sess)
    if new_department == old_department:
        print("Error, you're not moving to a different department.")
    else:
        name_count: int = sess.query(Course).filter(Course.department_abbreviation == new_department.abbreviation,
                                                    Course.name == course.name).count()
        unique_name = name_count == 0
        if not unique_name:
            print("We already have a course by that name in that department.  Try again.")
        if unique_name:
            number_count = sess.query(Course). \
                filter(Course.department_abbreviation == new_department.abbreviation,
                       Course.courseNumber == course.courseNumber).count()
            if number_count != 0:
                print("We already have a course by that number in that department.  Try again.")
            else:
                course.set_department(new_department)


def select_student_from_list(session):
    students: [Department] = list(sess.query(Department).order_by(Department.lastName, Department.firstName))
    options: [Option] = []
    for student in students:
        options.append(Option(student.lastName + ', ' + student.firstName, student.studentId))
    temp_menu = Menu('Student list', 'Select a student from this list', options)
    text_studentId: str = temp_menu.menu_prompt()
    returned_student = sess.query(Department).filter(Department.studentId == int(text_studentId)).first()
    print("Selected student: ", returned_student)


def list_department_courses(sess):
    department = select_department(sess)
    dept_courses: [Course] = department.get_courses()
    print("Course for department: " + str(department))
    for dept_course in dept_courses:
        print(dept_course)


def boilerplate(sess):
    department: Department = Department('CECS', 'Computer Engineering Computer Science')
    major1: Major = Major(department, 'Computer Science', 'Fun with blinking lights')
    major2: Major = Major(department, 'Computer Engineering', 'Much closer to the silicon')
    course: Course = Course(department, '323', 'Database', 'sql', '3')
    section1: Section = Section(course, '1', 'Spring', '2023', 'ECS', '105', 'MW', '12:00', 'Brown')
    section2: Section = Section(course, '2', 'Spring', '2023', 'ECS', '106', 'MW', '11:00', 'Brown')
    student1: Student = Student('Brown', 'David', 'david.brown@gmail.com')
    student2: Student = Student('Brown', 'Mary', 'marydenni.brown@gmail.com')
    student3: Student = Student('Disposable', 'Bandit', 'disposable.bandit@gmail.com')
    student1.add_major(major1)
    student2.add_major(major1)
    student2.add_major(major2)
    student1.add_section(section1)
    student2.add_section(section2)
    student3.add_section(section2)
    sess.add(department)
    sess.add(course)
    sess.add(section1)
    sess.add(section2)
    sess.add(major1)
    sess.add(major2)
    sess.add(student1)
    sess.add(student2)
    sess.add(student3)

    sess.flush()


def session_rollback(sess):
    confirm_menu = Menu('main', 'Please select one of the following options:', [
        Option("Yes, I really want to roll back this session", "sess.rollback()"),
        Option("No, I hit this option by mistake", "pass")
    ])
    exec(confirm_menu.menu_prompt())


if __name__ == '__main__':
    # print('Starting off')
    # logging.basicConfig()
    # logging_action = debug_select.menu_prompt()
    # logging.getLogger("sqlalchemy.engine").setLevel(eval(logging_action))
    # logging.getLogger("sqlalchemy.pool").setLevel(eval(logging_action))
    metadata.drop_all(bind=engine)
    metadata.create_all(bind=engine)

    with Session() as sess:
        main_action: str = ''
        while main_action != menu_main.last_action():
            main_action = menu_main.menu_prompt()
            print('next action: ', main_action)
            exec(main_action)
        sess.commit()
    print('Ending normally')