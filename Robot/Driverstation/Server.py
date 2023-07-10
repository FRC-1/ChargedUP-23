import socket
import pickle
import tkinter as tk
from .Controller import Controller

Controller()

received_controller = None
ready = False

def run_server():
    global received_controller, ready
    # Server information
    host = 'localhost'
    port = 11111

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port
    server_socket.bind((host, port))

    # Listen for incoming connections
    server_socket.listen(1)
    print('Server listening on {}:{}'.format(host, port))

    ready = False
    while True:
        # Accept a client connection
        client_socket, client_address = server_socket.accept()
        print('Accepted connection from:', client_address)
        
        ready = True
        while True:
            # Receive data from the client
            data = client_socket.recv(1024)
            if not data:
                break

            # Deserialize the received object
            #print('received -', pickle.loads(data))
            received_controller = Controller(values = pickle.loads(data))

        # Close the client connection
        client_socket.close()
        print('Client connection closed.')

    # Close the server socket
    server_socket.close()
    print('Server socket closed.')

def GetController() -> Controller:
    return received_controller

def isReady():
    return ready

if __name__ == '__main__':
    run_server()