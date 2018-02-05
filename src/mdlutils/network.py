
import socket

class ClientCloseWarning(Exception):

    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return "ClientCloseWarning : {}".format(self.message)

class ServerCloseWarning(Exception):

    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return "ServerCloseWarning : {}".format(self.message)

class FormatIPError(Exception):

    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return "FormatIPError : {}".format(self.message)

class SocketError(Exception):

    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return "SocketError : {}".format(self.message)

def checkIp(ip):
	if "." not in ip:
		raise FormatIPError("IP incorrectly formated")
	ip_bytes = ip.split(".")
	if len(ip_bytes) != 4:
		raise FormatIPError("Bytes number error")
	for byte in ip_bytes:
		if byte == "":
			raise FormatIPError("Bytes number error")
		try:
			byte = int(byte)
		except:
			raise FormatIPError("Chars detected in IP")
		if byte < 0 or byte > 255:
			raise FormatIPError("Byte {} is wrong".format(byte))

        

def checkPort(port):
	if isinstance(port, str):
		port = int(port)
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			s.bind(("127.0.0.1", port))
		except socket.error as e:
			raise SocketError(e)

def getIpAddress():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	ip = s.getsockname()[0]
	s.close()
	return ip