import uuid
import datetime
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from api.models import Book, Review, Recommendation, UserPreference, GlobalPreference, Author
from django.urls import reverse
from rest_framework.authtoken.models import Token

class APITests(APITestCase):
    
    @classmethod
    def setUpTestData(cls):
        # Генерация уникального имени пользователя
        unique_username = f'testuser_{uuid.uuid4()}'
        cls.user = User.objects.create_user(username=unique_username, password='password123')
        
        # Создание других объектов теста
        cls.author = Author.objects.create(
            name="Имя", 
            surname="Фамилия", 
            birth_date=datetime.date(1980, 1, 1)
        )
        
        cls.book = Book.objects.create(
            title="Книга",
            publishDate=datetime.date.today(),
            description="Описание",
            thumbnail="http://example.com/image.jpg",
            averageRating=4.5,
            genre="Фантастика",
            author=cls.author
        )

        # Создаем токен для пользователя
        cls.token = Token.objects.create(user=cls.user)

        # Создаем отзыв
        cls.review = Review.objects.create(
            rating=5.0,
            comment="Отличная книга!",
            book=cls.book,
            user=cls.user  # Привязываем к пользователю
        )

    def test_registration(self):
        url = reverse('registration')
        data = {'username': 'newuser', 'password': 'password123', 'password2': 'password123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)

    def test_registration_password_mismatch(self):
        url = reverse('registration')
        data = {'username': 'newuser', 'password': 'password123', 'password2': 'wrongpassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Passwords must match')

    def test_review_list(self):
        url = reverse('review_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_create_review(self):
        url = reverse('review_list')
        data = {
            'rating': 4.0,
            'comment': 'Хорошая книга!',
            'book': self.book.id,
            'user': self.user.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['rating'], 4.0)

    def test_review_detail(self):
        url = reverse('review_detail', args=[self.review.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['comment'], 'Отличная книга!')

    def test_update_review(self):
        url = reverse('review_detail', args=[self.review.id])
        data = {'rating': 3.0, 'comment': 'Средняя книга!'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['rating'], 3.0)

    def test_delete_review(self):
        url = reverse('review_detail', args=[self.review.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_profile_get(self):
        # Получаем токен для авторизации
        token = self.token.key
        # Добавляем токен в заголовок Authorization
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        url = reverse('profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')

    def test_get_recommendations(self):
        url = reverse('get_recommendations', args=[self.user.id])
        data = {'user_id': self.user.id, 'user_book_titles': ['Книга']}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('recommended_titles', response.data)

    def test_search_books(self):
        url = reverse('search_books')
        response = self.client.get(url, {'q': 'Книга'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_update_user_preferences(self):
        self.client.login(username=self.user.username, password='password123')
        url = reverse('user_preferences', args=[self.user.id])
        data = {
            "Main Genre": {
                "Фантастика": 5
            },
            "Sub Genre": {
                "Детектив": 4
            }
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Preferences updated successfully')

    def test_get_user_preferences(self):
        self.client.login(username=self.user.username, password='password123')
        url = reverse('user_preferences', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Main Genre', response.data)

    def test_get_global_preferences(self):
        url = reverse('global_preferences')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Main Genre', response.data)
