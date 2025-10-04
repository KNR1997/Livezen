from enum import StrEnum


class UserRole(StrEnum):
    super_admin = "super_admin"
    admin = "admin"
    teacher = "teacher"
    student = "student"
