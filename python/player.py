
class Player:
    def __init__(self, name, id, userInfo):
        self.name = name
        self.id = id
        self.role = None
        self.roleid = None
        self.roleAssigned = False
        self.userInfo = userInfo
        self.roleName = None
        self.teamID = None

    def assignRole(self, roleid, roleName, teamID):
        self.roleid = roleid
        self.roleName = roleName
        self.teamID = teamID
        self.roleAssigned = True
