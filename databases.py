
databases = []

def executeInstruction(instruction):
    tokens = instruction.split(" ")
    if tokens[0] == "CREATE":
        Database(tokens[1])

    elif tokens[0] == "ADDATTRIBUTE":
        Database.addAttribute(tokens[1], tokens[2])

    elif tokens[0] == "ADD":
        Entry(tokens[1], databases[int(tokens[2])])

    elif tokens[0] == "LIST":
        return databases

    elif tokens[0] == "GET":
        return databases[int(tokens[1])].entrys[int(tokens[2])]

    elif tokens[0] == "SET":
        databases[int(tokens[1])].entrys[int(tokens[2])].setAttribute(tokens[3], tokens[4])

class Database:
    def __init(self, name):
        self.name = name
        self.attributes = []
        self.entrys = {}
        databases.append(self)
    
    def __hash__(self):
        return self.id

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return self.id

    def __repr__(self):
        return self.id

    def addAttribute(self, attribute):
        self.attributes.append(attribute)
        for entry in self.entrys:
            entry.__setAttribute(attribute)

    def getAttribute(self, attribute):
        return self.attributes[attribute]



class Entry:
    def __init__(self, id, parent):
        self.id = id
        self.parent = parent
        self.attributes = {}
        self.parent.entrys[id] = self

    def __setAttribute(self, attribute):
        self.attributes[attribute] = None

    def setAttribute(self, attribute, value):
        if attribute in self.attributes.keys():
            self.attributes[attribute] = value
        else:
            raise Exception("Attribute not found")


    
    
