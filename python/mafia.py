from roles import scenarios
from player import Player

class Mafia:
    def __init__(self, scenario):
        assert scenario in {'ranger', 'negotiation'}
        self.scenario = scenario
        self.nPlayers = len(scenarios[scenario])
        self.nRegisteredPlayers = 0
        self.players = []
        self.newPlayerID = 0

    def addPlayer(self, name):
        id = self.newPlayerID
        player = Player(name, id)
        self.players.append(player)
        self.nRegisteredPlayers = self.nRegisteredPlayers + 1
        self.newPlayerID = self.newPlayerID + 1

    # @classmethod
    # def zero(cls):
    #     return cls(False)

    def run(self):
        print('The game has just started ...')
