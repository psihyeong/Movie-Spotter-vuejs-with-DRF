
from rest_framework.response import Response
from rest_framework.decorators import api_view
# Authentication Decorators
# from rest_framework.decorators import authentication_classes
from rest_framework import status
from django.shortcuts import get_object_or_404, get_list_or_404
from .serializers import MovieSerializer, ReviewSerializer
from .models import Movie, Review
from django.contrib.auth import get_user_model



@api_view(['GET'])
def movie_list(request):
    if request.method == 'GET':
        movies = get_list_or_404(Movie)
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    # elif request.method == 'POST':
    #     serializer = MovieSerializer(data=request.data)
    #     if serializer.is_valid(raise_exception=True):
    #         # serializer.save()
    #         serializer.save(user=request.user)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.method == 'GET':
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
    
    
    # elif request.method == 'DELETE':
    #     movie.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

    # elif request.method == 'PUT':
    #     serializer = MovieSerializer(movie, data=request.data)
    #     if serializer.is_valid(raise_exception=True):
    #         serializer.save()
    #         return Response(serializer.data)


@api_view(['GET','POST'])
def reviews(request, movie_pk):
    # 리뷰 조회
    if request.method == 'GET':
        reviews = get_list_or_404(Review, pk=movie_pk)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    # 리뷰 create
    else:
        movie = get_object_or_404(Movie, pk=movie_pk)
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            serializer.save(movie=movie)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'DELETE', 'PUT'])
def review_detail(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == 'GET':
        serializer = ReviewSerializer(review)
        return Response(serializer.data)

    # 삭제 및 수정 기능
    # 로그인이 상태며
    if request.user.is_authenticated:
        # 리뷰를 쓴 사람이면
        if request.user == review.user:
            if request.method == 'DELETE':
                review.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)

            elif request.method == 'PUT':
                serializer = ReviewSerializer(review, data=request.data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.data)

        else:
            print('')
            # 작성자만 수정할 수 있습니다.
    else:
        print('')
        # 로그인을 해주세요
        

# 내가 쓴 리뷰들을 반환하는 함수
@api_view(['GET'])
def my_reviews(request, my_pk):
    if request.method == 'GET':
        review_list = Review.objects.all().filter(user_id=my_pk)
        serializer = ReviewSerializer(review_list, many=True)
        return Response(serializer.data)
