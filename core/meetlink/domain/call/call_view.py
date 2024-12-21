from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from meetlink.domain.call.call_adapter import GoogleMeetAdapter
from meetlink.domain.call.call_repository import CallRepository
from meetlink.domain.call.call_serializer import CallSerializer
from meetlink.domain.call.call_service import CallService
from meetlink.domain.subject.subject_repository import SubjectRepository
from meetlink.domain.user.user_repository import UserRepository
from meetlink.forms import EditCallForm
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet


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


class CallAPI(ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.call_repository = CallRepository()
        self.user_repository = UserRepository()
        self.subject_repository = SubjectRepository()

        self.call_service = CallService(
            self.call_repository, self.user_repository, self.subject_repository
        )

    def list(self, request):
        serialized_calls = CallSerializer(self.call_service.get_all(), many=True)
        return Response(serialized_calls.data, status=status.HTTP_200_OK)

    def create(self, request):
        print(request.data)
        serialized_call = CallSerializer(self.call_service.create())
        return Response(serialized_call.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def insert_manager(self, request, pk=None):
        try:
            serialized_call = CallSerializer(
                self.call_service.insert_manager(pk, request.data["manager_id"])
            )
            return Response(serialized_call.data, status=status.HTTP_200_OK)
        except APIException as e:
            return Response(str(e), status=e.status_code)
