import socket
from _thread import start_new_thread
import pickle
# IPv4 on local from ipconfig 192.168.1.113
server = "192.168.1.113"
port = 12345

s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(e)

s.listen(2)  # listen to only 2
print("Waiting for a connection, Server Started")


def threaded_client(conn, player):
    conn.send(pickle.dumps(players[player]))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            players[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]
                print(f"Recieved:{data}")
                print(f"Sending: {reply}")

            conn.sendall(pickle.dumps(reply))
        except:
            print("Something went wrong")
            break

    print("Lost connection")
    conn.close()


# Handling game session
connected = set()
games = {}
n_connections = 0
current_player = 0
while True:
    conn, addr = s.accept()
    print(f"Connected to: {addr}")
    n_connections += 1
    if current_player == 0:
        # new game
        pass
    else:
        # assign to assisting game
        pass

    start_new_thread(threaded_client, (conn, current_player))
    current_player += 1
