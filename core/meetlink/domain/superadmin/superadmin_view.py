from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from meetlink.domain.call.call_repository import CallRepository
from meetlink.domain.call.call_service import CallService
from meetlink.domain.subject.subject_repository import SubjectRepository
from meetlink.domain.user.user_repository import UserRepository

call_repository = CallRepository()
user_repository = UserRepository()
subject_repository = SubjectRepository()

call_service = CallService(call_repository, user_repository, subject_repository)


@login_required
def actions(request):
    call = call_service.get_last()

    return render(request, "superadmin/actions.html", {"call": call})
