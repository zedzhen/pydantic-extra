from __future__ import annotations

from pathlib import Path

from docutils.nodes import Element, Invisible, Node, TextElement
from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective
from sphinx.util.typing import ExtensionMetadata
from typing_extensions import override

ext_name = Path(__file__).name.removesuffix(".py")


class CommentNode(Invisible, Element):
    def __init__(self, comment: Comment):
        nodes: list[Node] = []
        if comment.arguments:
            text = comment.arguments[0]
            node = TextElement(text, text)
            node.source, node.line = comment.get_source_info()
            nodes.append(node)
        nodes.extend(comment.parse_content_to_nodes())
        super().__init__(comment.block_text, *nodes)


class Comment(SphinxDirective):
    has_content = True
    optional_arguments = 1
    final_argument_whitespace = True

    @override
    def run(self) -> list[Node]:
        return [CommentNode(self)]


def setup(app: Sphinx) -> ExtensionMetadata:
    app.add_directive(ext_name, Comment)
    return {
        "version": "1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
