class PlayerManager:

    def __init__(self, players):
        self.current_player = None
        self.PLAYERS = players

    def get_current_player(self):
        return self.current_player

    def switch_current_player(self):  # Cycles Through Players
        new_player = self.PLAYERS.index(self.current_player) - 1
        self.current_player = self.PLAYERS[new_player]