class Player:
    attempts = 0
    is_win = True
    datetime = None
    def __init__(self, user_id, attempts):
        self.user_id = user_id
        self.attempts = attempts

    def __int__(self):
        return int(self.user_id)

    def __repr__(self):
        return str(self.user_id)

    def __str__(self):
        return str(self.user_id)

    def lose(self, datetime):
        self.is_win = False
        self.datetime = datetime

    def change_attempts(self, true_number):
        self.attempts = self.attempts - 1

    def win(self):
        self.is_win = True

