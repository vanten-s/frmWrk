
import socket
import threading
import datetime
import os

def boron (code: str, path: str) -> str:
    total = []
    none = []

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
            code = code.replace("{" + string + "}", string)
            none.append(string)
            print("{" + string + "}")
            print(code)

    for string in none:
        code = code.replace(string, "{" + string + "}")

    return code


enable_logging = True
log_file = "log.txt"

def log(func):
    def wrapper(*args, **kwargs):
        if not enable_logging: return func(*args, **kwargs)
        returnVal = func(*args, **kwargs)
        try:
            if len(returnVal) < 10:
                log_string(f"[{datetime.datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}] {func.__name__} was called and returned {returnVal}\n")
            else:
                log_string(f"[{datetime.datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}] {func.__name__} was called\n")
        except TypeError as e:
            log_string(f"[{datetime.datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}] {func.__name__} was called\n")

        return returnVal

    return wrapper


def log_string(string):
    global log_file, enable_logging
    if not enable_logging: return
    with open(log_file, "a") as f:
        f.write(f"[{datetime.datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}] {string}\n")

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
                'xml': 'application/xml; charset=\'utf-8\'',
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
    def __init__(self, ip, port, directory, site404="/404.html", event_handler=None, overwrites={}, custom_router=None):
        self.directory = directory
        self.ip = ip
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((ip,port))
        self.threads = []
        self.running = True
        self.site404 = directory + "/404.html"
        self.event_handler = event_handler
        self.overwrites = overwrites
        self.custom_router = custom_router

    def __getContentType(self, path):
        path = path.split(".")[-1]
        if not path in content_type.keys():
            return 'application/octet-stream'

        return content_type[path]

    def __getResponse(self, code, content_type, payload, custom_headers={}):

        response = b'HTTP/1.1 ' + code.encode("utf-8") + b'\n'
        response += b'Content-Type: ' + content_type.encode("utf-8") + b'\n'
        response += b'Content-Length: ' + str(len(payload)).encode("utf-8") + b'\n'
        response += b'server: frmWrk\n'

        for header_key in custom_headers.keys():
            response += header_key.encode("utf-8") + custom_headers[header_key].encode("utf-8") + b'\n'

        response += b'\n'

        response += payload + b'\n\n'

        return response


    def __get(self, path):
        # Remove data after the ?
        original = path
        if "?" in path:
            path = path[:path.index("?")]

        if path == "/":
            path = "/index.html"

        if os.path.isdir(self.directory + path):
            if path.endswith("/"):
                path = path + "/index.html"

            else:
                return self.__getResponse("301 Moved Permanently", self.__getContentType("/index.html"), b'', custom_headers={"location: ": path + "/"})

        if path in self.overwrites.keys():
            return self.__getResponse("200 OK", self.__getContentType(path), self.overwrites[path](original).encode("utf-8"))

        path = self.directory + path

        try:
            with open(path, "rb") as f:
                content = f.read()
                content_type = self.__getContentType(path)
                # if content_type.startswith("text/html"):
                #     content = boron(content.decode('utf-8'), path).encode('utf-8')

                return self.__getResponse("200 OK", content_type, content)

        except FileNotFoundError:
            if "favicon.ico" in path:
                with open(os.path.dirname(os.path.abspath(__file__)) + "/favicon.ico", "rb") as f:
                    content = f.read()
                    return self.__getResponse("200 OK", "image/x-icon", content)

            try:
                print(log_string("404 Not Found: " + path))
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
            self.event_handler(method, (path))

        if self.custom_router:
            return self.custom_router(method, path, {})

        if method == "GET":
            return self.__get(path)

        return "Only GET Requests Supported Yet Sorry."

    def __handleClient(self, c: socket.socket, addr):
        global running
        while True and self.running:
            data = c.recv(1024)
            if not data:
                break

            request = data.decode("utf-8")
            response = self.__handleRequest(request)

            log_string(f"{addr} asked for {request.split(' ')[1]}")

            c.send(response)

        c.close()

    def __startServer(self):
        global running, s

        log_string("Server started on port " + str(self.port))

        while self.running:
            try:
                c, addr = self.s.accept()
                p = threading.Thread(target=self.__handleClient, args=(c, addr))
                p.start()
                self.threads.append(p)
            except Exception as e:
                log_string(e)


    def start(self):
        print("Starting server...")
        self.s.listen(1)
        t = threading.Thread(target=self.__startServer)
        t.start()
        self.main_process = t

    def close(self):
        self.running = False
        print("Closing server...")
        self.s.close()

        for thread in self.threads:
            thread.join()

        self.main_process.join()

        print("Server closed")

