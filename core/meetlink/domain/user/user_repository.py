from typing import List, Protocol

from meetlink.models import Call, User


def get_user_by_email(email: str):
    return User.objects.get(email=email)


class IUserRepository(Protocol):
    def get(self, user_id: int) -> User | None:
        pass

    def get_all(self) -> List[User]:
        pass

    def create(self) -> User:
        pass

    def update(self, user_id: int, user: User) -> User:
        pass

    def delete(self, user_id: int) -> None:
        pass


class UserRepository(IUserRepository):
    def get(self, user_id: int) -> Call | None:
        pass

    def get_all(self) -> List[Call]:
        pass

    def create(self) -> Call:
        pass

    def update(self, user_id: int, call: Call) -> Call:
        pass

    def delete(self, user_id: int) -> None:
        pass
