class PlayerManager:

    def __init__(self, players):
        self.current_player = players[0]
        self.PLAYERS = players

    def get_current_color(self):
        return self.get_current_player().get_color()

    def get_current_player(self):
        return self.current_player

    def get_next_color(self):
        return self.get_next_player().get_color()

    def get_next_player(self):
        return self.PLAYERS[self.PLAYERS.index(self.current_player) - 1]

    def get_players(self):
        return self.PLAYERS

    def switch_current_player(self):  # Cycles Through Players
        new_player = self.PLAYERS.index(self.current_player) - 1
        self.current_player = self.PLAYERS[new_player]

