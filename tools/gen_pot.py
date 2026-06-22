from subprocess import run

from __tools_init import chdir
from _const import build_dir, docs_dir


def main():
    with chdir:
        run(["sphinx-build", "-M", "gettext", docs_dir, build_dir])


if __name__ == "__main__":
    main()
