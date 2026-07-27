import os

DEFAULT_THEME = "default"
# Directory of the installed package, so bundled themes are found whether the
# project is run from a source checkout or installed via pip.
PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
THEMES_DIR = os.path.join(PACKAGE_DIR, "themes")
DEFAULT_OUTPUT_DIR = "_build"
