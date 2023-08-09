from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.user_serializers import UserSubRepresentSerializer, UserSubSerializer
from api.utils_logic.mixins import CreateCastomView
from users.models import Subscription, User


class UserSubscribeView(APIView):
    """Вью для работы с сабами."""
    def post(self, request, user_id):
        author = get_object_or_404(User, id=user_id)
        if self.request.user == author or Subscription.objects.filter(
                user=request.user, author=user_id).exists():
            return Response(
                {'error': 'Вы подписаны на этого автора'},
                status=status.HTTP_400_BAD_REQUEST)
        subscription = Subscription.objects.create(
            author=author, user=self.request.user)
        serializer = UserSubSerializer(
            subscription, context={'request': request})

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, user_id):
        subscription = Subscription.objects.filter(
            user=request.user, author=user_id)
        if subscription.exists():
            subscription.delete()
            return Response({'message': 'Подписка успешно удалена'},
                            status=status.HTTP_204_NO_CONTENT)
        return Response({'message': 'У вас не было такой подписки'},
                        status=status.HTTP_400_BAD_REQUEST)


class UserSubscriptionsViewSet(CreateCastomView):
    """Вью для получение списка подписок на пользователей."""
    serializer_class = UserSubRepresentSerializer

    def get_queryset(self):
        return User.objects.filter(following__user=self.request.user)
