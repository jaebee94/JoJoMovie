from django.shortcuts import render
import urllib.request




def search(request):
    client_id = "Rhpsh4RYDE3hQWmTHV0Z"
    client_secret = "qlMewu7URE"

    if request.method == 'GET':
        keyword = request.GET.get('keyword')    
        encText = urllib.parse.quote(keyword)
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
    
    return render(request, 'search/search.html', context)