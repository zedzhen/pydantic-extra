from subprocess import run

from __init import chdir
from _docs import build_dir, docs_dir


def main():
    with chdir:
        run(["sphinx-build", "-M", "gettext", docs_dir, build_dir])


if __name__ == "__main__":
    main()
