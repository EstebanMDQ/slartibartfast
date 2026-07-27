from functools import partial
import http.server
import os
import socketserver
import threading

import typer
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from .generator import generate_site

# File extensions whose changes should trigger a rebuild.
WATCHED_EXTENSIONS = {
    ".md",
    ".yaml",
    ".yml",
    ".html",
    ".htm",
    ".css",
    ".js",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".svg",
    ".webp",
    ".ico",
}

# Coalesce bursts of events (e.g. a single editor save) into one rebuild.
DEFAULT_DEBOUNCE_SECONDS = 0.4


class ReloadEventHandler(FileSystemEventHandler):
    def __init__(
        self,
        path: str,
        output: str,
        debounce_seconds: float = DEFAULT_DEBOUNCE_SECONDS,
    ):
        super().__init__()
        self.path = os.path.abspath(path)
        self.output = os.path.abspath(output)
        self.debounce_seconds = debounce_seconds
        self._timer: threading.Timer | None = None
        self._lock = threading.Lock()

    def should_handle(self, src_path: str) -> bool:
        """Return True if a change to ``src_path`` should trigger a rebuild."""
        abs_path = os.path.abspath(src_path)

        # Ignore events from inside the output directory to avoid a rebuild loop.
        if abs_path == self.output or abs_path.startswith(self.output + os.sep):
            return False

        # Ignore hidden files and anything inside a hidden directory.
        rel = os.path.relpath(abs_path, self.path)
        if any(part.startswith(".") for part in rel.split(os.sep)):
            return False

        # Only rebuild for content-relevant file types.
        ext = os.path.splitext(abs_path)[1].lower()
        return ext in WATCHED_EXTENSIONS

    def _schedule_regeneration(self) -> None:
        with self._lock:
            if self._timer is not None:
                self._timer.cancel()
            self._timer = threading.Timer(self.debounce_seconds, self._regenerate)
            self._timer.daemon = True
            self._timer.start()

    def _regenerate(self) -> None:
        typer.echo("Detected changes, regenerating site...")
        generate_site(self.path, self.output)

    def _on_change(self, event) -> None:
        if event.is_directory:
            return
        if self.should_handle(event.src_path):
            self._schedule_regeneration()

    def on_modified(self, event):
        self._on_change(event)

    def on_created(self, event):
        self._on_change(event)

    def on_moved(self, event):
        self._on_change(event)


def serve(path: str, output: str = "_build", port: int = 8000):
    """Serve the static site locally on the specified port."""
    path = os.path.abspath(path)
    if not os.path.isdir(path):
        typer.echo(f"Error: '{path}' is not a directory")
        raise typer.Exit(code=1)
    output = os.path.abspath(output)

    event_handler = ReloadEventHandler(path, output)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    handler = partial(http.server.SimpleHTTPRequestHandler, directory=output)
    try:
        with socketserver.TCPServer(("", port), handler) as httpd:
            typer.echo(f"Serving static site at http://localhost:{port} from {output}")
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                typer.echo("Shutting down server...")
                httpd.shutdown()
    finally:
        observer.stop()
        observer.join()
