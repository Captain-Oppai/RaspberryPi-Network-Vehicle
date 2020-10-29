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
# This file is meant to be ran on the 'guest', 'client', or 'slave' and contains all the commands 
# and the 'help' table which is sent to the server in the event of a help command received.
#
# This file also maintains the connection with the server and obediently waits for commands, responding with appropriate phrases on completion or returning 'Invalid command'
# in the event of a command being received that is not in the local command list.
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

import socket
import pickle
import RPi.GPIO as GPIO
from time import sleep

# Do note that the client is currently set up to work on a local system meaning that both server and client are being hosted on the same computer.
# If you are to use this program on a external computer the host variable should be replaced with the remote server's IP address.
#
# Ex.
# host = '192.168.1.10'

host = socket.gethostname()
port = 8888

# The robotName variable isn't important and can be anything you'd like, just putting this in for future use with multiple clients and identification is needed.
robotName = 'Robo Boi!'

# GPIO Setup for raspberry pi.
GPIO.setmode(GPIO.BCM)

#   -Assigning variables for the motor control pins and establishing PWM instances (replace these values with the pin # you're using on your setup.)
motor1a = 0
motor1b = 0
motor1enable = 0

motor2a = 0
motor2b = 0
motor2enable = 0

speedInt = 0

#   -Setting up the pins so they are ready to send signals out
GPIO.setup(motor1a, GPIO.OUT)
GPIO.setup(motor1b, GPIO.OUT)
GPIO.setup(motor2a, GPIO.OUT)
GPIO.setup(motor2b, GPIO.OUT)
GPIO.setup(motor1enable, GPIO.OUT)
GPIO.setup(motor2enable, GPIO.OUT)

motor1 = GPIO.PWM(motor1enable, 100)
motor2 = GPIO.PWM(motor2enable, 100)

GPIO.setup(14, GPIO.OUT)

# This help array is sent to the server anytime the 'help' command is sent to the client. Add the commands you'd like to be displayed or don't, let the server user guess.
help = [
    'bye',
    'forward',
    'backwards',
    'right',
    'left',
    'set speed'
    ]

# Establishing the connection to the server as well as making a socket variable.
s = socket.socket()
s.connect((host, port))
print("Connected to server!")

# These are variables used as reference for sending the server back a completion message.
unknown = 'Invalid command!'
received = 'Message received!'
forwardMsg = 'Going forward, Boss!'
backwardsMsg = 'Going backwards, Boss!'
rightMsg = 'Going right, Boss!'
leftMsg = 'Going left, Boss!'

# Simple send function, this will combine the robot's name and the appropriate command message (the cmd variable is the string you'd like to send back to the server.)
def send(cmd):
    sendCmd = robotName + ':' + ' ' + cmd
    s.send(sendCmd.encode())

# These will be the movement commands/functions and any other commands/functions that will be required besides movement.
def forward():
    # There will be more added eventually when I have the motors and have the documentation and modules to use.
    print(forwardMsg)

def backwards():
    # There will be more added eventually when I have the motors and have the documentation and modules to use.
    print(backwardsMsg)

def right():
    # There will be more added eventually when I have the motors and have the documentation and modules to use.
    print(rightMsg)

def left():
    # There will be more added eventually when I have the motors and have the documentation and modules to use.
    print(leftMsg)

def light():
    # Just testing a light on/off on raspberry pi.
    GPIO.output(14, GPIO.HIGH)
    print("On!")
    sleep(5)
    GPIO.output(14, GPIO.LOW)
    print("Off!")


def clientProgram():
    # Making a loop so that the client will constantly take commands.
    while True:
        # Receiving the data from server and decoding it.
        print("Waiting for command...")
        data = s.recv(1024).decode()

        if not data:
            s.close()
            break

        # This function along with the other move functions are just short blocks of if statements to either reference a different function or do something quickly like break the loop.
        if data == "bye":
            print("Goodbye!")
            s.close()
            exit()

        # This will just print out the received command.
        print("From server: " + str(data))

        if data.lower().strip() == 'forward':
            forward()
            send(forwardMsg)
            clientProgram()

        if data.lower().strip() == 'backwards':
            backwards()
            send(backwardsMsg)
            clientProgram()

        if data.lower().strip() == 'right':
            right()
            send(rightMsg)
            clientProgram()

        if data.lower().strip() == 'left':
            left()
            send(leftMsg)
            clientProgram()

        if data.lower().strip() == 'set speed':
            print('Setting speed!')
            send(received)
            speedData = s.recv(1024).decode()
            speedInt = int(speedData)
            send(received)
            clientProgram()

        if data.lower().strip() == 'light':
            light()
            send("Turning on the light boss!")
            clientProgram()
        # In the event of the help command being called we will be using the pickle module to dump our help array and send it over to the server where it is the loaded.
        if data.lower().strip() == 'help':
            s.send(pickle.dumps(help))
            clientProgram()

        # Seems self explanatory.
        print("Invalid command!")
        send(unknown)

    ## data = input(' -> ')

# Eventually might use more functions before the main client program function is called, in the future the clientProgram function might be called else where.
def main():
    clientProgram()

main()

GPIO.cleanup()
