import socket
import pickle

host = socket.gethostname()
port = 8888

s = socket.socket()

s.bind((host, port))

s.listen(2)
print("Server established, waiting for connection...")
conn, address = s.accept()
print("Connection from: " + str(address))

def server_program():
    while True:
        data = input(' -> ')

        if data.lower().strip() == 'bye':
            print("Goodbye!")
            conn.send(data.encode())
            conn.close()
            exit()

        if data.lower().strip() == 'help':
            conn.send(data.encode())
            data = conn.recv(1024)
            help = pickle.loads(data)
            print(*help, sep = "\n") 
            server_program()

        conn.send(data.encode())

        data = conn.recv(1024).decode()
        if not data:
            conn.close()
            break

        print("From connected robot, " + str(data))

def main():
    server_program()

main()