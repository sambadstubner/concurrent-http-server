import logging
from servers.utils.server_parser import ServerParser
from servers.threading_server import ThreadingServer
from servers.thread_pool_server import ThreadPoolServer
from servers.async_server import AsyncServer

if __name__ == "__main__":
    parser = ServerParser()
    if parser.args.concurrency == "thread":
        logging.info("Starting threaded server")
        server = ThreadingServer(parser.args.port, parser.args.folder, parser.args.delay)
    elif parser.args.concurrency == "thread-pool":
        logging.info("Starting thread pool server")
        server = ThreadPoolServer(parser.args.port, parser.args.folder, parser.args.delay)
    elif parser.args.concurrency == "async":
        logging.info("Starting async server")
        server = AsyncServer(parser.args.port, parser.args.folder, parser.args.delay)

    server.run()
