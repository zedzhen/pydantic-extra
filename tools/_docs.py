import sys
from functools import cached_property
from itertools import chain

from typing_extensions import Final

docs_dir: Final[str] = "docs"
build_dir: Final[str] = "build"

lang_args: tuple[str, ...]
langs_args: tuple[str, ...]

if len(sys.argv) > 1:
    build_dir_lang = f"{build_dir}/{sys.argv[1]}"
    lang_args = ("-D", f"language={sys.argv[1]}")
    langs_args = tuple(chain(*(("-l", arg) for arg in sys.argv[1:])))
else:
    build_dir_lang = build_dir
    lang_args = ()
    langs_args = ()


class ExtInfo:
    def __init__(self, name: str):
        self._name = name

    @cached_property
    def name(self) -> str:
        return self._name

    @cached_property
    def dir(self) -> str:
        return docs_dir + f"/ext/{self._name}"

    @cached_property
    def locales_dir(self) -> str:
        return self.dir + "/locales"

    @cached_property
    def pot(self) -> str:
        return self.locales_dir + f"{self._name}.pot"
