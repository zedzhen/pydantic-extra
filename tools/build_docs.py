from subprocess import run

from __tools_init import chdir
from _const import docs_dir
from _docs import args, build_dir, lang_from_argv


def main(lang: str | None) -> None:
    with chdir:
        run(["sphinx-build", docs_dir, build_dir(lang), *args(lang)])


if __name__ == "__main__":
    main(lang_from_argv())
