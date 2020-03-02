class PlayerManager:

    def __init__(self):
        self.current_player = None
        self.players = []

    def get_current_player(self):
        return self.current_player

    def switch_current_player(self):
        new_player = self.players.index(self.current_player) - 1
        self.current_player = self.players[new_player]