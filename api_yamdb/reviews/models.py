from django.db import models


class Genre(models.Model):
    """
    Жанры произведений. Одно произведение может быть привязано к нескольким
    жанрам.
    """

    name = models.CharField(max_length=200, verbose_name="Жанр", unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    """
    Категории (типы) произведений («Фильмы», «Книги», «Музыка»).
    """

    name = models.CharField(
        max_length=200, verbose_name="Категория", unique=True
    )
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    """
    Произведения, к которым пишут отзывы (определённый фильм, книга или
    песенка).
    """

    name = models.CharField(max_length=200, verbose_name="Произведение")
    year = models.IntegerField(
        null=True, verbose_name="Год издания", db_index=True
    )
    description = models.CharField(max_length=200, null=True)
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        related_name="titles",
    )
    category = models.ForeignKey(
        Category,
        null=True,
        related_name="titles",
        on_delete=models.SET_NULL,
    )
