from Mafia.python.roles import roles, teams, scenarios
from Mafia.python.player import Player
import random

class Mafia:
    '''
    Mafia game class.
    Stages:
    1 - Waiting for enough players to register
    2 - Role assignment.
    3 - Game running.
    '''

    def __init__(self, scenario, nPlayers, runnerInfo):
        assert scenario in {'ranger', 'negotiation', 'darbar'}
        self.scenario = scenario
        # self.nPlayers = len(scenarios[self.scenario])
        self.nPlayers = nPlayers
        self.runnerInfo = runnerInfo
        self.nRegisteredPlayers = 0
        self.players = []
        self.newPlayerID = 0
        self.enoughPlayersRegistered = False
        self.updateEnoughPlayersStatus()
        self.rolesAssigned = False

    def addPlayer(self, name, userInfo):
        id = self.newPlayerID
        player = Player(name, id, userInfo)
        self.players.append(player)
        self.nRegisteredPlayers = self.nRegisteredPlayers + 1
        self.newPlayerID = self.newPlayerID + 1
        self.updateEnoughPlayersStatus()

    # @classmethod
    # def zero(cls):
    #     return cls(False)

    def updateEnoughPlayersStatus(self):
        if (self.nRegisteredPlayers < self.nPlayers):
            self.enoughPlayersRegistered = False
        else:
            self.enoughPlayersRegistered = True

    def assignRoles(self):
        print('Numbe of registered players:', self.nRegisteredPlayers)
        if (not self.enoughPlayersRegistered):
            print('Not enough players registered yet')
            return False
        print('Assigning roles ...')
        roleList = [roles[roleid] for roleid in scenarios[self.scenario]]
        random.shuffle(roleList)
        for (player, role) in zip(self.players, roleList):
            # print(player.name, role['name'])
            player.assignRole(role)
        self.rolesAssigned = True

    def printRoles(self):
        for player in self.players:
            print(player.name, player.role['name'])

    def run(self):
        if (not self.rolesAssigned):
            print('Roles not assigned yet')
            return False
        print('The game has just started ...')
