from rest_framework import serializers
from .models import Author, Book, Review, Recommendation, UserPreference, GlobalPreference
from django.contrib.auth.models import User



class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'



class AuthorSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    surname = serializers.CharField()
    birth_date = serializers.DateField()

    class Meta:
        model = Author
        fields = ['name','id', 'surname', 'birth_date']
        
    def create(self, validated_data):
        instance = Author.objects.create(
            name=validated_data.get("name"),
            surname=validated_data.get("surname"),
            birth_date=validated_data.get("birth_date"),
        )
        return instance

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.surname = validated_data.get('surname', instance.surname)
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)
        instance.save()
        return instance
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'is_superuser']

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    class Meta:
        model = Book
        fields = ['id','title', 'publishDate', 'description', 'thumbnail', 'averageRating', 'genre', 'author']

class ReviewSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    class Meta:
        model = Review
        fields = ['id', 'rating', 'comment', 'created_at', 'book', 'user']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'age']




class PreferencesSerializer(serializers.Serializer):
    # Используем DictField для вложенных словарей "значение_атрибута": вес
    # source='...' позволяет сопоставить поле сериализатора с ключом словаря/атрибутом объекта
    # Используем source чтобы обрабатывать ключи с пробелами
    main_genre = serializers.DictField(
        child=serializers.FloatField(), required=False, source='Main Genre'
    )
    sub_genre = serializers.DictField(
        child=serializers.FloatField(), required=False, source='Sub Genre'
    )
    book_type = serializers.DictField(
        child=serializers.FloatField(), required=False, source='Type'  # Имя ключа из ML кода
    )
    author = serializers.DictField(
        child=serializers.FloatField(), required=False, source='Author'
    )

    def to_representation(self, instance):
        """Преобразует Python dict в формат для JSON ответа.
           instance здесь - это словарь вида {'Main Genre': {'Fantasy': 0.8}, ...}
        """
        # Возвращаем как есть, DRF DictField справится. Убедимся, что ключи совпадают с source.
        return instance

    def to_internal_value(self, data):
        """
        Этот метод используется для десериализации данных, поступающих в POST запросе.
        Мы переопределяем его, чтобы правильно обрабатывать ключи JSON с пробелами
        (например, "Main Genre" вместо "main_genre").
        """
        # Маппинг входных ключей на внутренние поля
        attribute_mapping = {
            "Main Genre": "main_genre",
            "Sub Genre": "sub_genre",
            "Type": "book_type",
            "Author": "author"
        }

        validated_data = {}

        for json_key, value in data.items():
            # Проверяем, что ключ есть в нашем маппинге
            if json_key in attribute_mapping:
                # Маппим ключ JSON на внутреннее поле
                internal_key = attribute_mapping[json_key]
                validated_data[internal_key] = value
            else:
                # Если пришел неизвестный ключ, игнорируем или возвращаем ошибку
                raise serializers.ValidationError(f"Unexpected key '{json_key}' in input data.")

        return validated_data




class RecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        fields = '__all__'