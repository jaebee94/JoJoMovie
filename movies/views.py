from django.shortcuts import render, redirect, get_object_or_404
import json
import urllib.request
from .models import Movie

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
    ,``
    return render(request, 'movies/search.html', context)

def detail(request, movie_pk):
    # 평점순 10개 뽑아주기
    recommendation = []
    movies = Movie.objects.order_by('-popularity')
    for i in range(10):
        recommendation.append(movies[i])

    # 기본 상세정보
    movie = get_object_or_404(Movie, pk=movie_pk)
    context = {
        'movie': movie,
        'recommendation': recommendation,
    }
    return render(request, 'movies/movie_detail.html', context)