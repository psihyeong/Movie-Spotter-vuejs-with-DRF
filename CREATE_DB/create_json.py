import requests
import json

TMDB_API_KEY = '633fd9754acba9ddc40773b19c562ed9'
# def GET_CREDIT(movie_id):
#     Get_Credit = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key=633fd9754acba9ddc40773b19c562ed9&language=ko').json()

#     actors = []
#     for i in Get_Credit['crew']:
#         if i['known_for_department'] == 'Directing':
#             actors.append(i['name'])
#             break
#     for i in Get_Credit['cast']:
#         actors.append(i['name'])
#         if len(actors) == 4:
#             break
#     return actors


# def GET_VIDEO(movie_id):
#     Get_Video = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key=633fd9754acba9ddc40773b19c562ed9&language=ko').json()
#     if len(Get_Video['results']) == 0 or ('results' not in Get_Video.keys()):
#         return 'novideo'
#     else:
#         return Get_Video['results'][0]['key']



def get_movie_datas():
    total_data = []

    # 1페이지부터 500페이지까지 (페이지당 20개, 총 10,000개)
    for i in range(1, 500):
        request_url = f'https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}&language=ko-KR&page={i}'
        movies = requests.get(request_url).json()

        for movie in movies['results']:
            if movie.get('release_date', ''):
                if movie.get('vote_average') > 7:
                    movie_id = movie['id']
                    Get_Credit = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key=633fd9754acba9ddc40773b19c562ed9&language=ko').json()
                    
                    actors = []
                    for i in Get_Credit['crew']:
                        if i['known_for_department'] == 'Directing':
                            actors.append(i['name'])
                            break
                    for i in Get_Credit['cast']:
                        actors.append(i['name'])
                        if len(actors) == 4:
                            break
                    
                    video = ''
                    Get_Video = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key=633fd9754acba9ddc40773b19c562ed9&language=ko').json()
                    if len(Get_Video['results']) == 0 or ('results' not in Get_Video.keys()):
                        video = 'novideo'
                    else:
                        video = Get_Video['results'][0]['key']



                    if len(actors) < 4 or video == 'novideo':
                        continue


                    fields = {
                        'title': movie['title'],
                        'release_date': movie['release_date'],
                        'adult': movie['adult'],
                        'vote_average': movie['vote_average'],
                        'overview': movie['overview'],
                        'backdrop_path': movie['backdrop_path'],
                        'poster_path': movie['poster_path'],
                        'genres': movie['genre_ids'],
                        'original_language': movie['original_language'],
                        'vote_count': movie['vote_count'],
                        'director' : actors[0],
                        'first_actor' : actors[1],
                        'second_actor' : actors[2],
                        'third_actor' : actors[3],                    
                        'video' : video,
                    }

                    data = {
                        "pk": movie['id'],
                        "model": "movies.movie",
                        "fields": fields
                    }

                   

                    total_data.append(data)
                 

                    print(len(total_data))
            if len(total_data) == 50:
                with open('movies.json', 'w', encoding='UTF-8') as file:
                    file.write(json.dumps(total_data, ensure_ascii=False))
                return


get_movie_datas()
print('?')