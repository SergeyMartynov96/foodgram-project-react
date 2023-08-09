from django.contrib import admin

from recipes.models import Recipe

from .models import Subscription, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email', 'username', 'first_name',
                    'last_name', 'count_recipe', 'count_subscribe')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('username', 'email')
    empty_value_display = 'пусто'

    @admin.display(description='Количество рецептов')
    def count_recipe(self, obj):
        return Recipe.objects.filter(author__id=obj.id).count()

    @admin.display(description='Количество подписчиков')
    def count_subscribe(self, obj):
        return Subscription.objects.filter(author__id=obj.id).count()


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'author')
    search_fields = ('user', 'author')
    list_filter = ('user', 'author')
    empty_value_display = 'пусто'
