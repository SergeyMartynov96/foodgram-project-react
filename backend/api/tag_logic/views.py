from rest_framework import viewsets
from recipes.models import Tag
from api.tag_logic.serializers import TagSerialiser
from rest_framework.permissions import AllowAny


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение информации о тегах."""
    queryset = Tag.objects.all()
    serializer_class = TagSerialiser
    permission_classes = (AllowAny, )
    pagination_class = None
