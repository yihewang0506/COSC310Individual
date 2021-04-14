import socket

import main as robot

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = '127.0.0.1'
port = 8888

server.bind((host, port))
server.listen()

con, address = server.accept()

while True:
    data = con.recv(1024)

    if not data:
        break
    # usage prompt
    if '[system init]' == data.decode("utf-8"):
        msg = '1. Get definition from Wikipedia by using `ask wikipedia about {keyword}`\n' \
              '2. Ask question to Wolfram API by typing question\n\n'
        con.sendall(msg.encode("utf-8"))
        continue
    reply = robot.makereply(data.decode("utf-8"))
    con.sendall(reply.encode("utf-8"))
con.close()
