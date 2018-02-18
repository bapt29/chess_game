import logging
import selectors
import socket
import time

from chess_server.core.models.client import Client
from chess_server.network.handler.authentication_handler import AuthenticationHandler
from chess_server.network.handler.registration_handler import RegistrationHandler
from chess_server.network.handler.general_handler import GeneralHandler
from chess_server.network.handler.game_handler import GameHandler

HOST = '0.0.0.0'
PORT = 40405

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')


class Server:
    def __init__(self, host, port):
        self.main_socket = socket.socket()
        self.main_socket.bind((host, port))
        self.main_socket.listen(100)
        self.main_socket.setblocking(False)

        self.selector = selectors.DefaultSelector()
        self.selector.register(fileobj=self.main_socket, events=selectors.EVENT_READ, data=self.on_accept)

        self.client_list = {}

        self.authentication_handler = AuthenticationHandler(self)
        self.registration_handler = RegistrationHandler(self)
        self.general_handler = GeneralHandler(self)
        self.game_handler = GameHandler(self)

    def on_accept(self, sock, mask):
        conn, addr = self.main_socket.accept()
        logging.info('accepted connection from {0}'.format(addr))
        conn.setblocking(False)

        self.client_list[conn.fileno()] = Client(conn.getpeername(), socket)
        self.selector.register(fileobj=conn, events=selectors.EVENT_READ, data=self.authentication_handler.on_read)

    def close_connection(self, conn):
        client = self.client_list[conn.fileno()]

        logging.info('closing connection to {0}'.format(client.peer_name))

        del self.client_list[conn.fileno()]
        self.selector.unregister(conn)
        conn.close()

    def serve_forever(self):
        last_report_time = time.time()

        while True:
            events = self.selector.select(timeout=0.02)  # Block 20ms

            # For each new event, dispatch to its handler
            for key, mask in events:
                handler = key.data
                handler(key.fileobj, mask)

            cur_time = time.time()
            if cur_time - last_report_time > 1:
                logging.info('Running report...')
                logging.info('Num active clients = {0}'.format(len(self.client_list)))
                last_report_time = cur_time


if __name__ == '__main__':
    logging.info('starting')
    server = Server(host=HOST, port=PORT)
    server.serve_forever()
