from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter

from usersapp.views import UserModelViewSet

app_name = "usersapp"

router = DefaultRouter()
router.register("", UserModelViewSet)

urlpatterns = (
    path("", include((router.urls, "usersapp"))),
)
