from typing import List, Protocol

from meetlink.models import Subject


class ISubjectRepository(Protocol) :
    def get(self, subject_id: int) -> Subject | None :
        pass
    
    def get_all(self) -> List[Subject] :
        pass
    
    def create(self, subject: Subject) -> Subject :
        pass

    def update(self, subject_id: int, subject: Subject) -> Subject :
        pass

    def delete(self, subject_id: int) -> None :
        pass


class SubjectRepository(ISubjectRepository) :
    def get(self, subject_id) :
        try :
            return Subject.objects.get(id=subject_id)
        
        except Subject.DoesNotExist :
            return None
        
    def get_all(self):
        return Subject.objects.all()
    

    def create(self):
        return Subject.objects.create(Subject)

    def update(self, subject_id, subject) :
        pass

    def delete(self, subject_id) :
        pass
    
