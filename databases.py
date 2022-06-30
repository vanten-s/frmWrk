
class Database:
    def __init(self, id):
        self.id = id
    
    def __hash__(self):
        return self.id

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return self.id

    def __repr__(self):
        return self.id

        

        