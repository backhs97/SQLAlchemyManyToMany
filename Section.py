from orm_base import Base
from sqlalchemy import Integer, UniqueConstraint, ForeignKey, ForeignKeyConstraint, Identity
from sqlalchemy import String, Integer, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship
from Course import Course
from Department import Department
from typing import List
from Enrollment import Enrollment


class Section(Base):
    __tablename__ = "sections"
    section_number: Mapped[int] = mapped_column('section_number', Integer, Identity(start=1, cycle=True),
                                                primary_key=True, nullable=False)

    department_abbreviation: Mapped[str] = mapped_column('department_abbreviation', String(10))
    courseNumber: Mapped[int] = mapped_column('course_number', nullable=False)

    course: Mapped["Course"] = relationship("Course", back_populates="sections")
    students: Mapped[List["Enrollment"]] = relationship(back_populates="section",
                                                        cascade="all, save-update, delete-orphan")

    semester: Mapped[str] = mapped_column('semester', String(10), nullable=False)
    section_year: Mapped[int] = mapped_column('section_year', Integer, nullable=False)
    building: Mapped[str] = mapped_column('building', String(6), nullable=False)
    room: Mapped[int] = mapped_column('room', Integer, nullable=False)
    schedule: Mapped[str] = mapped_column('schedule', String(6), nullable=False)
    start_time: Mapped[Time] = mapped_column('start_time', Time, nullable=False)
    instructor: Mapped[str] = mapped_column('instructor', String(80), nullable=False)

    __table_args__ = (
    UniqueConstraint("section_year", "semester", "schedule", "start_time", "building", "room", name="sections_uk_01"),
    UniqueConstraint("section_year", "semester", "schedule", "start_time", "instructor", name="sections_uk_02"),
    UniqueConstraint("department_abbreviation", "course_number", "section_number", "section_year", "semester",
                     name="sections_uk_03"),
    ForeignKeyConstraint([department_abbreviation, courseNumber], [Course.department_abbreviation, Course.courseNumber]))

    def __init__(self, course: Course, sectionNumber: int, semester: str, section_year: int, building: str, room: int,
                 schedule: str, start_time: Time, instructor: str):
        self.set_course(course)
        self.sectionNumber = sectionNumber
        self.semester = semester
        self.section_year = section_year
        self.building = building
        self.room = room
        self.schedule = schedule
        self.start_time = start_time
        self.instructor = instructor

    def add_student(self, student):
        for next_student in self.students:
            if next_student.student == student:
                return
        student_section = Enrollment(student, self)

    def remove_student(self, student):
        for next_student in self.students:
            if next_student.student == student:
                self.students.remove(next_student)
                return

    def set_course(self, course: Course):
        self.course = course
        self.department_abbreviation = course.department_abbreviation
        self.courseNumber = course.courseNumber

    def __str__(self):
        return f"Department abbreviation: {self.department_abbreviation}\nCourse Number: {self.courseNumber}" \
               f"\nSection Number: {self.section_number}\nSemester: {self.semester}\nSection Year: {self.section_year}" \
               f"\nBuilding: {self.building}\nRoom: {self.room}\nSchedule: {self.schedule}" \
               f"\nStart Time: {self.start_time}\nInstructor: {self.instructor}"