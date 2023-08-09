from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from api.ingredient_serializers import IngredientInfoSerializer
from api.utils_logic.filters import IngredientFilter
from recipes.models import Ingredient


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение информации об ингредиентах."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientInfoSerializer
    permission_classes = (AllowAny, )
    filter_backends = (DjangoFilterBackend, )
    pagination_class = None
    filterset_class = IngredientFilter
