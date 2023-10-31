import logging
import signal
import socket
import sys

from .server import Server
from servers.utils.thread_pool import ThreadPool

class ThreadPoolServer(Server):

    def __init__(self, port: int, folder: str, delay: bool = False):
        self.root = folder
        self.port = port
        self.delay = delay
        signal.signal(signal.SIGINT, self.handle_exit)
        self.thread_pool = ThreadPool(10)

    def run(self):
        self.server_socket = socket.create_server(
            address=("", self.port), family=socket.AF_INET, reuse_port=True
        )
        self.server_socket.listen()

        while True:
            connection, address = self.server_socket.accept()
            logging.info(f"Connection from: {address}")

            task = lambda connection=connection: self.handle_connection(connection)
            self.thread_pool.submit(task)


    def handle_exit(self, sig, frame):
        logging.info("Interrupt detected, shutting down server...")

        self.wait_for_all_threads()    

        self.server_socket.close()
        sys.exit(0)


    def wait_for_all_threads(self):
        self.thread_pool.close()