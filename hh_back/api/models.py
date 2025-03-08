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




