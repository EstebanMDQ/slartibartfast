import typer

from . import config, server
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
    path: str = typer.Argument(..., help="Path to the site content"),
    output: str = typer.Option(
        default=config.DEFAULT_OUTPUT_DIR,
        help="Output directory for the generated site",
    ),
    port: int = 8000,
):
    """Serve the static site locally on port 8000."""
    server.serve(path, output, port)


if __name__ == "__main__":
    app()
