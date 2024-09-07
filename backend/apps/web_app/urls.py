from django.urls import path, include
from apps.web_app.views import (
    HomeView,
    PostData,
)


urlpatterns = [
    path("web_app/v1/home", HomeView.as_view(), name='home'),
    path("web_app/v1/post", PostData.as_view(), name='post'),
]
