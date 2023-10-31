import logging
import socket
import threading

from .server import Server


class ThreadingServer(Server):

    def run(self):
        self.server_socket = socket.create_server(
            address=("", self.port), family=socket.AF_INET, reuse_port=True
        )
        self.server_socket.listen()

        while True:
            connection, address = self.server_socket.accept()
            logging.info(f"Connection from: {address}")

            connection_thread = threading.Thread(target=self.handle_connection, args=(connection,))
            connection_thread.start()


    