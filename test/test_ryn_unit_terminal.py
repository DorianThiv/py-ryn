
import socket
import threading
import time
import unittest

class ThreadReception(threading.Thread):

    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connexion = conn # ref du socket de connexion
        self.isrun = True

    def run(self):
        while self.isrun:
            msg = self.connexion.recv(1024).decode()
            if msg == "" or msg.upper() == "FIN":
                self.isrun = False
            print(msg)
        print("Client arrêté Connexion interompue.")

def send_command_no_receive(sock, command):
    sock.send(command.encode())
    time.sleep(1)

def send_command(sock, command):
    sock.send(command.encode())
    print(sock.recv(1024))
    time.sleep(1)


def main():
    unittest.main()

class TerminalTest(unittest.TestCase):

    IP = "172.26.123.5"
    PORT = 1297

    def test_terminal_connection(self):
        host = str(TerminalTest.IP)
        port = int(TerminalTest.PORT)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        send_command_no_receive(sock, "")
        send_command(sock, "hello")
        send_command(sock, "mdlmodule")
        send_command(sock, "mdlterminal")
        send_command(sock, "mdlterminal -w")
        send_command(sock, "mdlterminal -w -a {} -t \"Hello World\" ".format(TerminalTest.IP))
        send_command(sock, "mdlterminal -w -a {} -t \"\" ".format(TerminalTest.IP))
        send_command(sock, "mdldefault -w -t \"Hello World\"")

main()
