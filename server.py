# server.py
import socket
import threading

def handle_client(client_socket, udp_socket, addr):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print(f"Message from {addr}: {message}")
                # Relay the message to all connected clients
                broadcast_tcp(message, client_socket)
        except:
            print(f"Client {addr} disconnected.")
            udp_socket.sendto(f"{addr} left the chat".encode(), ('<broadcast>', 8081))
            break

def broadcast_tcp(message, exclude_socket=None):
    for client in clients:
        if client != exclude_socket:
            try:
                client.send(message.encode())
            except:
                pass

def start_server():
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.bind(('0.0.0.0', 3000))
    tcp_socket.listen(5)

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    print("Server started...")
    while True:
        client_socket, addr = tcp_socket.accept()
        clients.append(client_socket)
        print(f"Client {addr} connected.")
        udp_socket.sendto(f"{addr} joined the chat".encode(), ('<broadcast>', 8081))
        threading.Thread(target=handle_client, args=(client_socket, udp_socket, addr)).start()

clients = []
start_server()
