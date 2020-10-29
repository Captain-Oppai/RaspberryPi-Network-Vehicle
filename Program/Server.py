# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Author: Captain Oppai
# Author Discord: Jisatsu#1987
# Github Project Repo: https://github.com/Zachry117/RaspberryPi-Network-Vehicle
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Copyright 2020 Zachry117
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# File description and information:
#
# This project is meant to run on the 'host', 'server', or 'master' and is used to start up the initial connection and send commands to the swarms in question.
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

import socket
import pickle
import time

# If you'd prefer you can always change the port (There may be some rules on what the port range is but I forgot)
# You shouldn't mess with the host variable as the server should bind with it's own ip address.
host = socket.gethostname()
port = 8888

# Creating a socket variable and binding itself to the host address and port. Starts to listen on the bound host and port, waiting for any incoming connections.
s = socket.socket()
s.bind((host, port))
s.listen(2)
print("Server established, waiting for connection...")

# Receive the incoming connection and announce it.
conn, address = s.accept()
print("Connection from: " + str(address))

# Main server program, it loops so commands can be constantly sent to the client(s).
def serverProgram():
    while True:
        # This is where the user will input the command they want, this will be sent to the client as well.
        data = input(' Command -> ')

        # This bye command will send 'bye' to the client and terminate the program.
        if data.lower().strip() == 'bye':
            print("Goodbye!")
            conn.send(data.encode())
            time.sleep(1)
            conn.close()
            exit()

        # This help if statement is used so I can specifically request the array and print it out in console line by line.
        if data.lower().strip() == 'help':
            conn.send(data.encode())
            data = conn.recv(1024)
            help = pickle.loads(data)
            print(*help, sep = "\n") 
            serverProgram()

        if data.lower().strip() == 'set speed':
            print("What speed would you like? (1-100)")
            speedInput = input(' Speed -> ')
            speed = int(speedInput)
            if 1 <= speed <= 100:
                conn.send(data.encode())
                conn.recv(1024)
                conn.send(speedInput.encode())
                conn.recv(1024)
                serverProgram()
            else:
                print('Invalid value!')
                serverProgram()

        # If there are no special server requirements it will send the command straight through to the client.
        conn.send(data.encode())

        # This usually will just be a success message from the client, stating the command that successfully ran.
        data = conn.recv(1024).decode()
        if not data:
            conn.close()
            break

        print("From connected robot, " + str(data))

# Eventually might use more functions before the main server program function is called, in the future the serverProgram function might be called else where.
def main():
    serverProgram()

main()