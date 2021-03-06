from django.db import models
from users.models import User
from django.db.models import UniqueConstraint

GRADES = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
    (8, 8),
    (9, 9),
    (10, 10),
)


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
        related_name="titles",
        null=True,
        on_delete=models.SET_NULL,
    )
    rating = models.SmallIntegerField(
        verbose_name="Средний рейтинг", null=True, blank=True
    )


class Review(models.Model):
    """
    Отзывы
    """

    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name="reviews"
    )
    text = models.TextField(verbose_name="Текст отзыва", max_length=500)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews"
    )
    score = models.SmallIntegerField(verbose_name="Оценка", choices=GRADES)
    pub_date = models.DateTimeField(
        verbose_name="Дата публикации",
        auto_now_add=True,
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["author", "title"], name="author_title_unique"
            )
        ]


class Comment(models.Model):
    """
    Комментарии
    """

    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField(verbose_name="Текст комментария", max_length=500)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    pub_date = models.DateTimeField(
        verbose_name="Дата публикации", auto_now_add=True
    )
