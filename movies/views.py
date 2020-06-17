from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import JsonResponse, HttpResponse
import json
import urllib.request
from .models import Movie, Genre, Rating

from .forms import RatingForm

def index(request):
    return render(request, 'movies/index.html')

def search(request):
    client_id = "Rhpsh4RYDE3hQWmTHV0Z"
    client_secret = "qlMewu7URE"

    if request.method == 'GET':
        keyword = request.GET.get('keyword')    
        encText = urllib.parse.quote('{}'.format(keyword))
        url = "https://openapi.naver.com/v1/search/movie?query=" + encText # json 결과
        movie_request = urllib.request.Request(url)
        movie_request.add_header("X-Naver-Client-Id",client_id)
        movie_request.add_header("X-Naver-Client-Secret",client_secret)
        response = urllib.request.urlopen(movie_request)
        rescode = response.getcode()
        if(rescode==200):
            response_body = response.read()
            result = json.loads(response_body.decode('utf-8'))
            movies = result.get('items')
            
            context = {
                'movies': movies,
            }
        else:
            print("Error Code:" + rescode)
    
    return render(request, 'movies/search.html', context)

def detail(request, movie_pk):
    # 기본 상세정보
    movie = get_object_or_404(Movie, pk=movie_pk)
    recommendations = Movie.objects.order_by('-vote_average')
    
    # 평점순 4개 뽑아주기
    recommendation_list = recommendations[:4]

    # 같은 장르 중에서 평점 높은 4개
    # detail 영화의 장르들
    genre_names = []
    for genre in movie.genres.all():
        genre_names.append(genre.name)
    # 장르 수 만큼 반복
    genre_cnt = len(genre_names)

    # 장르별 추천은 최대 3개 장르까지만
    if genre_cnt > 3:
        genre_cnt = 3
    # genre_cnt 만큼만 반복(최대 3번)
    recommend_list1 = []
    recommend_list2 = []
    recommend_list3 = []

    for t in range(genre_cnt):
        for test_movie in recommendations:
            for genre_movie in test_movie.genres.all():
                if t==0:
                    check_genre = genre_names[0]
                elif t==1:
                    check_genre = genre_names[1]
                else:
                    check_genre = genre_names[2]
                if genre_movie.name == check_genre:
                    if t==0:
                        if test_movie not in recommend_list1 and len(recommend_list1) < 5:
                            recommend_list1.append(test_movie)
                    elif t==1:
                        if test_movie not in recommend_list2 and len(recommend_list2) < 5:
                            recommend_list2.append(test_movie)
                    else:
                        if test_movie not in recommend_list3 and len(recommend_list3) < 5:
                            recommend_list3.append(test_movie)
                          



    # 모든 영화에 대해서, movie(detail)의 장르들 중 하나라도 일치하면 list 어팬드
    test_list = []
    for test_movie in recommendations:
        for genre_movie in test_movie.genres.all():
            for check in movie.genres.all():
                if genre_movie.name == check.name:
                    if test_movie not in test_list:
                        test_list.append(test_movie)
    test_list = test_list[:4]

    #recommendations2 = Movie.objects.order_by('-vote_average')
    #for DADADaD in recommendations2
    #recommendations2 = recommendations2[:4]

    context = {
        'movie': movie,
        'genre_cnt' : genre_cnt,
        'genre_names' : genre_names,
        'recommendation_list' : recommendation_list,
        'recommend_list1' : recommend_list1,
        'recommend_list2' : recommend_list2,
        'recommend_list3' : recommend_list3,
    }
    return render(request, 'movies/movie_detail.html', context)

def movie_list(request):
    # movies = Movie.objects.all()
    # context = {
    #     'movies': movies,
    # }
    # return render(request, 'movies/movie_list.html', context)
    return render(request, 'movies/movie_list.html')

def get_movies(request, page):
    movies = Movie.objects.all()[page*30:(page+1)*30]
    # for movie in movies:
    #     movie.poster_path = 
    movies_json = serializers.serialize('json', movies)
    # print(movies_json)
    return HttpResponse(movies_json, content_type="text/json-comment-filtered")

@login_required
def star_review(request, movie_pk, star_point):
    movie = get_object_or_404(Movie, pk=movie_pk)
    form = RatingForm()
    print(movie_pk)
    ratings = Rating.objects.filter(user=request.user)

    if len(ratings):
        for rating in ratings:
            print(rating.movie)
            print(movie)
            if rating.movie == movie:
                rating.point = star_point
                rating.save()
                break
    else:
        rating = form.save(commit=False)
        rating.user = request.user
        rating.movie = movie
        if float(star_point) <= 5:
            rating.point = float(star_point)
            rating.save()

    return JsonResponse({})
