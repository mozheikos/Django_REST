from mixer.backend.django import mixer

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate, APITestCase, APIClient

from usersapp.models import User
from usersapp.views import UserModelViewSet
from todoapp.models import ToDo, Project
from todoapp.views import ProjectModelViewSet, ToDoModelViewSet


def print_test_result(user: str, url: str, response_status: int) -> None:
    print(user, url, response_status)


class TestViewsUrls(TestCase):

    def setUp(self) -> None:

        """
        Чтобы не писать кучу одинакового кода, добавил ряд параметров:
        """

        """
        Ссылки на разные странице API
        """
        self.category_links = ("/users/", "/projects/", "/ToDo/")

        """
        Основная точка входа
        """
        self.url = "/api"

        """
        Словарь с моделями, чтобы брать нужную модель в зависимости от ссылки
        """
        self.models = {
            "/users/": User,
            "/projects/": Project,
            "/ToDo/": ToDo
        }

        """
        Аналогично моделям
        """
        self.views = {
            "/users/": UserModelViewSet,
            "/projects/": ProjectModelViewSet,
            "/ToDo/": ToDoModelViewSet
        }

        """
        Количество тестовых объектов, создаваемых в базе для проверки переходов на страницы с подробной 
        информацией
        """
        self.objects_quantity = 20

        """
        Учетные данные пользователя для проверки ссылок с авторизованным пользователем
        """
        self.auth_user = {
            "username": "admin",
            "email": "admin@admin.com",
            "password": "admin"
        }

        self.instance_to_create = {
            "/users/": {
                "username": "some_user",
                "first_name": "some_firstname",
                "last_name": "some_last_name",
                "email": "some_user@mail.ru",
                "project_set": ''
            },
            "/projects/": {
                "title": "some_project",
                "repository_link": "https://www.github.com",
                "users": ''
            },
            "/ToDo/": {
                "project": '',
                "user": '',
                "text": "some_message",
                "status": "active"
            }
        }

        self.instance_to_update = {
            "/users/": {
                "username": "some_user_updated",
                "first_name": "some_firstname",
                "last_name": "some_last_name",
                "email": "some_user_updated@mail.ru",
            },
            "/projects/": {
                "title": "some_project_updated",
                "repository_link": "https://www.google.com",
            },
            "/ToDo/": {
                "text": "some_message_updated",
                "status": "closed"
            }
        }

    def create_superuser(self) -> User:
        """
        Вынес создание пользователя "Админ" в отдельную функцию
        """
        return User.objects.create_superuser(**self.auth_user)

    def test_get_pages(self, is_anonymous: bool = True) -> None:

        print("\n", "-" * 50, "\n")
        print(self.__str__())

        """для теста с зарегистрированным пользователем создаем superuser"""
        user = "anonymous" if is_anonymous else self.create_superuser()

        factory = APIRequestFactory()

        """Обходим в цике все страницы ListView"""
        for link in self.category_links:

            """Для проверки страниц подробной информации создаем 20 сущностей для каждой модели"""
            for i in range(self.objects_quantity):
                mixer.blend(self.models[link])

            url = self.url + link
            request = factory.get(url)

            """Для не анонимного теста аутентифицируемся в системе"""
            if not is_anonymous:
                force_authenticate(request=request, user=user)

            view = self.views[link].as_view({"get": "list"})
            response = view(request)

            """Для удобства просмотра результатов конкретной итерации теста вывел данные в консоль"""
            print_test_result(user, url, response.status_code)

            """Проверяем результат запроса
            
            - Если пользователь ананимный - должны вернуться 200 везде, кроме страницы с проектами (в соответствии
            с настройкой прав проекта)
            
            - Админ обладает всеми правами, поэтому для проверки под админом 200 должен быть везде
            """
            self.assertEqual(
                response.status_code,
                status.HTTP_401_UNAUTHORIZED if is_anonymous and link == "/projects/" else status.HTTP_200_OK)

            """Выбираем id записей в базе"""
            items = [x.id for x in self.models[link].objects.all()]

            """В цикле проходим по подробным страницам для всех сущностей в базе"""
            for pk in items:
                url = self.url + link + f"{pk}/"
                request = factory.get(url)
                if not is_anonymous:
                    force_authenticate(request=request, user=user)
                view = self.views[link].as_view({"get": "retrieve"})
                response = view(request, pk=str(pk))
                print_test_result(user, url, response.status_code)

                """Проверка аналогична проверке статусов при обходе ListView"""
                self.assertEqual(
                    response.status_code,
                    status.HTTP_401_UNAUTHORIZED if is_anonymous and link == "/projects/" else status.HTTP_200_OK)

    def test_get_pages_as_admin(self) -> None:

        """Вызываю предыдущий тест, но с параметром is_anonymous=False"""
        self.test_get_pages(is_anonymous=False)

    def test_post_put_delete_method_object(self, is_anonymous: bool = True) -> None:

        print("\n", "-" * 50, "\n")
        print(self.__str__())

        client = APIClient()
        user = "anonymous"
        project = None
        if not is_anonymous:
            user = self.create_superuser()
            project = mixer.blend(Project)
            client.login(username=self.auth_user["username"], password=self.auth_user["password"])

        print("create")
        for link in self.category_links:
            if link == "/users/" and not is_anonymous:
                self.instance_to_create[link].update({"project_set": [project.title]})
            elif link == "/ToDo/" and not is_anonymous:
                self.instance_to_create[link].update({"project": project.title, "user": user.username})
            elif link == "/projects/" and not is_anonymous:
                self.instance_to_create[link].update({"users": [user.id]})
            url = self.url + link
            response = client.post(path=url, data=self.instance_to_create[link])
            print_test_result(user, url, response.status_code)
            self.assertEqual(
                response.status_code,
                status.HTTP_401_UNAUTHORIZED if is_anonymous else status.HTTP_201_CREATED
            )

        print("update")
        for link in self.category_links:
            if is_anonymous:
                instance = mixer.blend(self.models[link])
            else:
                instance = self.models[link].objects.last()
            url = self.url + link + f"{instance.pk}/"
            response = client.put(path=url, data=self.instance_to_update[link])
            print_test_result(user, url, response.status_code)
            self.assertEqual(
                response.status_code,
                status.HTTP_401_UNAUTHORIZED if is_anonymous else status.HTTP_200_OK
            )

        print("delete")
        for link in self.category_links[::-1]:
            if is_anonymous:
                instance = mixer.blend(self.models[link])
            else:
                instance = self.models[link].objects.last()
            url = self.url + link + f"{instance.pk}/"
            response = client.delete(path=url, data={"pk": 1})
            print_test_result(user, url, response.status_code)
            if not is_anonymous:
                self.assertEqual(
                    response.status_code,
                    status.HTTP_200_OK if link == "/ToDo/" else status.HTTP_204_NO_CONTENT)
            else:
                self.assertEqual(
                    response.status_code,
                    status.HTTP_401_UNAUTHORIZED)

        if not is_anonymous:
            client.logout()

    def test_post_put_delete_method_object_as_admin(self) -> None:
        self.test_post_put_delete_method_object(is_anonymous=False)


