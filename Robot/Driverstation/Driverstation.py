import socket
import pickle
import tkinter as tk
from .Controller import Controller

pollingRateMs = 10
connected = False
client_socket = None
enabled = False

def send_message(client_socket, message):
    client_socket.send(message.encode())

def enable_robot(client_socket, window):
    global enabled
    enabled = True
    window.configure(bg='green')
    send_message(client_socket, "enable")

def disable_robot(client_socket, window):
    global enabled
    enabled = False
    window.configure(bg='red')
    send_message(client_socket, "disable")

def connect_to_server(host, port,window):
    global connected,client_socket
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect to the server
        client_socket.connect((host, port))
        connected = True
        print('Connected to the robot.')
        window.configure(bg='red')

    except ConnectionRefusedError:
        connected = False
        print('Connection refused. Make sure the robot is running.')
        window.configure(bg='grey')

def main():
    global connected,client_socket, enabled

    # Server information
    host = 'localhost'
    port = 11111  # -1 in binary
    controller = Controller()
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def loop():
        if not connected or not enabled:
            window.after(pollingRateMs, loop)
            return
        
        # Send data to the server
        msg = pickle.dumps(controller.getValues())
        # print('sent -',msg)
        client_socket.send(msg)
        window.after(pollingRateMs, loop)

    # Create Tkinter window
    window = tk.Tk()
    window.title("Robot Controller")
    enabled = False
    window.configure(bg='grey')
    window.resizable(False, False)
    window.geometry("100x75")

    # Connect button
    connect_button = tk.Button(window, text="Connect", command=lambda: connect_to_server(host, port,window),width=10).pack()

    # Enable button
    enable_button = tk.Button(window, text="Enable", command=lambda: enable_robot(client_socket,window),width=10).pack()

    # Disable button
    disable_button = tk.Button(window, text="Disable", command=lambda: disable_robot(client_socket,window),width=10).pack()

    window.after(pollingRateMs, loop)
    window.mainloop()

    # Close the socket
    client_socket.close()
    window.configure(bg='grey')
    print('Socket closed.')

if __name__ == '__main__':
    main()
