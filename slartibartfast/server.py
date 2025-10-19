from functools import partial
import http.server
import os
import socketserver

import typer
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from .generator import generate_site


class ReloadEventHandler(FileSystemEventHandler):
    def __init__(self, path: str, output: str):
        super().__init__()
        self.path = path
        self.output = output

    def on_modified(self, event):
        typer.echo(f"Detected change in {event.src_path}, regenerating site...")
        generate_site(self.path, self.output)

    def on_created(self, event):
        typer.echo(f"Detected new file {event.src_path}, regenerating site...")
        generate_site(self.path, self.output)


def serve(path: str, output: str = "_build", port: int = 8000):
    """Serve the static site locally on the specified port."""
    path = os.path.abspath(path)
    if not os.path.isdir(path):
        typer.echo(f"Error: '{path}' is not a directory")
        raise typer.Exit(code=1)

    event_handler = ReloadEventHandler(path, output)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    handler = partial(http.server.SimpleHTTPRequestHandler, directory=output)
    with socketserver.TCPServer(("", port), handler) as httpd:
        typer.echo(f"Serving static site at http://localhost:{port} from {output}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            typer.echo("Shutting down server...")
            httpd.shutdown()
