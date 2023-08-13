from colorfield.fields import ColorField
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User


class Ingredient(models.Model):
    """Модель ингредиентов"""
    name = models.CharField(verbose_name='Ингредиент',
                            max_length=settings.MAX_LENGTH_RECIPE)
    measurement_unit = models.CharField(verbose_name='Единица измерения',
                                        max_length=settings.MAX_LENGTH_RECIPE)

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ingredient'
            )
        ]

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Tag(models.Model):
    """Модель тегов"""
    name = models.CharField(verbose_name='Тег',
                            max_length=settings.MAX_LENGTH_RECIPE)
    color = ColorField(format='hex',
                       verbose_name='Цвет', help_text='Введите цвет тега',
                       unique=True)
    slug = models.SlugField(verbose_name='Адрес',
                            max_length=settings.MAX_LENGTH_RECIPE, unique=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
    )
    name = models.CharField(verbose_name='Название',
                            max_length=settings.MAX_LENGTH_RECIPE,)
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='',
        blank=True,
    )
    text = models.TextField(verbose_name='Описание')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='Ингредиенты',
        blank=False,
    )
    tags = models.ManyToManyField(Tag, verbose_name='Теги', blank=False,)
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        validators=[
            MinValueValidator
            (1, 'Время приготовления не должно быть меньше 1 минуты'),
            MaxValueValidator
            (300, 'Время приготовления не должно быть меньше 5 часов')
        ]
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    """Модель ингридиентов определенного рецепта"""
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='recipeingredients',
        verbose_name='Рецепт'

    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE,
        related_name='recipeingredients',
        verbose_name='Ингредиент в рецепте',
        blank=False
    )
    amount = models.IntegerField(
        'Количество',
        validators=[
            MinValueValidator
            (1, 'Количество ингредиентов не может быть меньше 1'),
            MaxValueValidator
            (999, 'Количество ингредиентов не может быть больше 999')
        ]
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'

    def __str__(self):
        return f'{self.recipe} - {self.ingredient}'


class AbstractShopOrFavorite(models.Model):
    """Абстрактная модель избранного и корзины покупок"""
    class Meta:
        abstract = True
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)


class Favorite(AbstractShopOrFavorite):
    """Модель избранного рецепта"""
    class Meta:
        default_related_name = 'favorites'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_recipe_favorite'
            )
        ]
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'

    def __str__(self):
        return f'{self.user.username} добавил {self.recipe.name} в избраннное'


class ShoppingCart(AbstractShopOrFavorite):
    """Модель корзины покупок"""
    class Meta:
        default_related_name = 'carts'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_recipe_cart'
            )
        ]
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self):
        return (f'{self.user.username} добавил'
                f'{self.recipe.name} в список покупок')
