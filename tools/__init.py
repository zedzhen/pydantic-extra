__all__ = ["base_dir", "chdir"]

import sys
from pathlib import Path
from types import TracebackType

if sys.version_info >= (3, 11):
    from contextlib import chdir as _chdir
else:
    from os import chdir as _os_chdir, getcwd as _os_getcwd

    class _chdir:
        _old: list[str]

        def __init__(self, path: Path):
            self._path = path
            self._old = []

        def __enter__(self) -> None:
            self._old.append(_os_getcwd())
            _os_chdir(self._path)

        def __exit__(
            self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None
        ) -> None:
            _os_chdir(self._old.pop())


base_dir = Path(__file__).resolve().parent.parent
chdir = _chdir(base_dir)
sys.path.append(str(base_dir / "src"))
