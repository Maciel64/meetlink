from typing import List, Protocol

from meetlink.models import Call


class ICallRepository(Protocol):
    def get(self, call_id: int) -> Call | None:
        pass

    def get_all(self, sort: str) -> List[Call]:
        pass

    def filter_by_interpreter(self, interpreter_id, sort: str) -> List[Call]:
        pass

    def filter_by_responsible(self, responsible_id, sort: str) -> List[Call]:
        pass

    def create(self) -> Call:
        pass

    def update(self, call: Call) -> Call:
        pass

    def delete(self, call_id: int) -> None:
        pass


class CallRepository(ICallRepository):
    def get(self, call_id):
        return Call.objects.filter(id=call_id).first()

    def get_all(self, sort):
        return Call.objects.all().order_by(sort)

    def filter_by_interpreter(self, interpreter_id, sort):
        return Call.objects.filter(interpreter_id=interpreter_id).order_by(sort)

    def filter_by_responsible(self, responsible_id, sort):
        return Call.objects.filter(responsible_id=responsible_id).order_by(sort)

    def create(self):
        return Call.objects.create()

    def update(self, call):
        Call.objects.update()
        call.save()
        return call

    def delete(self, call_id):
        pass
