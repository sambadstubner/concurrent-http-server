import logging
import os
from pathlib import Path
import signal
import socket
import sys
import time
import threading

from .utils import responses

class Server:
    DEFAULT_BUFFER_SIZE = 1024
    DEFAULT_DELAY_TIME = 5.0

    def __init__(self, port: int, folder: str, delay: bool = False):
        self.root = folder
        self.port = port
        self.delay = delay
        signal.signal(signal.SIGINT, self.handle_exit)

    def run(self):
        self.server_socket = socket.create_server(
            address=("", self.port), family=socket.AF_INET, reuse_port=True
        )
        self.server_socket.listen()

        while True:
            connection, address = self.server_socket.accept()
            logging.info(f"Connection from: {address}")

            self.handle_connection(connection)
    

    def handle_connection(self, connection):
        while True:
            try:
                request = connection.recv(self.DEFAULT_BUFFER_SIZE).decode()
                if not request:
                    logging.info("Client disconnected...")
                    break
                while request.find("\r\n\r\n") == -1:
                    request += connection.recv(self.DEFAULT_BUFFER_SIZE).decode()

            except:
                logging.info("Client disconnected")
                break

            if self.delay:
                logging.debug(f"Delaying {self.DEFAULT_DELAY_TIME} seconds")
                time.sleep(self.DEFAULT_DELAY_TIME)

            action, resource = self.parse_request(request)
            logging.debug(f"Action: {action} Resource: {resource}")
            try:
                self.send_response(connection, action, resource)

                logging.debug("Sent")
            except:
                logging.info("Client disconnected")
            break

        connection.close()

    @staticmethod
    def thread_debug(message):
        logging.debug(f"Thread: {threading.current_thread().name} -  {message}")

    @staticmethod
    def parse_request(request: str) -> (str, str):
        Server.thread_debug(f"Request: \n{request}")
        action = Server.get_action_from_request(request)
        resource = Server.get_resource_from_request(request)
        return action, resource

    @staticmethod
    def get_action_from_request(request):
        space_index = request.index(" ")
        return request[:space_index]

    @staticmethod
    def get_resource_from_request(request):
        before_resource = request.index(" ")
        after_resource = request.index(" ", before_resource + 1)
        return request[before_resource + 1 : after_resource]

    def send_response(self, connection: socket, action: int, resource: str) -> int:
        Server.thread_debug(f"Full resource path: {self.root + resource}")
        resource = self.root + resource
        # Currently only supporting GET requests
        if action == "GET":
            if not Path(resource).exists():
                response = responses.get_file_not_found()
                Server.thread_debug(f"Invalid path. Sending: \n{response}")
                connection.send(response.encode())
            else:
                Server.send_resource(connection, resource)
        else:
            response = responses.get_method_not_allowed()
            Server.thread_debug(f"Invalid action. Sending: \n{response}")
            connection.send(response.encode())

    @staticmethod
    def send_resource(connection: socket, resource: str):
        file_size = os.path.getsize(resource)
        Server.thread_debug(f"File size: {file_size}")
        header = Server.create_header(200, "OK", file_size)
        Server.thread_debug(f"Response Header: \n{header}")
        connection.send(header.encode())
        with open(resource, "rb") as file:
            while True:
                chunk = file.read(Server.DEFAULT_BUFFER_SIZE)
                if not chunk:
                    break
                Server.thread_debug(f"Sending chunk: \n{chunk}")
                connection.send(chunk)

    @staticmethod
    def create_header(status_code, status_message, content_length):
        return f"""HTTP/1.0 {status_code} {status_message}
Content-Length: {content_length}

"""

    def handle_exit(self, sig, frame):
        logging.info("Interrupt detected, shutting down server...")

        self.wait_for_all_threads()    

        self.server_socket.close()
        sys.exit(0)

    @staticmethod
    def wait_for_all_threads():
        for thread in threading.enumerate():
            if thread != threading.main_thread():
                Server.thread_debug("Closing thread")
                thread.join()