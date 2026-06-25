from pathlib import Path

from babel.messages.mofile import write_mo
from babel.messages.pofile import read_po
from docutils.nodes import Node
from sphinx.application import Sphinx
from sphinx.locale import get_translation
from sphinx.util.docutils import SphinxDirective
from sphinx.util.typing import ExtensionMetadata
from typing_extensions import override

ext_name = Path(__file__).parent.name

_ = get_translation(ext_name)

_TEXT_INFO = _("Вы просматриваете документацию для устаревшей версии.")
_TEXT_LINK = _("Документация для последней стабильной версии")

_TEXT = """
.. warning::

   {info} `{link} </{lang}/stable>`_.

"""


class ViewLatest(SphinxDirective):
    @override
    def run(self) -> list[Node]:
        return self.parse_text_to_nodes(_TEXT.format(info=_TEXT_INFO, link=_TEXT_LINK, lang=self.config.language))


def setup(app: Sphinx) -> ExtensionMetadata:
    locale_dir = Path(__file__).resolve().parent / "locales"
    for file in (locale_dir / app.config.language).glob("**/*.po"):
        with file.open("rb") as f_in, file.with_suffix(".mo").open("wb") as f_out:
            write_mo(f_out, read_po(f_in))
    app.add_message_catalog(ext_name, locale_dir)
    app.add_directive(ext_name, ViewLatest)
    return {
        "version": "2.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
