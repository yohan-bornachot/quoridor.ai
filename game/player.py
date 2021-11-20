class Player:

    def __init__(self, i, j, nb_walls) -> None:
        self.i = i
        self.j = j
        self.nb_walls = nb_walls

    def possible_right(self, walls):
        pass #TODO

    def possible_left(self, walls):
        pass #TODO

    def possible_up(self, walls):
        pass #TODO

    def possible_down(self, walls):
        pass #TODO

    def get_position(self):
        return self.i, self.j

    def get_nb_stick(self):
        return self.nb_walls

    def set_position(self, i, j):
        self.x = i
        self.y = j

    def move_up(self):
        self.i += 1
    
    def move_down(self):
        self.i -= 1

    def move_right(self):
        self.j += 1

    def move_left(self):
        self.j -= 1

    def use_stick(self):
        self.nb_walls -= 1
