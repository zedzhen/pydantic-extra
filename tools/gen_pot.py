from subprocess import run

from __init import chdir
from _docs import ExtInfo, build_dir, docs_dir


def _ext(name: str) -> None:
    info = ExtInfo(name)
    run(["pybabel", "extract", info.dir, "--output", info.pot])


def main() -> None:
    with chdir:
        run(["sphinx-build", "-M", "gettext", docs_dir, build_dir])
        _ext("old_version")


if __name__ == "__main__":
    main()
