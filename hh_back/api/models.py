from django.db import models
from django.contrib.auth.models import User


    


class Author(models.Model):
    name = models.CharField('Имя автора', max_length=100)
    surname = models.CharField('Фамилия автора', max_length=100)
    birth_date = models.DateField()

    def __str__(self):
        return self.name + ' ' + self.surname
    

    

class Book(models.Model):
    title = models.CharField('Название книги', max_length=100)
    publishDate = models.CharField('Дата публикации книг', max_length=100)
    description=models.TextField('Описание')
    thumbnail=models.TextField('Ссылка на картинку')
    averageRating=models.FloatField('Рейтинг')
    genre = models.CharField('жанр книги', max_length=100)
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='книги',
        null=True, blank=True
    )

    def __str__(self):
        return self.title

class Review(models.Model):
    rating = models.FloatField()
    comment = models.TextField('Обзор')
    created_at = models.DateTimeField(auto_now_add=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews', null=True, blank=True)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        null=True, blank=True
    )

    def __str__(self):
        return self.comment


class Recommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book_title = models.CharField(max_length=255)
    recommended_books = models.JSONField()  # список рекомендованных книг
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recommendation for {self.user.username} - {self.book_title}"


class UserPreference(models.Model):
    """
    Модель для хранения предпочтений пользователя.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='preferences')
    category = models.CharField(max_length=255)  # Тип предпочтения (например, "Main Genre", "Author")
    value = models.CharField(max_length=255)  # Значение предпочтения (например, "Science Fiction", "J.K. Rowling")
    score = models.FloatField()  # Оценка/балл предпочтения
    weight = models.FloatField()
    class Meta:
        unique_together = ('user', 'category', 'value', 'weight')  # Уникальная пара: user + (attribute_type, attribute_value)

    def __str__(self):
        return f"{self.user.username} - {self.category}: {self.value} (Score: {self.score})"


class GlobalPreference(models.Model):
    """
    Модель для хранения глобальных предпочтений.
    """
    category = models.CharField(max_length=255)  # Тип предпочтения (например, "Main Genre", "Author")
    value = models.CharField(max_length=255)  # Значение предпочтения (например, "Science Fiction", "J.K. Rowling")
    score = models.FloatField()  # Оценка/балл предпочтения

    class Meta:
        unique_together = ('category', 'value')  # Уникальная пара: (attribute_type, attribute_value)

    def __str__(self):
        return f"{self.category}: {self.value} (Score: {self.score})"

