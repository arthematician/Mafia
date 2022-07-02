from roles import scenarios
from player import Player

class Mafia:
    '''
    Mafia game class.
    Stages:
    1 - Waiting for enough players to register
    2 - Role assignment.
    3 - Game running.
    '''

    def __init__(self, scenario):
        assert scenario in {'ranger', 'negotiation'}
        self.scenario = scenario
        self.nPlayers = len(scenarios[scenario])
        self.nRegisteredPlayers = 0
        self.players = []
        self.newPlayerID = 0
        self.enoughPlayersRegistered = False
        self.updateEnoughPlayersStatus()
        self.rolesAssigned = False

    def addPlayer(self, name):
        id = self.newPlayerID
        player = Player(name, id)
        self.players.append(player)
        self.nRegisteredPlayers = self.nRegisteredPlayers + 1
        self.newPlayerID = self.newPlayerID + 1
        self.updateEnoughPlayersStatus()

    # @classmethod
    # def zero(cls):
    #     return cls(False)

    def updateEnoughPlayersStatus(self):
        if (self.nRegisteredPlayers < len(scenarios[self.scenario])):
            self.enoughPlayersRegistered = False
        else:
            self.enoughPlayersRegistered = True

    def assignRoles(self):
        print('numbe of registered players:', self.nRegisteredPlayers)
        if (not self.enoughPlayersRegistered):
            print('Not enough players registered yet')
            return False
        print('assigning roles')
        self.rolesAssigned = True

    def run(self):
        if (not self.rolesAssigned):
            print('Roles not assigned yet')
            return False
        print('The game has just started ...')
