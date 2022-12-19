# from Mafia.python.roles import roles, teams, scenarios
from Mafia.python.player import Player
import random
import os
import json

class Mafia:
    '''
    Mafia game class.
    Stages:
    1 - Waiting for enough players to register
    2 - Role assignment.
    3 - Game running.
    '''

    def __init__(self, scenario, nPlayers, runnerInfo):

        scenarios_file = os.path.join(os.getcwd(), 'Mafia', 'python', 'scenarios.json')
        teams_file = os.path.join(os.getcwd(), 'Mafia', 'python', 'teams.json')
        roles_file = os.path.join(os.getcwd(), 'Mafia', 'python', 'roles.json')
        for file in [scenarios_file, teams_file, roles_file]:
            if not os.path.isfile(file):
                self.logger.error(f'Cannot read {file} game config file.')
                # self.clean_exit()

        # read details of the scenarios, teams, roles
        with open(scenarios_file) as json_file:
            self.scenarios_configuratoins = json.loads(json_file.read())
        with open(teams_file) as json_file:
            self.teams_configuratoins = json.loads(json_file.read())
        with open(roles_file) as json_file:
            self.roles_configuratoins = json.loads(json_file.read())

        assert scenario in {'ranger', 'negotiation', 'darbar', 'hunter'}
        self.scenario = scenario
        # self.nPlayers = len(scenarios[self.scenario])
        self.nPlayers = nPlayers
        self.runnerInfo = runnerInfo
        self.nRegisteredPlayers = 0
        self.players = []
        self.newPlayerID = 1
        self.enoughPlayersRegistered = False
        self.updateEnoughPlayersStatus()
        self.rolesAssigned = False
        self.gameSetUpMessageText = ""
        self.gameSetUpMessageID = ""
        self.roles = {}

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
        # print('Numbe of registered players:', self.nRegisteredPlayers)
        if (not self.enoughPlayersRegistered):
            # print('Not enough players registered yet')
            return False
        # print('Assigning roles ...')
        roleList = [self.roles_configuratoins[roleid] for roleid in self.scenarios_configuratoins[self.scenario]['roles']['10']['1']] + [self.roles_configuratoins[roleid] for roleid in self.scenarios_configuratoins[self.scenario]['roles']['10']['2']]
        random.shuffle(roleList)
        for (player, role) in zip(self.players, roleList):
            # print(player.name, role)
            self.roles[role] = player.id
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

    def playerAlreadyRegistered(self, id):
        for player in self.players:
            if (id == player.userInfo['id']):
                return True
        return False

    def setGameSetupUpdateMessageText(self, message):
        self.gameSetUpMessageText = message

    def setGameSetupUpdateMessageID(self, id):
        self.gameSetUpMessageID = id
