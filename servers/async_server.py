import asyncio
import logging
import os
from pathlib import Path
import sys

from .server import Server
from .utils import responses


class AsyncServer(Server):
    def run(self):
        asyncio.run(self.serve())

    async def serve(self):
        server = await asyncio.start_server(self.handle_client, "0.0.0.0", self.port)
        async with server:
            await server.serve_forever()

    async def handle_client(self, reader, writer):
        addr = writer.get_extra_info("peername")
        logging.debug(f"Connected to {addr}")

        while True:
            try:
                request = (await reader.read(self.DEFAULT_BUFFER_SIZE)).decode()
                if not request:
                    logging.info("Client disconnected...")
                    break
                while request.find("\r\n\r\n") == -1:
                    request += (await reader.read(self.DEFAULT_BUFFER_SIZE)).decode()
            except:
                logging.info("Client disconnected")
                break

            if self.delay:
                logging.debug(f"Delaying {self.DEFAULT_DELAY_TIME} seconds")
                await asyncio.sleep(self.DEFAULT_DELAY_TIME)

            action, resource = self.parse_request(request)
            logging.debug(f"Action: {action} Resource: {resource}")
            try:
                await self.send_response(writer, action, resource)
                await writer.drain()
                logging.debug("Sent")
            except:
                logging.info("Client disconnected")
            break

        writer.close()

    async def send_response(
        self, writer: asyncio.StreamWriter, action: str, resource: str
    ) -> int:
        logging.debug(f"Full resource path: {self.root + resource}")
        resource = self.root + resource
        # Currently only supporting GET requests
        if action == "GET":
            if not Path(resource).exists():
                response = responses.get_file_not_found()
                logging.debug(f"Invalid path. Sending: \n{response}")
                writer.write(response.encode())
            else:
                await self.send_resource(writer, resource)
        else:
            response = responses.get_method_not_allowed()
            logging.debug(f"Invalid action. Sending: \n{response}")
            writer.write(response.encode())

    async def send_resource(self, writer: asyncio.StreamWriter, resource: str):
        file_size = os.path.getsize(resource)
        logging.debug(f"File size: {file_size}")
        header = Server.create_header(200, "OK", file_size)
        logging.debug(f"Response Header: \n{header}")
        writer.write(header.encode())
        with open(resource, "rb") as file:
            while True:
                chunk = file.read(Server.DEFAULT_BUFFER_SIZE)
                if not chunk:
                    break
                logging.debug(f"Sending chunk: \n{chunk}")
                writer.write(chunk)

    def handle_exit(self, sig, frame):
        logging.info("Interrupt detected, shutting down server...")
        sys.exit(0)
