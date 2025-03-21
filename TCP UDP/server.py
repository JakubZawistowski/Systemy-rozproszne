import socket
import threading

#zrobione 2 pierwsze na 8 punktów

HOST = '127.0.0.1'
PORT = 12345

clients = []
udp_port = PORT
def broadcast(message, sender_socket):
    for client, _ in clients:
        if client != sender_socket:
            try:
                client.send(message.encode())
            except:
                client.close()
                clients.remove((client, _))


def handle_client(client_socket, addr, nickname):
    global clients
    try:
        while True:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            broadcast(f"{nickname}: {message}", client_socket)
    except:
        pass
    finally:
        clients.remove((client_socket, nickname))
        client_socket.close()
        print(f"{nickname} ({addr}) odłączony.")


def udp_server():
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.bind((HOST, udp_port))
    while True:
        data, addr = udp_sock.recvfrom(1024)
        message = data.decode()
        print(f"UDP od {addr}: {message}")
        for client, _ in clients:
            try:
                client.send(f"[UDP] {message}".encode())
            except:
                pass


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"Serwer działa na {HOST}:{PORT}")

    threading.Thread(target=udp_server, daemon=True).start()

    while True:
        client_socket, addr = server.accept()
        nickname = client_socket.recv(1024).decode()

        clients.append((client_socket, nickname))
        print(f"{nickname} ({addr}) dołączył.")

        threading.Thread(target=handle_client, args=(client_socket, addr, nickname)).start()

start_server()
