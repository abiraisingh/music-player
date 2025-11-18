import socket
import threading
import pygame
import time

# Initialize Pygame mixer
pygame.mixer.init()

# Server configuration
HOST = '0.0.0.0'  # Listen on all network interfaces
PORT = 12346     # Port number

# Create the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"Server listening on {HOST}:{PORT}")

# List to store connected clients
clients = []

# Play the song (for simplicity, use a static song path)
def play_music(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

# Handle client communication
def handle_client(client_socket):
    try:
        while True:
            # Receive message from client
            message = client_socket.recv(1024).decode('utf-8')
            if message == "play":
                print("Playing music")
                play_music("Softly(PagalNew.Com.Se).mp3")  
                # Notify other clients to play
                for client in clients:
                    if client != client_socket:
                        client.send("play".encode('utf-8'))
            elif message == "pause":
                print("Pausing music")
                pygame.mixer.music.pause()
                # Notify other clients to pause
                for client in clients:
                    if client != client_socket:
                        client.send("pause".encode('utf-8'))
            elif message == "stop":
                print("Stopping music")
                pygame.mixer.music.stop()
                # Notify other clients to stop
                for client in clients:
                    if client != client_socket:
                        client.send("stop".encode('utf-8'))
    except:
        print("Client disconnected")
        clients.remove(client_socket)

# Accept new connections
while True:
    client_sock, client_addr = server_socket.accept()
    print(f"New connection from {client_addr}")
    clients.append(client_sock)
    threading.Thread(target=handle_client, args=(client_sock,)).start()
