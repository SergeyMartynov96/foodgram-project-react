from django.core.validators import MinValueValidator
from django.db import models
from users.models import User


class Ingredient(models.Model):
    """Модель ингредиентов"""
    name = models.CharField('Ингредиент', max_length=100)
    measurement_unit = models.CharField('Единица измерения', max_length=100)

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Модель тегов"""
    name = models.CharField('Тег', max_length=200)
    color = models.CharField('Цвет', max_length=7)
    slug = models.SlugField('Адрес', max_length=200, unique=True)

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
    name = models.CharField('Название', max_length=200)
    image = models.ImageField(
        'Картинка',
        upload_to='',
        blank=True,
    )
    text = models.TextField('Описание')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='Ингредиенты',
    )
    tags = models.ManyToManyField(Tag, verbose_name='Теги',)
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        validators=[
            MinValueValidator(
                1, 'Время приготовления не должно быть меньше 1 минуты'
            )
        ]
    )

    class Meta:
        ordering = ['-id']
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
        verbose_name='Ингредиент в рецепте'
    )
    amount = models.IntegerField(
        'Количество',
        validators=[
            MinValueValidator(
                1, 'Количество ингредиентов не может быть меньше 1'
            )
        ]
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'

    def __str__(self):
        return f'{self.recipe} - {self.ingredient}'
 

class Favorite(models.Model):
    """Модель избранного рецепта"""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Избранный рецепт',
    )

    class Meta:
        ordering = ['-id']
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


class ShoppingCart(models.Model):
    """Модель корзины покупок"""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='carts',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='carts',
        verbose_name='Рецепт'
    )

    class Meta:
        ordering = ['-id']
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
