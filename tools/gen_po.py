import sys
from itertools import chain
from subprocess import run

from __tools_init import chdir
from _const import build_dir, docs_dir


def main():
    with chdir:
        l_arg = chain(*(("-l", arg) for arg in sys.argv[1:]))

        run(["sphinx-intl", "update", "-p", f"{build_dir}/gettext", "-d", f"{docs_dir}/locales", *l_arg])


if __name__ == "__main__":
    main()
