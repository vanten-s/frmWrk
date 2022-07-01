
# dont write bytecode to disk
import sys
sys.dont_write_bytecode = True

import socket
import threading
from decorators import *
import databases


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
    def __init__(self, ip, port, directory):
        self.directory = directory
        self.ip = ip
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((ip,port))
        self.threads = []
        self.running = True
        self.site404 = directory + "/404.html"

    def __getContentType(self, path):
        path = path.split(".")[-1]
        return content_type[path]

    def __getResponse(self, code, content_type, content):
        return b'HTTP/1.1 ' + code.encode("utf-8") + b'\nContent-Type: ' + content_type.encode("utf-8") + b'\nContent-Length: ' + str(len(content)).encode("utf-8") + b'\n\n' + content + b'\n\n'

    def __get(self, path):
        if path == "/":
            path = "/index.html"

        path = self.directory + path
        try:
            with open(path, "rb") as f:
                content = f.read()
                content_type = self.__getContentType(path)
                return self.__getResponse("200 OK", content_type, content)
        
        except FileNotFoundError:
            try:
                with open(self.site404, "rb") as f:
                    content = f.read()
                    content_type = self.__getContentType(self.site404)
                    return self.__getResponse("404 Not Found", content_type, content)
                    
            except FileNotFoundError:
                return self.__getResponse("404 Not Found", "text/html", "404 Not Found")

    
    def __handleRequest(self, request):
        tokens = request.split(" ")
        method = tokens[0]
        path = tokens[1]
        version = tokens[2]

        if method == "GET":
            return self.__get(path)

        return "Hello World"

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



    









