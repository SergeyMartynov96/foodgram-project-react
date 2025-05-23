from rest_framework import serializers

from recipes.models import Tag


class TagSerialiser(serializers.ModelSerializer):
    """Сериализатор для работы с тегами."""
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
