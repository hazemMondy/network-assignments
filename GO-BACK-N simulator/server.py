"server.py"
import socket
import threading
import time

HEADER = 1024
PORT = 3006
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    """
    1) receive message
    2) check sequence
    2.1) otherwise packet lost nack to the client
    3) ACK
    """
    sequence = 0
    print(f"[NEW CONNECTION] {addr} connected.")
    while True:
        message = conn.recv(HEADER).decode(FORMAT)
        #sequence that i'm waiting for
        if message==DISCONNECT_MESSAGE:
            print(DISCONNECT_MESSAGE)
            break

        if message:
            seq = message.split()

            if int(seq[0]) == sequence:
                sequence +=1
                print(f"[{addr[0]}] {message} [{time.ctime()}] ")
                conn.send(f"ACK {message} received".encode(FORMAT))
            else:
                print(f'NACK resend sequence {sequence} [{time.ctime()}]')
                conn.send(f'NACK resend sequence {sequence} '.encode(FORMAT))
        else:
            print("Transacation complete!")
            break
    conn.close()

def start():
    """
    listen
    every thread handle a client
    """
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print("START TRANSACTION")


def main():
    "main"
    print("[STARTING] server is starting...")
    start()

if __name__=='__main__':
    main()
