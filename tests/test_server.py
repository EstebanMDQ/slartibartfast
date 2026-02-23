import os
import time
from unittest.mock import MagicMock, patch

import pytest
import typer

from slartibartfast import generator
from slartibartfast.server import DEBOUNCE_SECONDS, ReloadEventHandler

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def site_dirs(tmp_path):
    """Create a minimal source/output directory pair and return their paths."""
    src = tmp_path / "site"
    src.mkdir()
    out = tmp_path / "site" / "_build"
    out.mkdir()
    return str(src), str(out)


@pytest.fixture
def handler(site_dirs):
    """Return a ReloadEventHandler wired to the tmp site dirs."""
    src, out = site_dirs
    return ReloadEventHandler(src, out)


def _make_event(src_path: str) -> MagicMock:
    """Create a minimal mock filesystem event with the given src_path."""
    event = MagicMock()
    event.src_path = src_path
    return event


# ---------------------------------------------------------------------------
# 1. ReloadEventHandler - path filtering
# ---------------------------------------------------------------------------


@patch("slartibartfast.server.generate_site")
def test_handler_ignores_events_in_output_dir(mock_generate, handler, site_dirs):
    """Events originating inside the output directory must not trigger a rebuild."""
    _, out = site_dirs
    event = _make_event(os.path.join(out, "index.html"))

    handler.on_modified(event)
    handler.on_created(event)

    mock_generate.assert_not_called()


@patch("slartibartfast.server.generate_site")
def test_handler_ignores_event_for_output_dir_itself(mock_generate, handler, site_dirs):
    """An event whose src_path equals the output directory itself is ignored."""
    _, out = site_dirs
    event = _make_event(out)

    handler.on_modified(event)

    mock_generate.assert_not_called()


@patch("slartibartfast.server.generate_site")
def test_handler_triggers_rebuild_for_source_events(mock_generate, handler, site_dirs):
    """Events outside the output directory must trigger generate_site."""
    src, out = site_dirs
    event = _make_event(os.path.join(src, "content.md"))

    handler.on_modified(event)

    mock_generate.assert_called_once_with(src, out)


@patch("slartibartfast.server.generate_site")
def test_on_created_triggers_rebuild(mock_generate, handler, site_dirs):
    """on_created also triggers a rebuild for valid source events."""
    src, out = site_dirs
    event = _make_event(os.path.join(src, "new_page.md"))

    handler.on_created(event)

    mock_generate.assert_called_once_with(src, out)


@patch("slartibartfast.server.generate_site")
def test_on_modified_and_on_created_both_filter_output(
    mock_generate, handler, site_dirs
):
    """Both on_modified and on_created skip events from the output directory."""
    _, out = site_dirs
    event = _make_event(os.path.join(out, "style.css"))

    handler.on_modified(event)
    handler.on_created(event)

    mock_generate.assert_not_called()


# ---------------------------------------------------------------------------
# 2. Debounce behavior
# ---------------------------------------------------------------------------


@patch("slartibartfast.server.generate_site")
def test_debounce_prevents_rapid_rebuilds(mock_generate, handler, site_dirs):
    """Rapid events within the cooldown window result in only one rebuild."""
    src, _ = site_dirs
    event = _make_event(os.path.join(src, "page.md"))

    # First event triggers a rebuild
    handler.on_modified(event)
    assert mock_generate.call_count == 1

    # Immediately fire more events - should be suppressed
    handler.on_modified(event)
    handler.on_created(event)
    assert mock_generate.call_count == 1


@patch("slartibartfast.server.generate_site")
def test_rebuild_after_cooldown(mock_generate, handler, site_dirs):
    """An event after the cooldown period triggers a new rebuild."""
    src, _ = site_dirs
    event = _make_event(os.path.join(src, "page.md"))

    handler.on_modified(event)
    assert mock_generate.call_count == 1

    # Simulate time passing beyond the debounce window
    handler.last_rebuild = time.time() - DEBOUNCE_SECONDS - 0.1

    handler.on_modified(event)
    assert mock_generate.call_count == 2


# ---------------------------------------------------------------------------
# 3. copy_static_directories() - output dir skipping
# ---------------------------------------------------------------------------


def test_copy_static_directories_skips_custom_output_dir(tmp_path):
    """When output dir has a custom name, it is still skipped during copy."""
    src = tmp_path / "site"
    src.mkdir()
    out = tmp_path / "site" / "dist"
    out.mkdir()

    # Create a static directory that should be copied
    images = src / "images"
    images.mkdir()
    (images / "logo.png").write_text("png data", encoding="utf-8")

    # Put a file in the output dir so we can verify it's not copied
    (out / "index.html").write_text("<html></html>", encoding="utf-8")

    dest = tmp_path / "dest"
    dest.mkdir()

    copied = generator.copy_static_directories(str(src), str(dest), output_dir="dist")

    assert copied == 1
    assert (dest / "images").exists()
    assert not (dest / "dist").exists()


# ---------------------------------------------------------------------------
# 4. serve() function setup
# ---------------------------------------------------------------------------


def test_serve_rejects_nonexistent_directory(tmp_path):
    """serve() prints an error and exits when given a non-existent path."""
    from slartibartfast.server import serve

    bad_path = str(tmp_path / "does_not_exist")

    with pytest.raises(typer.Exit) as exc_info:
        serve(bad_path)

    assert exc_info.value.exit_code == 1


@patch("slartibartfast.server.socketserver.TCPServer")
@patch("slartibartfast.server.Observer")
@patch("slartibartfast.server.generate_site")
def test_serve_creates_observer_and_handler(
    mock_generate, mock_observer_cls, mock_tcp, tmp_path
):
    """serve() sets up a watchdog observer and schedules the event handler."""
    site = tmp_path / "site"
    site.mkdir()

    mock_observer = MagicMock()
    mock_observer_cls.return_value = mock_observer

    # Make the TCP server context manager raise KeyboardInterrupt to exit
    mock_server = MagicMock()
    mock_server.__enter__ = MagicMock(return_value=mock_server)
    mock_server.__exit__ = MagicMock(return_value=False)
    mock_server.serve_forever.side_effect = KeyboardInterrupt
    mock_tcp.return_value = mock_server

    from slartibartfast.server import serve

    serve(str(site), output="_build", port=9999)

    # Observer was created and started
    mock_observer_cls.assert_called_once()
    mock_observer.start.assert_called_once()

    # Handler was scheduled on the source directory
    mock_observer.schedule.assert_called_once()
    args, kwargs = mock_observer.schedule.call_args
    assert isinstance(args[0], ReloadEventHandler)
    assert args[1] == str(site)
    assert kwargs.get("recursive", args[2] if len(args) > 2 else None) is True

    # TCP server was created with the right port
    mock_tcp.assert_called_once()
    tcp_args = mock_tcp.call_args[0]
    assert tcp_args[0] == ("", 9999)
