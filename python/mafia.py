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

    def __init__(self, scenario, nPlayers, runnerInfo, abstractor):

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
        # abstractors: 'Terminal', 'Telegram'
        self.abstractor = abstractor
        self.nRegisteredPlayers = 0
        self.players = []
        self.newPlayerID = 1
        self.enoughPlayersRegistered = False
        self.updateEnoughPlayersStatus()
        self.rolesAssigned = False
        self.gameSetUpMessageText = ""
        self.gameSetUpMessageID = ""
        self.roles = {}
        # self.gameStarted = False
        # 'preparation', 'blindDay', 'blindNight', 'day', 'night'
        self.phase = 'preparation'
        self.dayCount = 0
        self.nightCount = 0
        self.events = {}

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
        roleList = [roleid for roleid in self.scenarios_configuratoins[self.scenario]['roles']['10']['1']] + [roleid for roleid in self.scenarios_configuratoins[self.scenario]['roles']['10']['2']]

        for i in range(10):
            random.shuffle(roleList)

        for (player, roleid) in zip(self.players, roleList):
            # print(player.name, self.roles_configuratoins[roleid]["name"])
            self.roles[roleid] = player.id
            player.assignRole(roleid, self.roles_configuratoins[roleid]["name"], self.roles_configuratoins[roleid]["teamID"])
        self.rolesAssigned = True
        # print("Roles assigned")

    def printRoles(self):
        for player in self.players:
            if (player.teamID == '1'):
                roleColor = '🟢 '
            else:
                roleColor = '🔴 '
            print(roleColor + str(player.id) + '- ' + player.name, player.roleName)

    def developPhase(self):
        if (self.phase == 'preparation'):
            self.phase = 'blindDay'
        elif (self.phase == 'blindDay'):
            self.phase = 'blindNight'
        elif (self.phase == 'blindNight' or self.phase == 'night'):
            self.phase = 'day'
            self.dayCount += 1
        elif (self.phase == 'day'):
            self.phase = 'night'
            self.nightCount += 1
            self.events[self.phase + '_' + str(self.nightCount)] = {}

    def playerAlreadyRegistered(self, id):
        for player in self.players:
            if (id == player.userInfo['id']):
                return True
        return False

    def setGameSetupUpdateMessageText(self, message):
        self.gameSetUpMessageText = message

    def setGameSetupUpdateMessageID(self, id):
        self.gameSetUpMessageID = id

    def act(self, act, playerID, actData):
        self.events[self.phase + '_' + str(self.nightCount)]['act' + '_' + act] = {
            'actor': playerID,
            'actData': actData
        }

    def process(self, process):
        # print(self.events)
        # print(process)
        if (process == 'capting'):
            targetedPlayerIDs = []
            protectedPlayerIDs = []

            # Check if the act of this event's actor is gotten
            if (self.events[self.phase + '_' + str(self.nightCount)].get('act' + '_' + self.scenarios_configuratoins[self.scenario]['events'][self.phase]['processes'][process]['actor']) != None):
                targetedPlayerIDs = self.events[self.phase + '_' + str(self.nightCount)]['act' + '_' + self.scenarios_configuratoins[self.scenario]['events'][self.phase]['processes'][process]['actor']]['actData']

            # Check if the act of this event's protector is gotten
            if (self.events[self.phase + '_' + str(self.nightCount)].get('act' + '_' + self.scenarios_configuratoins[self.scenario]['events'][self.phase]['processes'][process]['protector']) != None):
                protectedPlayerIDs = self.events[self.phase + '_' + str(self.nightCount)]['act' + '_' + self.scenarios_configuratoins[self.scenario]['events'][self.phase]['processes'][process]['protector']]['actData']

            blockedPlayerIDs = list(set(targetedPlayerIDs) - set(protectedPlayerIDs))

            if (blockedPlayerIDs):
                for playerid in blockedPlayerIDs:
                    print('player number ' + str(playerid) + ', ' + self.players[playerid-1].roleName + ' of the game, is blocked')

            self.events[self.phase + '_' + str(self.nightCount)]['process' + '_' + process] = {
                'processData': blockedPlayerIDs
            }
        elif (process == 'decideToShotOrNato'):

            decision = None

            # Check if the act of this event's actor is gotten
            if (self.events[self.phase + '_' + str(self.nightCount)].get('act' + '_' + self.scenarios_configuratoins[self.scenario]['events'][self.phase]['processes'][process]['actor']) != None):
                decision = self.events[self.phase + '_' + str(self.nightCount)]['act' + '_' + self.scenarios_configuratoins[self.scenario]['events'][self.phase]['processes'][process]['actor']]['actData'][0]

            self.events[self.phase + '_' + str(self.nightCount)]['process' + '_' + process] = {
                'processData': decision
            }

        # print(self.events[])

    def roleInGame(self, roleid):
        exists = False
        id = None
        for player in self.players:
            # print(player.id, player.name, player.roleid, player.roleName, player.teamID, player.roleAssigned)
            if (player.roleid == roleid):
                exists = True
                id = player.id
        return exists, id
