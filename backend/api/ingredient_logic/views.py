from rest_framework import viewsets
from recipes.models import Ingredient
from api.ingredient_logic.serializers import IngredientInfoSerializer
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение информации об ингредиентах."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientInfoSerializer
    permission_classes = (AllowAny, )
    filter_backends = (DjangoFilterBackend, )
    pagination_class = None
