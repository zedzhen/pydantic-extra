import sys
from contextlib import chdir as _chdir
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent
chdir = _chdir(base_dir)
sys.path.append(str(base_dir / "src"))
