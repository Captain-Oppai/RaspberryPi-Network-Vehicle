import socket
import pickle

host = socket.gethostname()
port = 8888

robotName = 'Robo Boi!'

help = [
    'bye',
    'forward', 
    'backwards'
    ]

s = socket.socket()
s.connect((host, port))
print("Connected to server!")

unknown = 'Invalid command!'
forwardMsg = 'Going forward, Boss!'
backwardsMsg = 'Going backwards, Boss!'

def send(cmd):
    sendCmd = robotName + ':' + ' ' + cmd
    s.send(sendCmd.encode())

def forward():
    print('Going forward, Boss!')

def backwards():
    print('Going backwards, Boss!')

def client_program():
    while True:
        print("Waiting for command...")
        data = s.recv(1024).decode()

        if not data:
            s.close()
            break

        if data == "bye":
            print("Goodbye!")
            s.close()
            break

        print("From server: " + str(data))

        if data.lower().strip() == 'forward':
            forward()
            send(forwardMsg)
            client_program()

        if data.lower().strip() == 'backwards':
            backwards()
            send(backwardsMsg)
            client_program()

        if data.lower().strip() == 'help':
            s.send(pickle.dumps(help))
            client_program()

        print("Invalid command!")
        send(unknown)

    ## data = input(' -> ')

def main():
    client_program()

main()
