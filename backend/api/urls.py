from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.ingredient_views import IngredientViewSet
from api.recipe_views import RecipeViewSet
from api.tag_views import TagViewSet
from api.user_views import UserSubscribeView, UserSubscriptionsViewSet

router = DefaultRouter()

router.register(r'tags', TagViewSet, basename='tags')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'recipes', RecipeViewSet, basename='recipes')


urlpatterns = [
    path('users/subscriptions/',
         UserSubscriptionsViewSet.as_view({'get': 'list'})),
    path('users/<int:user_id>/subscribe/', UserSubscribeView.as_view()),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
