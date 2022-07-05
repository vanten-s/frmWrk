

import socket
import threading
import datetime

enable_logging = True
log_file = "log.txt"

def log(func):
    def wrapper(*args, **kwargs):
        if not enable_logging: return func(*args, **kwargs)
        returnVal = func(*args, **kwargs)
        with open(log_file, "a") as f:
            try:
                if len(returnVal) < 100:
                    f.write(f"{func.__name__} was called at {datetime.datetime.now().strftime('%m/%d/%Y, %H:%M:%S')} and returned {returnVal}\n")
                else:
                    f.write(f"{func.__name__} was called at {datetime.datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}\n")
            except TypeError as e:
                f.write(f"{func.__name__} was called at {datetime.datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}\n")    

        return returnVal
    
    return wrapper


def log_string(string):
    if not enable_logging: return string
    with open(log_file, "a") as f:
        f.write(f"{string}\n")
    return string




databases = {}
__using_remote_access = False

"""
Usage:
    CREATE <name> # Creates a new database
    ADDATTRIBUTE <name> <attribute> # Adds an attribute to a database
    ADD <name> <database> # Adds an entry to a database
    LIST # Lists all databases
    GET <entry> <database> <attribute> # Gets an entry from a database
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
    log_string(f"Executing instruction: {instruction}")
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
        return databases[tokens[1]].entrys[tokens[2]].getAttribute(tokens[3]).__str__()

    elif tokens[0] == "SET":
        database = databases[tokens[1]].entrys[tokens[2]].setAttribute(tokens[3], tokens[4])

    else:
        print(instruction)
        return "Invalid instruction"

    return "Success"

def __enable_remote_access(ip, port):
    HOST = ip  # The server's hostname or IP address
    PORT = port        # The port used by the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    while True and __using_remote_access:
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024).decode()

                firstLine = data.split("\n")[0]
                instruction = " ".join(firstLine.split(" ")[1:-1])

                conn.send(executeInstruction(instruction).encode())
                if not data: break
                

    print('Connection closed')

@log
def enable_remote_access(ip, port):
    global __using_remote_access
    __using_remote_access = True
    t = threading.Thread(target=__enable_remote_access, args=(ip, port))
    t.start()
    return "Enabled remote access"

def disable_remote_access():
    global __using_remote_access
    __using_remote_access = False
    return "Disabled remote access"
    

