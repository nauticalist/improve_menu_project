from django.db import models


class Menu(models.Model):
    """
    Menu model
    """
    season = models.CharField(max_length=20)
    items = models.ManyToManyField('Item', related_name='items')
    created_date = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField(
            blank=True, null=True)

    def __str__(self):
        return self.season

    class Meta:
        ordering = ('-expiration_date', )


class Item(models.Model):
    """
    Menu items
    """
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=255)
    chef = models.ForeignKey('auth.User')
    created_date = models.DateTimeField(
            auto_now_add=True)
    standard = models.BooleanField(default=False)
    ingredients = models.ManyToManyField('Ingredient')

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
