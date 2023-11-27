from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Movie, ExtraInfo, Review, Actor

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'required': True, 'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class ExtraInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtraInfo
        fields = ('id', 'time', 'genre')

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        # depth = 1
        # read_only_fields = ('movie', 'id')
    def update(self, instance, validated_data):
        instance.description = validated_data.get('description', instance.description)
        instance.stars = validated_data.get('stars', instance.stars)
        instance.save()
        return instance

class MovieSerializer(serializers.ModelSerializer):
    extra_info = ExtraInfoSerializer(many = False)
    reviews = ReviewSerializer(many = True)
    class Meta:
        model = Movie
        fields = ('id', 'title', 'description', 'after_premiere',
                  'premiere', 'pub_year', 'imdb_rating', 'extra_info', 'reviews')
        read_only_fields = ('extra_info', 'reviews')

class MovieMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('title', 'pub_year')

class ActorSerializer(serializers.ModelSerializer):
    movies = MovieMiniSerializer(many = True, read_only = True)
    class Meta:
        model = Actor
        fields = ('id','name', 'surname', 'movies')

    # def create(self, validated_data):
    #     movies = validated_data["movies"]
    #     del validated_data["movies"]
    #
    #     actor = Actor.objects.create(**validated_data)
    #
    #     for movie in movies:
    #         f = Movie.objects.create(**movie)
    #         actor.movies.add(f)
    #
    #     actor.save()
    #     return actor


