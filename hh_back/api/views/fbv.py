from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view
from api.models import Book, Review, Author, Recommendation, UserPreference, GlobalPreference
from django.db.models import Q
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from api.serializers import ReviewSerializer, RecommendationSerializer, BookSerializer, PreferencesSerializer
from django.shortcuts import get_object_or_404
from collections import defaultdict
import requests
import logging
from django.db import transaction

@api_view(['POST'])
def registration(request):
    username = request.data.get('username')
    password = request.data.get('password')
    password2 = request.data.get('password2')
    
    if password != password2:
        return Response({'error': 'Passwords must match'}, status=status.HTTP_400_BAD_REQUEST)
    
    if not (username and password):
        return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username is already taken'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.create(username=username, password=make_password(password))
    user.save()
    return Response({'id': user.id}, status=status.HTTP_201_CREATED)

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def review_list(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def review_detail(request, pk):
    try:
        review = Review.objects.get(pk=pk)
    except Review.DoesNotExist:
        return Response({'message': 'The review does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ReviewSerializer(review)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def profile(request):
    print(request.headers) 
    user = request.user

    if request.method == 'GET':
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'age': user.profile.age if hasattr(user, 'profile') else None
        })

    elif request.method == 'PUT':
        user.email = request.data.get('email', user.email)
        user.first_name = request.data.get('first_name', user.first_name)
        user.last_name = request.data.get('last_name', user.last_name)
        
        if hasattr(user, 'profile') and 'age' in request.data:
            user.profile.age = request.data['age']
            user.profile.save()

        user.save()
        return Response({'message': 'Profile updated successfully'})

FASTAPI_RECOMMENDATION_URL = "http://localhost:8001/recommendations"

@api_view(['GET', 'POST'])
def get_recommendations(request, user_id):
    if request.method == 'POST':
        # Получение данных из тела запроса
        user_id = request.data.get('user_id')
        book_titles = request.data.get('user_book_titles', [])

        if not user_id or not book_titles:
            return Response({'error': 'user_id и user_book_titles обязательны'}, status=status.HTTP_400_BAD_REQUEST)

        # Отправка запроса на FastAPI сервер
        try:
            fastapi_response = requests.post(FASTAPI_RECOMMENDATION_URL, json={
                "user_id": user_id,
                "user_book_titles": book_titles
            })
            if fastapi_response.status_code != 200:
                return Response({'error': 'Ошибка на стороне FastAPI-сервера'}, status=fastapi_response.status_code)

            fastapi_data = fastapi_response.json()
            recommendations = fastapi_data.get('recommended_titles', [])

            # Сохраняем рекомендации в БД
            for title in book_titles:
                Recommendation.objects.create(
                    user_id=user_id,
                    book_title=title,
                    recommended_books=recommendations
                )

            return Response({
                'user_id': user_id,
                'recommended_titles': recommendations
            }, status=status.HTTP_201_CREATED)

        except requests.RequestException as e:
            return Response({'error': f'Ошибка запроса к FastAPI-серверу: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    elif request.method == 'GET':
        # Получение рекомендаций из базы данных для пользователя
        user_id = request.GET.get('user_id')

        if not user_id:
            return Response({'error': 'user_id обязателен'}, status=status.HTTP_400_BAD_REQUEST)

        recommendations = Recommendation.objects.filter(user_id=user_id)

        if not recommendations:
            return Response({'message': 'Рекомендации для данного пользователя не найдены'}, status=status.HTTP_404_NOT_FOUND)

        # Сериализация и возврат списка рекомендаций
        serializer = RecommendationSerializer(recommendations, many=True)
        return Response(serializer.data)

logger = logging.getLogger(__name__)

class UserPreferencesView(APIView):
    """
    Получает (GET) и обновляет (POST) предпочтения пользователя.
    """
    # TODO: Добавить аутентификацию и проверку прав доступа (permissions)
    # authentication_classes = [YourAuthentication]
    # permission_classes = [IsAuthenticated, YourPermissionToCheckUserMatch]

    def get(self, request, user_id, format=None):
        logger.info(f"[START] Получение предпочтений пользователя: user_id={user_id}")

        user = get_object_or_404(User, pk=user_id)
        logger.debug(f"[USER FOUND] user_id={user.id}, username={user.username}")

        try:
            preferences_qs = UserPreference.objects.filter(user=user).values(
                'category', 'value', 'score', 'weight'
            )
            logger.debug(f"[QUERYSET] Получено {preferences_qs.count()} предпочтений из базы")

            preferences_dict = defaultdict(dict)
            for pref in preferences_qs:
                logger.debug(f"[PREFERENCE] {pref}")
                attr_type_key = pref['category']
                preferences_dict[attr_type_key][pref['value']] = pref['score']

            serializer = PreferencesSerializer(instance=dict(preferences_dict))
            logger.info(f"[SUCCESS] Предпочтения успешно сериализованы для user_id={user_id}")
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
                logger.exception(f"[ERROR] Ошибка при получении предпочтений: user_id={user_id}, ошибка: {e}")
                return Response({"error": "An internal error occurred"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @transaction.atomic  # Гарантирует, что все обновления будут выполнены или ни одного
    def post(self, request, user_id, format=None):
        """
        Обрабатывает POST /user/{user_id}/preferences/
        """
        logger.info(f"Запрос на обновление предпочтений для user_id={user_id}")
        user = get_object_or_404(User, pk=user_id)

        # Десериализуем и валидируем входные данные
        serializer = PreferencesSerializer(data=request.data)

        if serializer.is_valid():
            data_to_process = request.data
            if not isinstance(data_to_process, dict):
                return Response({"error": "Invalid input format, expected a JSON object."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                attribute_mapping = {
                    "Main Genre": "Main Genre",
                    "Sub Genre": "Sub Genre",
                    "Type": "Type",  # Убедитесь, что значение 'Type' соответствует вашему выбору в модели
                    "Author": "Author"
                }

                for json_key, values in data_to_process.items():
                    if json_key in attribute_mapping and isinstance(values, dict):
                        attribute_type = attribute_mapping[json_key]  # Получаем имя для БД
                        for attribute_value, score in values.items():
                            if not isinstance(score, (int, float)):
                                logger.warning(f"Неверный тип score ({type(score)}) для {category}='{value}' user_id={user_id}")
                                continue  # Пропускаем некорректную запись

                            UserPreference.objects.update_or_create(
                                user=user,
                                attribute_type=category,
                                attribute_value=value,
                                defaults={'score': float(score)}  # Обновляем или создаем с этим score
                            )
                    elif json_key in attribute_mapping:
                        logger.warning(f"Неверный формат данных для ключа '{json_key}' user_id={user_id}. Ожидался словарь.")

                logger.info(f"Предпочтения для user_id={user_id} успешно обновлены.")
                return Response({"message": "Preferences updated successfully"}, status=status.HTTP_200_OK)

            except Exception as e:
                logger.exception(f"Ошибка БД при обновлении предпочтений для user_id={user_id}: {e}")
                return Response(
                    {"error": "An internal error occurred during update"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        else:
            logger.warning(f"Ошибка валидации данных при обновлении предпочтений user_id={user_id}: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_all_user_preferences(self, request, format=None):
        """
        Получает предпочтения всех пользователей.
        """
        logger.info("[START] Получение предпочтений всех пользователей")

        try:
            # Получаем все предпочтения
            preferences_qs = UserPreference.objects.select_related("user").values(
                 'category', 'value', 'score', 'weight'
            )
            logger.debug(f"[QUERYSET] Получено {preferences_qs.count()} предпочтений из базы")

            result = defaultdict(lambda: defaultdict(dict))
            for pref in preferences_qs:
                category = pref['category']
                value = pref['value']
                score = pref['score']

                result[user_id]['username'] = username
                result[user_id]['preferences'][category][value] = score

            # Преобразуем в список для сериализации
            data = []
            for user_id, info in result.items():
                data.append({
                    "user_id": user_id,
                    "username": info["username"],
                    "preferences": info["preferences"]
                })

            logger.info("[SUCCESS] Все предпочтения успешно собраны")
            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.exception(f"[ERROR] Ошибка при получении всех предпочтений: {e}")
            return Response({"error": "An internal error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GlobalPreferencesView(APIView):
    """
    Получает (GET) глобальные предпочтения.
    """
    # TODO: Добавить кэширование для этого эндпоинта, т.к. данные меняются редко

    def get(self, request, format=None):
        """
        Обрабатывает GET /global/preferences/
        """
        logger.info(f"Запрос глобальных предпочтений")
        try:
            preferences_qs = GlobalPreference.objects.all().values(
                'category', 'value', 'score'
            )

            preferences_dict = defaultdict(dict)
            for pref in preferences_qs:
                attr_type_key = pref['category']
                preferences_dict[attr_type_key][pref['value']] = pref['score']

            serializer = PreferencesSerializer(instance=dict(preferences_dict))
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.exception(f"Ошибка при получении глобальных предпочтений: {e}")
            return Response(
                {"error": "An internal error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        def post(self, request, format=None):
            """
            Обновляет глобальные предпочтения. 
            Ожидается список объектов с полями: category, value, score.
            """
        logger.info("Запрос на обновление глобальных предпочтений")
        try:
            data = request.data
            if not isinstance(data, list):
                return Response({"error": "Expected a list of preferences"}, status=status.HTTP_400_BAD_REQUEST)

            for pref in data:
                category = pref.get("category")
                value = pref.get("value")
                score = pref.get("score")

                if not all([category, value, score]):
                    logger.warning(f"Некорректные данные: {pref}")
                    continue

                # Обновляем или создаём новую глобальную предпочтение
                GlobalPreference.objects.update_or_create(
                    category=category,
                    value=value,
                    defaults={"score": score}
                )

            return Response({"status": "updated"}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.exception(f"Ошибка при обновлении глобальных предпочтений: {e}")
            return Response(
                {"error": "An internal error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )




@api_view(['GET'])
def search_books(request):
    query = request.GET.get('q', '')
    if query:
        # Разбиваем запрос на слова по пробелам
        query_parts = query.split()

        # Строим фильтрацию с учетом всех частей запроса
        books = Book.objects.all()
        
        for part in query_parts:
            books = books.filter(
                Q(title__icontains=part) | 
                Q(author__name__icontains=part) | 
                Q(author__surname__icontains=part)
            )
    else:
        books = Book.objects.none()
    
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)