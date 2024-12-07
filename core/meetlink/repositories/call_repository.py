from typing import List, Protocol

from meetlink.models import Call


class ICallRepository(Protocol) :
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


class CallRepository(ICallRepository) :
    def get(self, call_id) :
        try :
            return Call.objects.get(id=call_id)
        
        except Call.DoesNotExist :
            return None
        
    def get_all(self):
        return Call.objects.all()
    

    def create(self):
        return Call.objects.create()

    def update(self, call_id, call) :
        pass

    def delete(self, call_id) :
        pass
    
