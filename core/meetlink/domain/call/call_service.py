from typing import Dict, List, Protocol

from django.utils import timezone
from meetlink.domain.call.call_exceptions import (
    CallIdNotPassedException,
    CallNotFoundException,
    EditCallFormException,
)
from meetlink.domain.call.call_repository import ICallRepository
from meetlink.domain.subject.subject_repository import ISubjectRepository
from meetlink.domain.user.user_exceptions import (
    InterpreterIdNotPassedException,
    InterpreterNotFoundException,
    InvalidUserRoleException,
    ManagerIdNotPassedException,
    ManagerNotFoundException,
)
from meetlink.domain.user.user_repository import IUserRepository
from meetlink.forms import EditCallForm
from meetlink.models import Call, Role


class ICallService(Protocol):
    def __init__(
        self, call_repository: ICallRepository, user_repository: IUserRepository
    ):
        pass

    def get(self, call_id: int) -> Call | None:
        pass

    def get_all(self, sort: Dict) -> List[Call]:
        pass

    def create(self) -> Call:
        pass

    def insert_manager(
        self, call_id: int | None, manager_id: int | None
    ) -> Call | None:
        pass

    def insert_interpreter(
        self, call_id: int | None, interpreter_id: int | None
    ) -> Call | None:
        pass

    def finish(self, call_id: int | None) -> Call | None:
        pass

    def update(self, call_id: int, new_call: EditCallForm) -> Call:
        pass

    def delete(self, call_id: int) -> None:
        pass


class CallService(ICallService):
    def __init__(
        self,
        call_repository: ICallRepository,
        user_repository: IUserRepository,
        subject_repository: ISubjectRepository,
    ):
        self.call_repository = call_repository
        self.user_repository = user_repository
        self.subject_repository = subject_repository

    def get(self, call_id):
        call = self.call_repository.get(call_id)

        if not call:
            raise CallNotFoundException()

        return call

    def get_all(self, sort={"created_at": "asc"}):
        order_by_str = ",".join(
            f"{'-' if direction == 'desc' else ''}{field}"
            for field, direction in sort.items()
        )

        return self.call_repository.get_all(order_by_str)

    def create(self):
        return self.call_repository.create()

    def insert_manager(self, call_id, manager_id):
        if not manager_id:
            raise ManagerIdNotPassedException()

        if not call_id:
            raise CallIdNotPassedException()

        manager = self.user_repository.get(manager_id)

        if not manager:
            raise ManagerNotFoundException()

        if manager.role not in (Role.SUPERADMIN, Role.MANAGER):
            raise InvalidUserRoleException(manager.first_name, manager.role)

        call = self.call_repository.get(call_id)

        if not call:
            raise CallNotFoundException()

        call.manager_entered_at = timezone.now()
        call.responsible = manager
        call.save()

        return call

    def insert_interpreter(self, call_id, interpreter_id):
        if not interpreter_id:
            raise InterpreterIdNotPassedException()

        if not call_id:
            raise CallIdNotPassedException()

        interpreter = self.user_repository.get(interpreter_id)

        if not interpreter:
            raise InterpreterNotFoundException()

        if interpreter.role not in (Role.SUPERADMIN, Role.interpreter):
            raise InvalidUserRoleException(interpreter.first_name, interpreter.role)

        call = self.call_repository.get(call_id)

        if not call:
            raise CallNotFoundException()

        call.interpreter_entered_at = timezone.now()
        call.interpreter = interpreter
        call.save()

        return call

    def finish(self, call_id):
        if not call_id:
            raise CallIdNotPassedException()

        call = self.call_repository.get(call_id)

        if not call:
            raise CallNotFoundException()

        if call.finished_at:
            return call

        call.finished_at = timezone.now()
        call.save()

        return call

    def update(self, call_id, new_call):
        if not new_call.is_valid():
            raise EditCallFormException(new_call.errors.__str__)

        cleaned_new_call = new_call.cleaned_data

        if not call_id:
            raise CallIdNotPassedException()

        old_call = self.call_repository.get(call_id)

        if not old_call:
            raise CallNotFoundException()

        if cleaned_new_call["description"]:
            old_call.description = cleaned_new_call["description"]

        if cleaned_new_call["subject"]:
            subject = self.subject_repository.get(cleaned_new_call["subject"])

            old_call.subject = subject

        self.call_repository.update(old_call)

        return old_call
