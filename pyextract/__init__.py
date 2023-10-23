"""PyExtract Python package, for extracting code in modules from a node id."""

import importlib
import importlib.util
import inspect
import random
import string
import sys
from pathlib import Path
from typing import List, Tuple


class BuiltInModuleError(Exception):
    """Error when trying to read source code from a built-in module."""

    def __init__(self, module: str) -> None:
        super().__init__()
        self.module = module

    def __str__(self) -> str:
        return f"Cannot read source code from built-in module '{self.module}'"


def extract_source_lines_from_node_id(node_id: str) -> Tuple[Path, List[str], int]:
    """Extract source lines of code from a given node id."""
    try:
        path_str, parts_str = node_id.split("::", maxsplit=1)
        path = Path(path_str)
        parts = parts_str.split("::")
    except ValueError:
        path = Path(node_id)
        parts = []

    try:
        name = basename = path.resolve(strict=True).stem

        while name in sys.modules:  # To avoid name clash with already imported modules
            name = (
                basename
                + "_"
                + "".join(random.choice(string.ascii_letters) for i in range(8))
            )

        spec = importlib.util.spec_from_file_location(name, path)
        assert spec is not None
        module = importlib.util.module_from_spec(spec)
        assert module is not None
        sys.modules[name] = module
        spec.loader.exec_module(module)

    except FileNotFoundError:
        name = str(path)
        module = importlib.import_module(name)

    obj = module

    for part in parts:
        try:
            obj = getattr(obj, part)
        except AttributeError as e:
            raise AttributeError(f"Could not find part '{part}' in '{node_id}'") from e

    try:
        lines, lineno = inspect.getsourcelines(obj)

    except TypeError as e:
        raise BuiltInModuleError(name) from e

    return path, lines, lineno
