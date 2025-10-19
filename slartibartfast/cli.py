from functools import partial
import http.server
import os
import socketserver

import typer

from . import config
from .generator import generate_site

app = typer.Typer(
    help="Slartibartfast: A tiny, fast static site generator.",
    # pretty_exceptions_enable=False,
)


@app.command("generate")
def generate_cmd(
    path: str = typer.Argument(..., help="Path to the site content"),
    output: str = typer.Option(
        default=config.DEFAULT_OUTPUT_DIR,
        help="Output directory for the generated site",
    ),
):
    """Generate the static site."""
    stats = generate_site(path, output)
    # typer.echo(f"Loaded configuration: {config}")
    typer.echo(f"Generating static site from {path} to {output}...")
    typer.echo(
        f"Site generation complete: {stats['pages']} pages created, "
        f"{stats['errors']} errors."
    )


@app.command("serve")
def serve_cmd(
    path: str = typer.Option(
        default=config.DEFAULT_OUTPUT_DIR, help="Path to the generated site"
    ),
    port: int = 8000,
):
    """Serve the static site locally on port 8000."""
    path = os.path.abspath(path)
    if not os.path.isdir(path):
        typer.echo(f"Error: '{path}' is not a directory")
        raise typer.Exit(code=1)

    handler = partial(http.server.SimpleHTTPRequestHandler, directory=path)
    with socketserver.TCPServer(("", port), handler) as httpd:
        typer.echo(f"Serving static site at http://localhost:{port} from {path}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            typer.echo("Shutting down server...")
            httpd.shutdown()


if __name__ == "__main__":
    app()
