from typing import List, Protocol

from meetlink.exceptions.call_exceptions import CallNotFoundException
from meetlink.repositories.call_repository import ICallRepository
from meetlink.models import Call


class ICallService(Protocol) :
    def __init__(self, call_repository: ICallRepository):
        pass

    def get(self, call_id: int) -> Call | None :
        pass
    
    def get_all(self) -> List[Call] :
        pass
    
    def create(self) -> Call :
        pass

    def update(self, call_id: int, call: Call) -> Call :
        pass

    def delete(self, call_id: int) -> None :
        pass



class CallService(ICallService) :
    def __init__ (self, call_repository: ICallRepository) :
        self.call_repository = call_repository

    def get(self, call_id) :
        call = self.call_repository.get(call_id)

        if not call :
            raise CallNotFoundException()
        
        return call
    
    def create(self):
        return self.call_repository.create()