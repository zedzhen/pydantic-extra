import sys

from _const import build_dir as _build_dir


def lang_from_argv() -> str | None:
    if len(sys.argv) > 1:
        return sys.argv[1]
    return None


def build_dir(lang: str | None) -> str:
    if lang is None:
        return _build_dir
    else:
        return f"{_build_dir}/{lang}"


def args(lang: str | None) -> list[str]:
    if lang is None:
        return []
    else:
        return ["-D", f"language={lang}"]
