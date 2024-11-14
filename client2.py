# client.py
import socket
import threading
import tkinter as tk

def listen_for_messages(tcp_socket):
    while True:
        try:
            message = tcp_socket.recv(1024).decode()
            if message:
                chat_log.insert(tk.END, message + "\n")
        except:
            print("Disconnected from server.")
            break

def listen_for_broadcasts():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(('', 3000))
    while True:
        message, _ = udp_socket.recvfrom(1024)
        chat_log.insert(tk.END, "Broadcast: " + message.decode() + "\n")

def send_message():
    message = message_entry.get()
    tcp_socket.send(message.encode())
    message_entry.delete(0, tk.END)

# Initialize TCP connection
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.connect(('127.0.0.1', 3000))

# Start threads for TCP and UDP listening
threading.Thread(target=listen_for_messages, args=(tcp_socket,)).start()
threading.Thread(target=listen_for_broadcasts).start()

# UI Setup
root = tk.Tk()
root.title("Chat Client")

chat_log = tk.Text(root, state='normal', height=20, width=50)
chat_log.pack()

message_entry = tk.Entry(root, width=50)
message_entry.pack()

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack()

root.mainloop()
