import socket
import pygame
import threading

# Initialize Pygame mixer
pygame.mixer.init()

# Server connection details
SERVER_IP = '127.0.0.1'  # Replace with the server's IP address
PORT = 12346

# Create the client socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, PORT))

# Function to play music
def play_music():
    pygame.mixer.music.play()

# Function to handle server commands
def receive_commands():
    while True:
        command = client.recv(1024).decode('utf-8')
        if command == "play":
            print("Received 'play' command")
            play_music()
        elif command == "pause":
            print("Received 'pause' command")
            pygame.mixer.music.pause()
        elif command == "stop":
            print("Received 'stop' command")
            pygame.mixer.music.stop()

# Start listening for commands
threading.Thread(target=receive_commands, daemon=True).start()

# Client input loop
while True:
    user_input = input("Enter command (play, pause, stop): ")
    client.send(user_input.encode('utf-8'))
