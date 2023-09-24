from orm_base import Base
from sqlalchemy import Column, Integer, UniqueConstraint, Identity
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from StudentMajor import StudentMajor
from datetime import datetime
from Enrollment import Enrollment


class Student(Base):
    __tablename__ = "students"
    studentID: Mapped[int] = mapped_column('student_id', Integer, Identity(start=1, cycle=True), primary_key=True)
    lastName: Mapped[str] = mapped_column('last_name', String(50), nullable=False, primary_key=False)
    firstName: Mapped[str] = mapped_column('first_name', String(50), nullable=False, primary_key=False)
    email: Mapped[str] = mapped_column('email', String(255), nullable=False)

    majors: Mapped[List["StudentMajor"]] = relationship(back_populates="student",
                                                        cascade="all, save-update, delete-orphan")
    sections: Mapped[List["Enrollment"]] = relationship(back_populates="student",
                                                        cascade="all, save-update, delete-orphan")
    __table_args__ = (UniqueConstraint("first_name", "last_name", name="students_uk_01"),
                      UniqueConstraint("email", name="students_uk_02"))

    def __init__(self, lastName: str, firstName: str, email: str):
        self.lastName = lastName
        self.firstName = firstName
        self.email = email

    def add_section(self, section):
        for next_section in self.sections:
            if next_section.section == section:
                return
        student_section = Enrollment(self, section)

    def remove_section(self, section):
        for next_section in self.sections:
            if next_section.section == section:
                self.sections.remove(next_section)
                return

    def add_major(self, major):
        for next_major in self.majors:
            if next_major.major == major:
                return
        student_major = StudentMajor(self, major, datetime.now())

    def remove_major(self, major):
        for next_major in self.majors:
            if next_major.major == major:
                self.majors.remove(next_major)
                return

    def __str__(self):
        return f"Student ID: {self.studentID} name: {self.lastName}, {self.firstName} e-mail: {self.email}"