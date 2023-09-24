from orm_base import Base
from sqlalchemy import Integer, UniqueConstraint, ForeignKeyConstraint
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from Department import Department
from typing import List


class Course(Base):
    __tablename__ = "courses"
    department_abbreviation: Mapped[str] = mapped_column('department_abbreviation',
                                                        primary_key=True)
    department: Mapped["Department"] = relationship(back_populates="courses")
    sections: Mapped[List["Section"]] = relationship(back_populates="course")

    courseNumber: Mapped[int] = mapped_column('course_number', Integer,
                                              nullable=False, primary_key=True)
    name: Mapped[str] = mapped_column('name', String(50), nullable=False)
    description: Mapped[str] = mapped_column('description', String(500), nullable=False)
    units: Mapped[int] = mapped_column('units', Integer, nullable=False)
    __table_args__ = (UniqueConstraint("department_abbreviation", "name", name="courses_uk_01"),
                      ForeignKeyConstraint([department_abbreviation],
                                           [Department.abbreviation]))

    def __init__(self, department: Department, courseNumber: int, name: str, description: str, units: int):
        self.set_department(department)
        self.courseNumber = courseNumber
        self.name = name
        self.description = description
        self.units = units

    def set_department(self, department: Department):
        self.department = department
        self.department_abbreviation = department.abbreviation

    def __str__(self):
        return f"Department abbrev: {self.department_abbreviation} number: {self.courseNumber} name: {self.name} units: {self.units}"