import socket
import pickle
import time

class Network:
    def __init__(self):
        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._host = "localhost"
        self._port = 5555
        self._addr = (self._host, self._port)
        self._board = self.connect()
        self._board = pickle.loads(self._board)

    # Getters
    def get_client(self):
        return self._client

    def get_host(self):
        return self._host

    def get_port(self):
        return self._port

    def get_addr(self):
        return self._addr

    def get_board(self):
        return self._board

    # Setters
    def set_client(self, client):
        self._client = client

    def set_host(self, host):
        self._host = host
        self._addr = (self._host, self._port)

    def set_port(self, port):
        self._port = port
        self._addr = (self._host, self._port)

    def set_addr(self, addr):
        self._addr = addr

    def set_board(self, board):
        self._board = board

    def connect(self):
        """
        :param None
        :return: bytes
        """
        
        self._client.connect(self._addr)
        return self._client.recv(4096*8)

    def disconnect(self):
        self._client.close()

    def send(self, data, pick=False):
        """
        :param data: str
        :return: str
        """
        startTime = time.time()
        while time.time() - startTime < 5:
            try:
                if pick:
                    self._client.send(pickle.dumps(data))
                else:
                    self._client.send(str.encode(data))
                reply = self._client.recv(4096*8)
                try:
                    reply = pickle.loads(reply)
                    break
                except Exception as e:
                    print(f"Error while loading reply: {e}")

            except socket.error as e:
                print(f"Socket error while sending client data: {e}")


        return reply


