from subprocess import run

from __init import chdir
from _docs import build_dir_lang, docs_dir, lang_args


def main() -> None:
    with chdir:
        run(["sphinx-autobuild", docs_dir, build_dir_lang, *lang_args])


if __name__ == "__main__":
    main()
