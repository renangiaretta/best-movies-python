from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView, Request, Response, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .serializers import MovieSerializer, MovieOrderSerializer
from .permissions import MoviesPermission
from .models import Movie
from rest_framework.pagination import PageNumberPagination


class MovieView(APIView, PageNumberPagination):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, MoviesPermission]

    def post(self, request: Request) -> Response:
        serializer = MovieSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user_id=request.user.id)

        return Response(serializer.data, status.HTTP_201_CREATED)

    def get(self, request: Request) -> Response:
        movies = Movie.objects.all()
        page_result = self.paginate_queryset(movies, request, view=self)
        serializer = MovieSerializer(page_result, many=True)
        return self.get_paginated_response(serializer.data)


class MovieDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, MoviesPermission]

    def delete(self, request: Request, movie_id: int):
        try:
            movie = Movie.objects.get(id=movie_id).delete()
        except Movie.DoesNotExist:
            return Response({'detail': 'Movie not found'}, status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request: Request, movie_id: int) -> Response:
        try:
            movie = Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            return Response({'detail': 'Movie not found'}, status.HTTP_404_NOT_FOUND)
        serializer = MovieSerializer(movie, many=False)

        return Response(serializer.data, status.HTTP_200_OK)


class MovieOrderDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, movie_id: int):
        movie = get_object_or_404(Movie, id=movie_id)
        serializer = MovieOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(movie_id=movie_id, user_id=request.user.id)

        return Response(serializer.data, status.HTTP_201_CREATED)
