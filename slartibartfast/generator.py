from copy import deepcopy
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


def should_process(config: dict) -> bool:
    """Determine if the site should be processed based on config."""
    published = bool(config.get("published", False))
    try:
        publish_date = date.fromisoformat(config.get("publish_date", None))  # type: ignore
    except (ValueError, TypeError):
        publish_date = None
    return published and (publish_date is None or publish_date <= date.today())


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


def collect_pages_metadata(path: str) -> list[dict]:
    """Collect metadata from all markdown files in the path."""
    pages_metadata = []
    for filename in os.listdir(path):
        if filename.endswith(".md"):
            filepath = os.path.join(path, filename)
            with open(filepath, "r") as file:
                page_config, content = _extract_config_header(file.read())

            # Skip pages that shouldn't be processed
            if not should_process(page_config):
                continue

            # Create page metadata
            default_title = filename.replace(".md", "").replace("-", " ").title()
            page_meta = {
                "filename": filename,
                "filepath": filepath,
                "url": "/" + filename.replace(".md", ".html"),
                "title": page_config.get("title", default_title),
                "description": page_config.get("description", ""),
                "date": page_config.get("date", None),
                "publish_date": page_config.get("publish_date", None),
                "nav_order": page_config.get("nav_order", 999),
                "in_nav": page_config.get("in_nav", True),
                "content": content,
                "config": page_config,
            }
            pages_metadata.append(page_meta)

    # Sort pages by nav_order, then by title
    pages_metadata.sort(key=lambda x: (x["nav_order"], x["title"]))
    return pages_metadata


def generate_navigation(pages_metadata: list[dict]) -> list[dict]:
    """Generate navigation menu from pages metadata."""
    nav_items = []
    for page in pages_metadata:
        if page["in_nav"]:
            nav_items.append(
                {
                    "url": page["url"],
                    "title": page["title"],
                    "description": page["description"],
                    "active": False,
                    "nav_order": page["nav_order"],
                }
            )
    sorted(nav_items, key=lambda x: x["nav_order"])
    return nav_items


def generate_sitemap(pages_metadata: list[dict], config: dict) -> str:
    """Generate XML sitemap from pages metadata."""
    base_url = config.get("base_url", "")
    sitemap_entries = []

    for page in pages_metadata:
        url = base_url.rstrip("/") + page["url"]
        # Use publish_date or date, fallback to today
        lastmod = page["publish_date"] or page["date"]
        if lastmod:
            try:
                if isinstance(lastmod, str):
                    lastmod = date.fromisoformat(lastmod)
                lastmod_str = lastmod.isoformat()
            except (ValueError, TypeError):
                lastmod_str = date.today().isoformat()
        else:
            lastmod_str = date.today().isoformat()

        sitemap_entries.append(f"""
    <url>
        <loc>{url}</loc>
        <lastmod>{lastmod_str}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
    </url>""")

    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{"".join(sitemap_entries)}
</urlset>"""
    return sitemap


def generate_site(path: str, output: str) -> dict:
    """Generate the static site from content at path to output directory."""
    config = load_config(path)
    os.makedirs(output, exist_ok=True)

    # Step 1: Collect all pages metadata
    pages_metadata = collect_pages_metadata(path)

    # Step 2: Generate site-wide context
    site_context = {
        "config": config,
        "pages": pages_metadata,
        "sitemap_url": "/sitemap.xml",
    }

    navigation = generate_navigation(pages_metadata)
    # Step 3: Generate sitemap
    sitemap_content = generate_sitemap(pages_metadata, config)
    sitemap_path = os.path.join(output, "sitemap.xml")
    with open(sitemap_path, "w") as file:
        file.write(sitemap_content)

    # Step 4: Generate HTML pages
    stats = {"pages": 0, "errors": 0}
    for page_meta in pages_metadata:
        try:
            template = template_loader(
                config["source_path"],
                config.get("theme", "default"),
                page_meta["config"].get("template", "page.html"),
            )
            current_nav_id = navigation.index(
                [
                    item
                    for item in navigation
                    if item["nav_order"] == page_meta["nav_order"]
                ][0]
            )
            active_navigation = deepcopy(navigation)
            active_navigation[current_nav_id]["active"] = True
            page_html = template.render(
                content=md.render(page_meta["content"]),
                meta=page_meta["config"],
                site=site_context,
                navigation=active_navigation,
            )

            output_filename = page_meta["filename"].replace(".md", ".html")
            output_file = os.path.join(output, output_filename)
            with open(output_file, "w") as file:
                file.write(page_html)
            stats["pages"] += 1

        except Exception as e:
            print(f"Error processing {page_meta['filename']}: {e}")
            stats["errors"] += 1

    return stats
