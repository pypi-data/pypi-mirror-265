class Rating:
    def __init__(self, name:str, rate:float) -> None:
        self.name = name.capitalize()
        self.rate = rate

    def __str__(self) -> str:
        return f"{self.name:<35s}{self.rate:>25.1f}"

    def edit_rating(self, new_name, new_rate):
        self.name = new_name
        self.rate = new_rate

    def to_dict(self):
        return {"name":self.name, "rate":self.rate}