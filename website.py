
import socket
import threading
import datetime
import os

def boron (code: str, path: str) -> str:
    total = []

    while "{" in code and "}" in code:
        startIndex = code.index("{")
        endIndex = code.index("}")
        try:
            string = code[startIndex+1:endIndex]
            ip = string.split(":")[0]
            port = int(string.split(":")[1])
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            addr = (ip, port)
            print(addr)
            s.connect(addr)
            s.send((string.split(":")[2] + " " + path).encode('utf-8'))
            response = s.recv(1024).decode()
            s.close()
            code = code.replace("{" + string + "}", response)
            print("{" + string + "}")
            print(code)

        except Exception as e:
            print(e)
            code = code.replace("{" + string + "}", "")
            print("{" + string + "}")
            print(code)
    
    '''
    for token in code.split():
        if token.startswith("{") and token.endswith("}"):
            token = token[1:-1]
            ip = token.split(":")[0]
            port = int(token.split(":")[1])
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            addr = (ip, port)
            print(addr)
            s.connect(addr)
            s.send((token.split(":")[2] + " " + path).encode())
            response = s.recv(1024).decode()
            total.append(response)
            s.close()

        else:
            total.append(token)
    '''

    print("Done Computing!")

    return code


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




AASCI_404_NOT_FOUND = """

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="author" content="">
</head>
<body>

    <h1>404 Not Found</h1>
 <pre style="font-size: xx-large;">
   _  _    ___  _  _                 _      __                      _   
  | || |  / _ \| || |               | |    / _|                    | |  
  | || |_| | | | || |_   _ __   ___ | |_  | |_ ___  _   _ _ __   __| |  
  |__   _| | | |__   _| | '_ \ / _ \| __| |  _/ _ \| | | | '_ \ / _` |  
     | | | |_| |  | |   | | | | (_) | |_  | || (_) | |_| | | | | (_| |  
     |_|  \___/   |_|   |_| |_|\___/ \__| |_| \___/ \__,_|_| |_|\__,_|</pre> 
                                                                         
</body>

"""

content_type = {
                'html': 'text/html; charset=\'utf-8\'', 
                'css': 'text/css; charset=\'utf-8\'', 
                'js': 'application/javascript; charset=\'utf-8\'', 
                'png': 'image/png', 
                'jpg': 'image/jpeg', 
                'jpeg': 'image/jpeg', 
                'gif': 'image/gif',
                'ico': 'image/x-icon',
                'svg': 'image/svg+xml',
                'json': 'application/json; charset=\'utf-8\'',
                'txt': 'text/plain; charset=\'utf-8\'',
                'pdf': 'application/pdf',
                'zip': 'application/zip',
                'rar': 'application/x-rar-compressed',
                '7z': 'application/x-7z-compressed',
                'doc': 'application/msword',
                'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'xls': 'application/vnd.ms-excel',
                'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                'ppt': 'application/vnd.ms-powerpoint',
                'pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
                'mp3': 'audio/mpeg',
                'wav': 'audio/x-wav',
                'mp4': 'video/mp4',
                'm4v': 'video/x-m4v',
                'mov': 'video/quicktime',
                'wmv': 'video/x-ms-wmv',
                'flv': 'video/x-flv',
                'avi': 'video/x-msvideo',
                'mkv': 'video/x-matroska',
                'm3u': 'application/x-mpegURL',
                'm3u8': 'application/vnd.apple.mpegurl',
                'ts': 'video/MP2T',
                '3gp': 'video/3gpp',
                '3g2': 'video/3gpp2',
                'mpd': 'video/vnd.mpeg.dash.mpd',
                'mp4': 'video/mp4',
                'webm': 'video/webm',
                'ogv': 'video/ogg',
                'ogm': 'video/ogg',
                'ogg': 'video/ogg',
                'ogx': 'application/ogg',
                'oga': 'audio/ogg',
                'spx': 'audio/ogg',
                'opus': 'audio/ogg',
                'flac': 'audio/flac'
}

class WebServer:
    def __init__(self, ip, port, directory, site404="/404.html", event_handler=None):
        self.directory = directory
        self.ip = ip
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((ip,port))
        self.threads = []
        self.running = True
        self.site404 = directory + "/404.html"
        self.event_handler = event_handler

    def __getContentType(self, path):
        path = path.split(".")[-1]
        return content_type[path]

    def __getResponse(self, code, content_type, content):

        response = b'HTTP/1.1 ' + code.encode("utf-8") + b'\n'
        response += b'Content-Type: ' + content_type.encode("utf-8") + b'\n'
        response += b'Content-Length: ' + str(len(content)).encode("utf-8") + b'\n\n'
        response += content + b'\n\n'

        return response


    def __get(self, path):
        # Remove data after the ?
        if "?" in path:
            path = path[:path.index("?")]
        
        print(path)

        if path == "/":
            path = "/index.html"
        
        path = self.directory + path

        print(path)

        try:
            with open(path, "rb") as f:
                content = f.read()
                content_type = self.__getContentType(path)
                if content_type.startswith("text/html"):
                    print("Executing Connection")
                    content = boron(content.decode('utf-8'), path).encode('utf-8')

                return self.__getResponse("200 OK", content_type, content)
        
        except FileNotFoundError:
            if "favicon.ico" in path:
                print("Favicon not found")
                with open(os.path.dirname(os.path.abspath(__file__)) + "/favicon.ico", "rb") as f:
                    content = f.read()
                    return self.__getResponse("200 OK", "image/x-icon", content)

            try:
                with open(self.site404, "rb") as f:
                    content = f.read()
                    content_type = self.__getContentType(self.site404)
                    return self.__getResponse("404 Not Found", content_type, content)
                    
            except FileNotFoundError:
                return self.__getResponse("404 Not Found", "text/html; charset=\"utf-8\"", AASCI_404_NOT_FOUND.encode("utf-8"))

    
    def __handleRequest(self, request):
        tokens = request.split(" ")
        method = tokens[0]
        path = tokens[1]
        version = tokens[2]

        if self.event_handler:
            self.event_handler(method, (path, version))
        
        if method == "GET":
            return self.__get(path)

        return "Only GET Requests Supported Yet Sorry."

    def __handleClient(self, c: socket.socket, addr):
        print("Handling client...")
        global running
        while True and self.running:
            data = c.recv(1024)
            if not data:
                break

            request = data.decode("utf-8")
            response = self.__handleRequest(request)

            log_string(f"{addr} asked for {request.split(' ')[1]}")            
            print(f"{addr} asked for {request.split(' ')[1]}")

            c.send(response)
        
        print("Closing client connection...")
        c.close()

    def __startServer(self):
        global running, s

        print("Server started on port " + str(self.port))

        while self.running:
            print("Waiting for connection...")
            c, addr = self.s.accept()
            print("Got connection from", addr)
            self.__handleClient(c, addr)

        

    @log
    def start(self):
        print("Starting server...")
        self.s.listen(1)
        t = threading.Thread(target=self.__startServer)
        t.start()
        self.threads.append(t)

    @log
    def close(self):
        self.running = False
        print("Closing server...")
        for t in self.threads:
            t.join()

        self.s.close()
        print("Server closed")



    









