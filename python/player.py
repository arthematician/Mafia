
class Player:
    def __init__(self, name, id, userInfo):
        self.name = name
        self.id = id
        self.role = None
        self.roleAssigned = False
        self.userInfo = userInfo

    def assignRole(self, role):
        self.role = role
        self.roleAssigned = True
