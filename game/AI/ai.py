class AI:

    def __init__(self, play_as,  time_to_play) -> None:
        self.time_to_play = time_to_play
        self.play_as = play_as

    def switch_player(self, play_as):
        self.play_as = play_as
