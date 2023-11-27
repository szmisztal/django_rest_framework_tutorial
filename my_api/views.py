from django.contrib.auth.models import User
from rest_framework import viewsets, filters
from my_api.serializers import UserSerializer
from .models import Movie, Review, Actor
from .serializers import MovieSerializer, ReviewSerializer, ActorSerializer
from rest_framework.response import Response
from django.http.response import HttpResponseNotAllowed
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, DjangoModelPermissions

class MovieSetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 10

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class MovieViewSet(viewsets.ModelViewSet):
    serializer_class = MovieSerializer
    filterset_fields = ('title', 'description', 'pub_year')
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ('title', 'description')
    ordering_fields = '__all__'
    ordering = ('-pub_year',)
    pagination_class = MovieSetPagination
    authentication_classes = (TokenAuthentication, )
    permission_classes = (DjangoModelPermissions, )

    def get_queryset(self):
        movies = Movie.objects.all()
        # pub_year = self.request.query_params.get('pub_year', None)
        # id = self.request.query_params.get('id', None)
        # if id:
        #     movie = Movie.objects.filter(id = id)
        #     return movie
        # else:
        #     if pub_year:
        #         movies = Movie.objects.filter(pub_year = pub_year)
        #     else:
        #         movies = Movie.objects.all()
        #movies = Movie.objects.filter(after_premiere = True)
        return movies

    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     title = self.request.query_params.get('title', None)
    #     movies = Movie.objects.filter(title__exact = title)
    #     movies = Movie.objects.filter(title__contains = title)
    #     movies = Movie.objects.filter(pub_year__gte = '2001')
    #     serializer = MovieSerializer(queryset, many = True)
    #     return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        movie = self.get_object()
        serializer = MovieSerializer(movie)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        #if request.user.is_superuser:
        movie = Movie.objects.create(title = request.data['title'],
                                 description = request.data['description'],
                                 after_premiere = request.data['after_premiere'],
                                 pub_year = request.data['pub_year'])

        serializer = MovieSerializer(movie, many = False)
        return Response(serializer.data)
        #else:
        #   return HttpResponseNotAllowed('not allowed')

    def update(self, request, *args, **kwargs):
        movie = self.get_object()
        movie.title = request.data['title']
        movie.description = request.data['description']
        movie.after_premiere = request.data['after_premiere']
        movie.pub_year = request.data['pub_year']
        movie.save()
        serializer = MovieSerializer(movie, many = False)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        movie = self.get_object()
        movie.delete()
        return Response('movie deleted')

    @action(detail = True)
    def premiere(self, request, *args, **kwargs):
        movie = self.get_object()
        movie.after_premiere = True
        movie.save()
        serializer = MovieSerializer(movie, many = False)
        return Response(serializer.data)

    @action(detail = False, methods = ['POST'])
    def premiere_all(self, request, *args, **kwargs):
        movies = Movie.objects.all()
        movies.update(after_premiere = request.data['after_premiere'])
        serializer = MovieSerializer(movies, many = True)
        return Response(serializer.data)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

    @action(detail = True, methods = ['POST'])
    def add(self, request, **kwargs):
        actor = self.get_object()
        movie = Movie.objects.get(id = request.data['movie'])
        actor.movies.add(movie)
        serializer = ActorSerializer(actor, many = False)
        return Response(serializer.data)
