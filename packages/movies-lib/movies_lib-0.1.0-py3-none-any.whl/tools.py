import json
import os

from movies import MovieList
from rating import Rating
from movie import Movie

class Tools:
    @staticmethod
    def get_input(text):
        return input(f"\n{text}\n>")

    @staticmethod
    def get_menu():
        print('''add - добавить фильм
list - список фильмов
find - найти фильм
delete - удалить фильм
rate - оценить фильм
        ''')

    @staticmethod
    def write_file(movie_list, file_name):
        with open(f'../../../../{file_name}', "w", encoding="utf-8") as fp:
            movies = [movie.to_dict() for movie in movie_list.movies]
            json.dump(movies, fp, indent=4)

    @staticmethod
    def read_from_file(file_name):
        if not os.path.exists(f'../../../../{file_name}'):
            f = open(f'../../../../{file_name}', "w", encoding="utf-8")
            f.close()
        with open(f'../../../../{file_name}', "r", encoding="utf-8") as fp:
            movies_json = fp.read()
            movies = []
            if movies_json:
                movies_data = json.loads(movies_json)
                for movie_data in movies_data:
                    ratings = []
                    for rating_data in movie_data['ratings']:
                        ratings.append(Rating(rating_data['name'], float(rating_data['rate'])))
                    movies.append(Movie(movie_data['name'], ratings))
            return MovieList(movies)