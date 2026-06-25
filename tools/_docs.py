import sys
from itertools import chain

from typing_extensions import Final

docs_dir: Final[str] = "docs"
build_dir: Final[str] = "build"

if len(sys.argv) > 1:
    build_dir_lang = f"{build_dir}/{sys.argv[1]}"
    lang_args = ("-D", f"language={sys.argv[1]}")
    langs_args = tuple(chain(*(("-l", arg) for arg in sys.argv[1:])))
else:
    build_dir_lang = build_dir
    lang_args = ()
    langs_args = ()
