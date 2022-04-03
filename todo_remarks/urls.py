"""todo_remarks URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from usersapp.views import UserModelViewSet
from usersapp.views import get_links
from todoapp.views import ProjectModelViewSet, ToDoModelViewSet
from rest_framework.authtoken import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register("users", UserModelViewSet)
router.register("projects", ProjectModelViewSet)
router.register("ToDo", ToDoModelViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', include(router.urls)),
    path('api/', include(router.urls)),

    path('api/jwt-token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/jwt-token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-token-auth', views.obtain_auth_token),
    path('api/links/', get_links),
]

"""Ниже код, который я использовал, чтобы проверить jwt-авторизацию"""
# import requests
# import json
#
# credentials = {
#     "username": "admin",
#     "password": "admin"
# }
#
# token_url = "http://localhost:8000/api/jwt-token/"
# token_headers = {
#     "content-type": "application/json",
# }
# token_data = json.dumps(credentials)
# token = requests.post(url=token_url, data=token_data, headers=token_headers).json()
# print(token)
#
# access_token = token["access"]
# refresh_token = token["refresh"]
#
# get_projects_url = "http://localhost:8000/api/projects/"
# get_projects_header = {
#     "authorization": f"Bearer {access_token}"
# }
#
# response = requests.get(url=get_projects_url, headers=get_projects_header).json()
# print(response)
