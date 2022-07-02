from roles import scenarios

class Mafia:
    def __init__(self, scenario):
        assert scenario in {'ranger', 'negotiation'}
        self.scenario = scenario
        self.nPlayers = len(scenarios[scenario])
        self.nRegisteredPlayers = 0
        self.players = []

    def addPlayer(self, player):
        self.players.append(player)

    # @classmethod
    # def zero(cls):
    #     return cls(False)

    def run(self):
        print('The game has just started ...')
