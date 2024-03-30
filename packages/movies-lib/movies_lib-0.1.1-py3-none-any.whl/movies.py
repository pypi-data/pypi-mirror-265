from movie import Movie

class MovieList:
    def __init__(self, movies = None) -> None:
        self.movies = movies if movies else []

    def add_movie(self, movie:Movie):
        self.movies.append(movie)
        print("Фильм успешно добавлен")

    def delete_movie(self, movie:Movie):
        self.movies.remove(movie)
        print("Фильм успешно удален")

    def get_movie(self, name):
        for movie in self.movies:
            if movie.name.lower().strip() == name.lower().strip():
                return movie
        return None

    def print_movies(self):
        print(f"{'Название':<30s}{'Средний рейтинг':>25s}")
        print("-"*55)
        self.movies.sort(key=lambda movie: movie.name)
        for movie in self.movies:
            print(movie)