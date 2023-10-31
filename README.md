# Concurrent HTTP Server

An example of an HTTP server which serves GET requests. It is implemented in three concurrent versions: spawning a thread for every request, using a thread pool, and using the asyncio library.

benchmark.md shows a comparison of the three examples against a single-threaded version.

## Usage
```
usage: http_server.py [-h] [-p PORT] [-v] [-d] [-f FOLDER] [-c {thread,thread-pool,async}]

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  port to bind to
  -v, --verbose         turn on debugging output
  -d, --delay           add a delay for debugging purposes
  -f FOLDER, --folder FOLDER
                        folder from where to serve from
  -c {thread,thread-pool,async}, --concurrency {thread,thread-pool,async}
                        concurrency methodology to use
```