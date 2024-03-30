from statistics import mean


class Movie:
    def __init__(self, name:str, ratings = None) -> None:
        self.name = name.capitalize()
        self.ratings = ratings if ratings else []

    def __str__(self):
        avg = self.get_avg()
        if avg:
            return f"{self.name:<30s}{avg:>25.1f}"
        else:
            avg = "Фильм не оценивался"
            return f"{self.name:<30s}{avg:>25s}"

    def full_movie_info(self):
        print(f"{self.name:^60}")
        for rating in self.ratings:
            print(rating)
        avg = self.get_avg()
        if avg:
            print(f"{'Средняя оценка':<35s}{avg:>25.1f}")
        else:
            avg = "Фильм не оценивался"
            print(f"{'Средняя оценка':<35s}{avg:>25s}")

    def get_avg(self):
        if self.ratings:
            # return mean([rating.rate for rating in self.ratings])
            total = 0
            for rating in self.ratings:
                total += rating.rate
            return total/len(self.ratings)
        else:    
            return 0

    def get_rating(self, user_name):
        for rating in self.ratings:
            if rating.name.lower().strip() == user_name.lower().strip():
                return rating
        return None

    def rate_movie(self, user_name, user_rate):
        try:
            user_rate = float(user_rate)
            if 10 >= user_rate >= 0:
                old_rating = self.get_rating(user_name)
                if old_rating:
                    if user_rate == 0:
                        self.ratings.remove(old_rating)
                        print("Ваша оценка удалена")
                        return True
                    else:
                        old_rating.edit_rating(user_name, user_rate)
                        print("Ваша оценка успешно изменена")
                        return True
                else:
                    if user_rate == 0:
                        print("Вы еще не выставляли оценку этому фильму")
                    else:
                        new_rating = Rating(user_name, user_rate)
                        self.ratings.append(new_rating)
                        print("Ваша оценка успешно добавлена")
                        return True
            else:
                print("Оценка введена не корректно")
        except ValueError:
            print("Оценка введена не корректно, нужно вводить числа")
    
    def to_dict(self):
        ratings_dict = [rating.to_dict() for rating in self.ratings]
        return {"name": self.name, "ratings": ratings_dict}





