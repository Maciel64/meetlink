from datetime import date
from typing import List, Protocol

from django.utils import timezone

from meetlink.domain.user.user_repository import IUserRepository
from meetlink.domain.user.user_exceptions import InvalidUserRoleException, ManagerIdNotPassedException, ManagerNotFoundException
from meetlink.domain.call.call_exceptions import CallIdNotPassedException, CallNotFoundException
from meetlink.domain.call.call_repository import ICallRepository
from meetlink.models import Call, Role


class ICallService(Protocol) :
    def __init__(self, call_repository: ICallRepository, user_repository: IUserRepository):
        pass

    def get(self, call_id: int) -> Call | None :
        pass
    
    def get_all(self) -> List[Call] :
        pass
    
    def create(self) -> Call :
        pass

    def insert_manager(self, call_id: int | None, manager_id: int | None) -> Call | None :
        pass

    def finish(self, call_id: int | None) -> Call | None :
        pass

    def update(self, call_id: int, new_call: Call) -> Call :
        pass

    def delete(self, call_id: int) -> None :
        pass



class CallService(ICallService) :
    def __init__ (self, call_repository: ICallRepository, user_repository: IUserRepository) :
        self.call_repository = call_repository
        self.user_repository = user_repository

    def get(self, call_id) :
        call = self.call_repository.get(call_id)

        if not call :
            raise CallNotFoundException()
        
        return call
    

    def create(self):
        return self.call_repository.create()


    def insert_manager(self, call_id, manager_id) :
        if not manager_id :
            raise ManagerIdNotPassedException()
        
        if not call_id :
            raise CallIdNotPassedException()
        
        manager = self.user_repository.get(manager_id)
        
        if not manager :
            raise ManagerNotFoundException()
        
        if manager.role in (Role.SUPERADMIN, Role.MANAGER) :
            raise InvalidUserRoleException(manager.first_name, manager.role)
        
        call = self.call_repository.get(call_id)

        if not call :
            raise CallNotFoundException()
        
        call.manager_entered_at = timezone.now()
        call.responsible = manager
        call.save()

        return call
    

    def finish(self, call_id) :
        if not call_id :
            raise CallIdNotPassedException()
        
        call = self.call_repository.get(call_id)

        if not call :
            raise CallNotFoundException()
        
        call.finished_at = timezone.now()
        call.save()

        return call
    
    
    def update(self, call_id, new_call):
        if not call_id :
            raise CallIdNotPassedException()
        
        old_call = self.call_repository.get(call_id)

        if not old_call :
            raise CallNotFoundException()
        
        if new_call.description :
            old_call.description = new_call.description

        if new_call.subject :
            old_call.subject = new_call.subject

        old_call.save()

        return old_call