from rest_framework import serializers
from .models import Author, Book, Review
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
        fields = ['username']

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
    