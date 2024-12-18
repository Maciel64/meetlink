from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from meetlink.domain.call.call_adapter import GoogleMeetAdapter
from meetlink.domain.call.call_repository import CallRepository
from meetlink.domain.call.call_service import CallService
from meetlink.domain.subject.subject_repository import SubjectRepository
from meetlink.domain.user.user_repository import UserRepository
from meetlink.forms import EditCallForm


@login_required
def create_call(request):
    call_adapter = GoogleMeetAdapter()

    call = call_adapter.create_call()

    return render(request, "create_call.html", {"call_uri": call.call_uri})


@login_required
def calls_index(request):
    call_repository = CallRepository()
    user_repository = UserRepository()
    subject_repository = SubjectRepository()

    call_service = CallService(call_repository, user_repository, subject_repository)

    calls = call_service.get_all()

    return render(request, "calls/index.html", {"calls": calls})


class CallsEdit(View):
    def __init__(self):
        self.call_repository = CallRepository()
        self.user_repository = UserRepository()
        self.subject_repository = SubjectRepository()

        self.call_service = CallService(
            self.call_repository, self.user_repository, self.subject_repository
        )

    @method_decorator(login_required)
    def get(self, request, id):
        call = self.call_service.get(id)
        subjects = self.subject_repository.get_all()

        return render(
            request,
            "calls/edit.html",
            {
                "call": call,
                "subjects": subjects,
                "error": request.session.pop("error", None),
                "success": request.session.pop("success", None),
            },
        )

    @method_decorator(login_required)
    def post(self, request, id):
        try:
            self.call_service.update(id, EditCallForm(request.POST))
            request.session["success"] = "Dados da Chamada atualizados com sucesso!"

        except Exception as e:
            request.session["error"] = str(e)

        return redirect("calls_edit", id=id)
