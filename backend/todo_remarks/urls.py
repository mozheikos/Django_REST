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
from django.urls import path, include, re_path
from django.conf import settings
from django.contrib.staticfiles import views as sf_views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from graphene_django.views import GraphQLView

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from usersapp.views import UserModelViewSet, get_links
from todoapp.views import ProjectModelViewSet, ToDoModelViewSet


schema_view = get_schema_view(
    info=openapi.Info(
        title="ToDo-Remarks",
        default_version='v2',
        description='documentation',
        contact=openapi.Contact(
                name="Stanislav",
                url="https://github.com/mozheikos/Django_REST",
                email="mozheiko.stanislav@yandex.ru"
            ),
        license=openapi.License(
                name="MIT"
            )
        ),
    public=True,
    )


router = DefaultRouter()
# router.register("v1/users", UserModelViewSet, basename="v1")  # В другом варианте раскомментировать
# router.register("v2/users", UserModelViewSet, basename="v2")  # В другом варианте раскомментировать
router.register("projects", ProjectModelViewSet)
router.register("ToDo", ToDoModelViewSet)
router.register("users", UserModelViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    # path('', include(router.urls)),
    path('api/', include(router.urls)),
    path('api/jwt-token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/jwt-token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-token-auth', views.obtain_auth_token),
    path('api/links/', get_links),

    # re_path(r'^users/v1/', include('usersapp.urls', namespace="v1")),  # В другом варианте закомментировать
    # re_path(r'^users/v2/', include('usersapp.urls', namespace="v2")),  # В другом варианте закомментировать

    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('graphql/', GraphQLView.as_view(graphiql=True)),
    re_path(r'^static/(?P<path>.*)$', sf_views.serve)
]

