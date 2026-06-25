from subprocess import run

from __init import chdir
from _docs import ExtInfo, build_dir, docs_dir, langs_args


def _ext(name: str) -> None:
    info = ExtInfo(name)
    run(
        [
            "pybabel",
            "update",
            "--input-file",
            info.pot,
            "--domain",
            info.name,
            "--output-dir",
            info.locales_dir,
            "--init-missing",
            *langs_args,
        ]
    )


def main() -> None:
    with chdir:
        run(["sphinx-intl", "update", "-p", f"{build_dir}/gettext", "-d", f"{docs_dir}/locales", *langs_args])
        _ext("old_version")


if __name__ == "__main__":
    main()
