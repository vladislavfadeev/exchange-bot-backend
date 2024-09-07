from typing import Any, Dict

from django.views import View
from django.views.generic import ListView
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.db.models.query import QuerySet

from apps.db_model.models import Transaction
from apps.web_app.security import is_valid 


class CBaseView():
    def valid_check(self, request):
        init_data_hash = request.GET['initDataHash']
        data_check_string = request.GET['dataCheckString']
        if not is_valid(init_data_hash, data_check_string):
            return HttpResponse("Unauthorized", status=401)


class HomeView(CBaseView, View):
    template_name = "web_app/home/index.html"

    def get(self, request, *args, **kwargs):
        # self.valid_check(self, request)
        print(request.GET, args, kwargs)
        return render(request, self.template_name)
    

class MyBarters(CBaseView, ListView):
    # form_class = HomeCreateLinkForm
    template_name = "home/index.html"
    context_object_name = "links"
    paginate_by = 5
    ordering = "-date_created"
    model = Transaction

    def get_queryset(self) -> QuerySet[Any]:
        self.queryset = self.model.objects.filter(user=self.request.user)
        return super().get_queryset()

class PostData(CBaseView, View):
    def post(self, request, *args, **kwargs):
        # self.valid_check(request)
        raw_data = request.body.decode('utf-8') 
        print(raw_data)
        return HttpResponse(status=200)