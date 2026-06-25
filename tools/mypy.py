import sys
from subprocess import run

from __init import chdir

MIN_VERSION = {
    "tools/mypy_docs.toml": 12,
    "tools/mypy_src.toml": 10,
}
MAX_VERSION = 15

FAST = {file: [f"3.{version}"] for file, version in MIN_VERSION.items()}
FULL = {
    file: [f"3.{version}" for version in range(min_version, MAX_VERSION + 1)]
    for file, min_version in MIN_VERSION.items()
}


def main() -> None:
    config = FAST if "--fast" in sys.argv else FULL
    failed: bool = False
    with chdir:
        for file, versions in config.items():
            for version in versions:
                print(f"{file}:{version}", flush=True)
                if run(["mypy", "--config-file", file, "--python-version", version]).returncode != 0:
                    failed = True
                    break
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
