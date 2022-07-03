
class Player:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.role = None
        self.roleAssigned = False

    def assignRole(self, role):
        self.role = role
        self.roleAssigned = True
