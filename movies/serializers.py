from rest_framework import serializers
from rest_framework.views import Response
from .models import MovieRating, Movie, MovieOrder
from users.models import User
from datetime import datetime


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=127)
    duration = serializers.CharField(max_length=10, required=False)
    rating = serializers.ChoiceField(choices=MovieRating.choices, default=MovieRating.DEFAULT, required=False)
    synopsis = serializers.CharField(required=False)
    added_by = serializers.SerializerMethodField(read_only=True)

    def create(self, validated_data: dict):
        return Movie.objects.create(**validated_data)

    def get_added_by(self, obj):
        user = User.objects.get(id=obj.user_id)
        return user.email


class MovieOrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.SerializerMethodField(read_only=True)
    buyed_by = serializers.SerializerMethodField(read_only=True)
    buyed_at = serializers.DateTimeField(read_only=True)
    price = serializers.DecimalField(max_digits=8, decimal_places=2, required=True)

    def create(self, validated_data):
        return MovieOrder.objects.create(**validated_data)

    def get_buyed_by(self, obj):
        # buyer = User.objects.get(id=obj.user_id)
        return obj.user.email

    def get_title(self, obj):
        try:
            movie = Movie.objects.get(id=obj.movie_id)
        except Movie.DoesNotExist:
            return Response({'detail': 'Movie not found'}, 404)
        return obj.movie.title
