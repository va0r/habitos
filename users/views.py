from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from users.models import User
from users.seriliazers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        # получаем данные отправленные в запросе
        data = request.data

        # Извлекаем значение Telegram ID из данных запроса
        telegram_id = data.get('telegram_id', None)

        # Проверка на валидность
        if not telegram_id:
            return Response({"telegram_id": "Это поле обязательно."}, status=status.HTTP_400_BAD_REQUEST)

        # Создаем пользователя с Telegram ID
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        else:
            return [IsAuthenticated()]

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
