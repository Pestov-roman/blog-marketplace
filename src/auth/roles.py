from enum import StrEnum


class Role(StrEnum):
    ADMIN = "admin"
    AUTHOR = "editor"
    READER = "reader"

    @classmethod
    def from_str(cls, value: str) -> "Role":
        return cls(value)

    def __str__(self) -> str:
        return self.value


ALL_ROLES = [Role.ADMIN, Role.AUTHOR, Role.READER]
