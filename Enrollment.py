from orm_base import Base
from sqlalchemy import UniqueConstraint, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
# We canNOT import Student and Major here because Student and Major
# are both importing StudentMajor.  So we have to go without the
# ability to validate the Student or Major class references in
# this class.  Otherwise, we get a circular import.
# from Student import Student
# from Major import Major


class Enrollment(Base):
    """The association class between Student and Major.  I resorted to using
    this style of implementing a Many to Many because I feel that it is the
    most versatile approach, and we only have time for one Many to Many
    protocol in this class."""
    __tablename__ = "enrollments"
    section: Mapped["Section"] = relationship(back_populates="students")
    section_number: Mapped[int] = mapped_column('section_number', ForeignKey("sections.section_number"), primary_key=True)

    student: Mapped["Student"] = relationship(back_populates="sections")
    studentId: Mapped[int] = mapped_column('student_id', ForeignKey("students.student_id"), primary_key=True)

    def __init__(self, student, section):
        self.student = student
        self.student_id = student.studentID
        self.section = section
        self.section_number = section.section_number

    def __str__(self):
        return f"Student section - student: {self.student} section: {self.section}"
