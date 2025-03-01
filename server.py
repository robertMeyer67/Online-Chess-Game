import socket
from _thread import *
from board import Board
import pickle
import time

socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = "localhost"
port = 5555

serverIP = socket.gethostbyname(server)

try:
    socket.bind((server, port))

except socket.error as e:
    print(f"Socket error while binding to server and port: {str(e)}")

socket.listen()
print("[START] Waiting for a connection")

connections = 0

games = {0:Board(8, 8)}

spectatorIDs = [] 
specs = 0

def read_specs():
    """
    :return: None
    """
        
    global spectatorIDs

    spectatorIDs = []
    try:
        with open("specs.txt", "r") as f:
            for line in f:
                spectatorIDs.append(line.strip())
    except:
        print("[ERROR] No specs.txt file found, creating one...")
        open("specs.txt", "w")


def threaded_client(conn, game, spec=False):
    """
    :param game: Game, spec=False: bool
    :return: None
    """
        
    global pos, games, currentId, connections, specs

    if not spec:
        name = None
        gameBoard = games[game]

        if connections % 2 == 0:
            currentId = "w"
        else:
            currentId = "b"

        gameBoard.start_user = currentId

        # Pickle the object and send it to the server
        dataString = pickle.dumps(gameBoard)

        if currentId == "b":
            gameBoard.set_ready(True)
            gameBoard.set_startTime(time.time())

        conn.send(dataString)
        connections += 1

        while True:
            if game not in games:
                break

            try:
                d = conn.recv(8192 * 3)
                data = d.decode("utf-8")
                if not d:
                    break
                else:
                    if data.count("select") > 0:
                        all = data.split(" ")
                        col = int(all[1])
                        row = int(all[2])
                        color = all[3]
                        gameBoard.select(col, row, color)

                    if data == "winner b":
                        gameBoard.set_winner("b")
                        print("[GAME] Player b won in game", game)
                    if data == "winner w":
                        gameBoard.set_winner("w")
                        print("[GAME] Player w won in game", game)

                    if data == "update moves":
                        gameBoard.update_moves()

                    if data.count("name") == 1:
                        name = data.split(" ")[1]
                        if currentId == "b":
                            gameBoard.set_p2Name = name
                        elif currentId == "w":
                            gameBoard.set_p1Name(name)

                    #print("Recieved board from", currentId, "in game", game)

                    if gameBoard.ready:
                        if gameBoard.get_turn() == "w":
                            gameBoard.set_time1(900 - (time.time() - gameBoard.get_startTime()) - gameBoard.get_storedtime1())
                        else:
                            gameBoard.set_time2(900 - (time.time() - gameBoard.get_startTime()) - gameBoard._storedtime2())

                    sendData = pickle.dumps(gameBoard)
                    #print("Sending board to player", currentId, "in game", game)

                conn.sendall(sendData)

            except Exception as e:
                print(f"Error while recieving and decoding data: {e}")
        
        connections -= 1
        try:
            del games[game]
            print("[GAME] Game", game, "ended")
        except Exception as e:
            print(f"Error while deleting game: {e}")
            pass
        print("[DISCONNECT] Player", name, "left game", game)
        conn.close()

    else:
        availableGames = list(games.keys())
        gameIndex = 0
        gameBoard = games[availableGames[gameIndex]]
        gameBoard.start_user = "s"
        dataString = pickle.dumps(gameBoard)
        conn.send(dataString)

        while True:
            availableGames = list(games.keys())
            gameBoard = games[availableGames[gameIndex]]
            try:
                d = conn.recv(128)
                data = d.decode("utf-8")
                if not d:
                    break
                else:
                    try:
                        if data == "forward":
                            print("[SPECTATOR] Moved Games forward")
                            gameIndex += 1
                            if gameIndex >= len(availableGames):
                                gameIndex = 0
                        elif data == "back":
                            print("[SPECTATOR] Moved Games back")
                            gameIndex -= 1
                            if gameIndex < 0:
                                gameIndex = len(availableGames) -1

                        gameBoard = games[availableGames[gameIndex]]
                    except:
                        print("[ERROR] Invalid Game Recieved from Spectator")

                    sendData = pickle.dumps(gameBoard)
                    conn.sendall(sendData)

            except Exception as e:
                print(f"Error while recieving and decoding data: {e}")

        print("[DISCONNECT] Spectator left game", game)
        specs -= 1
        conn.close()


while True:
    read_specs()
    if connections < 6:
        conn, addr = socket.accept()
        spec = False
        g = -1
        print("[CONNECT] New connection")

        for game in games.keys():
            if games[game].ready == False:
                g=game

        if g == -1:
            try:
                g = list(games.keys())[-1]+1
                games[g] = Board(8,8)
            except:
                g = 0
                games[g] = Board(8,8)

        '''if addr[0] in spectatorIDs and specs == 0:
            spec = True
            print("[SPECTATOR DATA] Games to view: ")
            print("[SPECTATOR DATA]", games.keys())
            g = 0
            specs += 1'''

        print("[DATA] Number of Connections:", connections+1)
        print("[DATA] Number of Games:", len(games))

        start_new_thread(threaded_client, (conn,g,spec))
