from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import HttpResponse, get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from api.utils_logic.filters import RecipeFilter
from api.recipes_logic.serializers import (FavoriteSerializer,
                             RecipeCreateSerializer,
                             RecipeGetSerializer, ShoppingCartSerializer)
from api.utils_logic.utilit import create_model_instance, delete_model_instance
from recipes.models import Favorite, Recipe, RecipeIngredient, ShoppingCart




class RecipeViewSet(viewsets.ModelViewSet):
    """Работа с рецептами. Создание/изменение/удаление рецепта."""
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthenticated, )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeGetSerializer
        return RecipeCreateSerializer

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated, ]
    )
    def favorite(self, request, pk):
        """Работа с избранными рецептами."""
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            return create_model_instance(request, recipe, FavoriteSerializer)

        if request.method == 'DELETE':
            return delete_model_instance(request, Favorite, recipe)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated, ]
    )
    def shopping_cart(self, request, pk):
        """Работа со списком покупок."""
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            return create_model_instance(request, recipe, ShoppingCartSerializer)

        if request.method == 'DELETE':
            return delete_model_instance(request, ShoppingCart, recipe)
    
    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated, ]
    )
    def download_shopping_cart(self, request):
        """Отправка файла со списком покупок."""
        ingredients = (
            RecipeIngredient.objects.filter(recipe__carts__user=request.user)
            .values('ingredient__name', 'ingredient__measurement_unit')
            .order_by('ingredient__name')
            .annotate(total=Sum('amount'))
        )
        shop_list = 'Список покупок: '
        result = shop_list + "\n".join(
            (
                f'{ingredient["ingredient__name"]} - {ingredient["total"]}/'
                f'{ingredient["ingredient__measurement_unit"]}'
                for ingredient in ingredients
            )
        )
        response = HttpResponse(result, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="Моя корзина"'
        return response
