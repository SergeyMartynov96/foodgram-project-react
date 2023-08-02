from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.recipes_logic.views import RecipeViewSet
from api.users_logic.views import UserSubscribeView, UserSubscriptionsViewSet
from api.tag_logic.views import TagViewSet
from api.ingredient_logic.views import IngredientViewSet

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
