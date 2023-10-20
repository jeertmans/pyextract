import importlib.util
import inspect
import random
import string
import sys

from pathlib import Path
from typing import Tuple, List

def extract_source_lines_from_path_and_parts(path_and_parts: str) -> Tuple[Path, List[str], int]:
    try:
        path_str, parts_str = path_and_parts.split("::", maxsplit=1)
        path = Path(path_str)
        parts = parts_str.split("::")
    except ValueError:
        path = Path(path_and_parts)
        parts = []

    name = basename = path.resolve(strict=True).stem

    while name in sys.modules:
        name = basename + "_" + "".join(random.choice(string.ascii_letters) for i in range(8))

    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    obj = module

    for part in parts:
        try:
            obj = getattr(obj, part)
        except AttributeError as e:
            raise AttributeError(f"Could not find part '{part}' in '{path_and_parts}'") from e

    lines, lineno = inspect.getsourcelines(obj)

    return path, lines, lineno

