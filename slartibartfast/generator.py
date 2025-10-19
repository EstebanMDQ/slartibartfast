from datetime import date
import os

from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from markdown_it import MarkdownIt
from mdit_py_plugins.footnote import footnote_plugin
from mdit_py_plugins.front_matter import front_matter_plugin
import yaml

from . import config

md = (
    MarkdownIt("commonmark", {"breaks": True, "html": True})
    .use(front_matter_plugin)
    .use(footnote_plugin)
    .enable("table")
)


def load_config(path: str) -> dict:
    """Load configuration from a given path."""
    configfile = os.path.join(path, "_config.yaml")
    if not os.path.isfile(configfile):
        raise FileNotFoundError(f"Configuration file not found at {configfile}")
    with open(configfile, "r") as file:
        config = yaml.safe_load(file)
        config["source_path"] = path
    return config


def _extract_config_header(content: str) -> tuple[dict, str]:
    """Extract YAML front matter from content."""
    if content.startswith("---"):
        end = content.find("---", 3)
        if end != -1:
            front_matter = content[3:end].strip()
            return (yaml.safe_load(front_matter), content[end + 3 :].lstrip())
    return ({}, content)


def should_process(config:dict) -> bool:
    """Determine if the site should be processed based on config."""
    published = config.get("published", False)
    publish_date = config.get("publish_date", None)
    return published is bool and published and (publish_date is None or publish_date <= date.today())

def template_loader(source_path: str, theme: str, template_name: str):
    """Load a Jinja2 template from themes/<theme>/<template_name>.

    If template_name contains a slash (e.g. "other_theme/page.html"), the
    first path segment will be treated as the theme name and override the
    `theme` argument.
    """

    source_theme_dir = os.path.join(source_path, theme)
    theme_dir = os.path.join(config.THEMES_DIR, theme)
    if not os.path.isdir(theme_dir) and not os.path.isdir(source_theme_dir):
        raise FileNotFoundError(f"Theme not found: {theme}")

    env = Environment(loader=FileSystemLoader([source_theme_dir, theme_dir]))
    try:
        return env.get_template(template_name)
    except TemplateNotFound as exc:
        raise TemplateNotFound(
            f"Template '{template_name}' not found in theme '{theme}'"
        ) from exc


def generate_page(content: str, config: dict) -> str:
    """Generate a page by applying a template to content."""
    page_config, content = _extract_config_header(content)
    template = template_loader(
        config["source_path"],
        config.get("theme", "default"),
        page_config.get("template", "page.html"),
    )
    return template.render(content=md.render(content), meta=page_config)


def generate_site(path: str, output: str) -> dict:
    """Generate the static site from content at path to output directory."""
    config = load_config(path)
    os.makedirs(output, exist_ok=True)
    stats = {"pages": 0, "errors": 0}
    for filename in os.listdir(path):
        if filename.endswith(".md"):
            with open(os.path.join(path, filename), "r") as file:
                content = file.read()
            page = generate_page(content, config)
            output_file = os.path.join(output, filename.replace(".md", ".html"))
            with open(output_file, "w") as file:
                file.write(page)
            stats["pages"] += 1

    return stats
