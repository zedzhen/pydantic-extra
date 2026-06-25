from subprocess import run

from __init import chdir
from _docs import build_dir, docs_dir, langs_args


def main():
    with chdir:
        run(["sphinx-intl", "update", "-p", f"{build_dir}/gettext", "-d", f"{docs_dir}/locales", *langs_args])


if __name__ == "__main__":
    main()
