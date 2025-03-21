import socket
import threading

HOST = '127.0.0.1'
PORT = 12345

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

nickname = input("Podaj swój nick: ")
client.send(nickname.encode())

udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def receive():
    while True:
        try:
            message = client.recv(1024).decode()
            if message:
                print(message)
        except:
            print("Błąd połączenia.")
            client.close()
            break

threading.Thread(target=receive, daemon=True).start()

while True:
    msg = input()
    if msg == "U":
        udp_msg = f"{nickname} wysyła wiadomość UDP\nASCII Art: ✧♡(◕‿◕✿)"
        udp_sock.sendto(udp_msg.encode(), (HOST, PORT))
    else:
        client.send(msg.encode())
