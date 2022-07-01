

import decorators

databases = {}

"""
Usage:
    CREATE <name> # Creates a new database
    ADDATTRIBUTE <name> <attribute> # Adds an attribute to a database
    ADD <name> <database> # Adds an entry to a database
    LIST # Lists all databases
    GET <entry> <database> # Gets an entry from a database
    SET <entry> <database> <attribute> <value> # Sets an attribute of an entry in a database


"""

def help():
    return "Usage: CREATE <name> # Creates a new database\nADDATTRIBUTE <name> <attribute> # Adds an attribute to a database\nADD <name> <database> # Adds an entry to a database\nLIST # Lists all databases\nGET <entry> <database> # Gets an entry from a database\nSET <entry> <database> <attribute> <value> # Sets an attribute of an entry in a database"


class Database:
    def __init__(self, name):
        self.name = name
        self.attributes = []
        self.entrys = {}
        databases[name] = self
    
    def __hash__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def addAttribute(self, attribute):
        self.attributes.append(attribute)
        for entry in self.entrys:
            entry.__setAttribute(attribute)

    def getAttribute(self, attribute):
        return self.attributes[attribute]



class Entry:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.attributes = {attr:None for attr in parent.attributes}
        self.parent.entrys[name] = self

    def __hash__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return self.attributes.__str__()

    def __repr__(self):
        return self.name + " with " + self.attributes.__str__()

    def __setAttribute(self, attribute):
        self.attributes[attribute] = ""

    def setAttribute(self, attribute, value):
        if attribute in self.attributes.keys():
            self.attributes[attribute] = value
        else:
            raise Exception("Attribute not found")

    def getAttribute(self, attribute):
        if attribute in self.attributes.keys():
            return self.attributes[attribute]
        else:
            raise Exception("Attribute not found")


def executeInstruction(instruction):
    tokens = instruction.split(" ")
    decorators.log_string(f"Executing instruction: {instruction}")
    if tokens[0] == "CREATE":
        database = Database(tokens[1])
        return database

    elif tokens[0] == "ADDATTRIBUTE":
        databases[tokens[1]].addAttribute(tokens[2])

    elif tokens[0] == "ADD":
        Entry(tokens[1], databases[tokens[2]])

    elif tokens[0] == "LIST":
        if len(databases) == 0:
            return "No databases"
        
        if len(tokens) == 2:
            return databases[tokens[1]].entrys

        if len(tokens) == 3:
            return databases[tokens[1]].entrys[tokens[2]]

        return databases

    elif tokens[0] == "GET":
        return databases[tokens[1]].entrys[tokens[2]].getAttribute(tokens[3])

    elif tokens[0] == "SET":
        databases[tokens[1]].entrys[tokens[2]].setAttribute(tokens[3], tokens[4])

    else:
        return "Invalid instruction"
    
    
