import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.absolute()))

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "pydantic-extra"
author = "Ярыкин Евгений"
copyright = f"2026, {author}"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx_refs_alias.ext",
    "sphinx_deprecated_deleted.ext",
    "ext.old_version",
]

templates_path = ["_templates"]
exclude_patterns = ["include/*"]

language = "ru"

# uncomment for an outdated version
# rst_prolog = ".. old_version::"

with open("include/epilog.rst", encoding="utf-8") as f:
    rst_epilog = f.read()
    del f

# Extensions configuration
locale_dirs = ["locales/"]
gettext_compact = True

extlinks = {
    "gh": ("https://github.com/zedzhen/pydantic-extra/issues/%s", "#%s"),
}

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "pydantic": ("https://pydantic.dev/docs/validation/latest", None),
    "sqlalchemy": ("https://docs.sqlalchemy.org/en/20/", None),
}

reference_aliases = {
    "sqlalchemy.Engine": "sqlalchemy.engine.Engine",
    "sqlalchemy.URL": "sqlalchemy.engine.URL",
    "sqlalchemy.AsyncEngine": ("sqlalchemy.ext.asyncio.AsyncEngine", "AsyncEngine"),
    "sqlalchemy.AsyncSession": ("sqlalchemy.ext.asyncio.AsyncSession", "AsyncSession"),
}

deprecated_removed_type = "deprecated"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_static_path = ["_static"]
html_theme_options = {
    "light_css_variables": {
        "color-api-changed": "#605706",
        "color-api-changed-border": "#f0d90f",
        "color-api-deprecated": "var(--color-api-removed)",
        "color-api-deprecated-border": "var(--color-api-removed-border)",
    },
    "dark_css_variables": {
        "color-api-changed": "#b1a10b",
        "color-api-changed-border": "#6e6407",
        "color-api-deprecated": "var(--color-api-removed)",
        "color-api-deprecated-border": "var(--color-api-removed-border)",
    },
}