class TestViewsGetRequestsAPITestCase(APITestCase):

    def setUp(self) -> None:

        """Данные возьму те же, кроме данных для создания и обновления: тестировать будем только GET-запросы"""

        self.category_links = ("/users/", "/projects/", "/ToDo/")
        self.url = "/api"
        self.models = {
            "/users/": User,
            "/projects/": Project,
            "/ToDo/": ToDo
        }
        self.views = {
            "/users/": UserModelViewSet,
            "/projects/": ProjectModelViewSet,
            "/ToDo/": ToDoModelViewSet
        }
        self.objects_quantity = 20
        self.auth_user = {
            "username": "admin",
            "email": "admin@admin.com",
            "password": "admin"
        }

    def create_superuser(self) -> User:
        return User.objects.create_superuser(**self.auth_user)

    def test_get_requests(self, is_anonymous: bool = True) -> None:

        print("\n", "-" * 50, "\n")
        print(self.__str__())

        user = "anonymous"

        if not is_anonymous:
            user = self.create_superuser()
            self.client.login(username=self.auth_user["username"], password=self.auth_user["password"])

        for link in self.category_links:

            for i in range(self.objects_quantity):
                mixer.blend(self.models[link])

            url = self.url + link
            response = self.client.get(path=url)
            print_test_result(user, url, response.status_code)
            self.assertEqual(
                response.status_code,
                status.HTTP_401_UNAUTHORIZED if link == "/projects/" and is_anonymous else status.HTTP_200_OK
            )

            items = [x.id for x in self.models[link].objects.all()]

            for pk in items:
                url = self.url + link + f"{pk}/"
                response = self.client.get(path=url)
                print_test_result(user, url, response.status_code)
                self.assertEqual(
                    response.status_code,
                    status.HTTP_401_UNAUTHORIZED if link == "/projects/" and is_anonymous else status.HTTP_200_OK
                )

        if not is_anonymous:
            self.client.logout()

    def test_get_requests_as_admin(self) -> None:
        self.test_get_requests(is_anonymous=False)
