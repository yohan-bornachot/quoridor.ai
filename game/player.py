class Player:

    def __init__(self, x, y, nb_stick) -> None:
        self.x = x
        self.y = y
        self.nb_stick = nb_stick


    def get_position(self):
        return self.x, self.y

    def get_nb_stick(self):
        return self.nb_stick

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def move_up(self):
        self.y += 1
    
    def move_down(self):
        self.y -= 1

    def move_right(self):
        self.x += 1

    def move_left(self):
        self.x -= 1

    def use_stick(self):
        self.nb_stick -= 1
