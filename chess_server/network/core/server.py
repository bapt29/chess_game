import logging
import selectors
import socket
import time

HOST = '0.0.0.0'
PORT = 40405

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')


class Server:
    def __init__(self, host, port):
        # Create the main socket that accepts incoming connections and start
        # listening. The socket is non-blocking.
        self.main_socket = socket.socket()
        self.main_socket.bind((host, port))
        self.main_socket.listen(100)
        self.main_socket.setblocking(False)

        # Create the selector object that will dispatch events. Register
        # interest in read events, that include incoming connections.
        # The handler method is passed in data so we can fetch it in
        # serve_forever.
        self.selector = selectors.DefaultSelector()
        self.selector.register(fileobj=self.main_socket,
                               events=selectors.EVENT_READ,
                               data=self.on_accept)

        # Keeps track of the peers currently connected. Maps socket fd to
        # peer name.
        self.client_list = []

    def on_accept(self, sock, mask):
        # This is a handler for the main_socket which is now listening, so we
        # know it's ready to accept a new connection.
        conn, addr = self.main_socket.accept()
        logging.info('accepted connection from {0}'.format(addr))
        conn.setblocking(False)

        self.client_list.append(conn)
        # Register interest in read events on the new socket, dispatching to
        # self.on_read
        self.selector.register(fileobj=conn, events=selectors.EVENT_READ,
                               data=self.on_read)

    def close_connection(self, conn):
        # We can't ask conn for getpeername() here, because the peer may no
        # longer exist (hung up); instead we use our own mapping of socket
        # fds to peer names - our socket fd is still open.
        logging.info('closing connection to {0}'.format(conn.getpeername()))
        self.client_list.remove(conn)
        self.selector.unregister(conn)
        conn.close()

    def on_read(self, conn, mask):
        # This is a handler for peer sockets - it's called when there's new
        # data.
        try:
            data = conn.recv(1000)
            if data:
                peername = conn.getpeername()
                logging.info('got data from {}: {!r}'.format(peername, data))
                # Assume for simplicity that send won't block
                for client in self.client_list:
                    if client != conn:
                        client.send(data)
            else:
                self.close_connection(conn)
        except ConnectionResetError:
            self.close_connection(conn)

    def serve_forever(self):
        last_report_time = time.time()

        while True:
            # Wait until some registered socket becomes ready. This will block
            # for 200 ms.
            events = self.selector.select(timeout=0.2)

            # For each new event, dispatch to its handler
            for key, mask in events:
                handler = key.data
                handler(key.fileobj, mask)

            # This part happens roughly every second.
            cur_time = time.time()
            if cur_time - last_report_time > 1:
                logging.info('Running report...')
                logging.info('Num active peers = {0}'.format(
                    len(self.client_list)))
                last_report_time = cur_time


if __name__ == '__main__':
    logging.info('starting')
    server = Server(host=HOST, port=PORT)
    server.serve_forever()
