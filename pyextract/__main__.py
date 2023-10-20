from . import extract_source_lines_from_path_and_parts

import sys

from textwrap import dedent

from pygments import highlight
from pygments.style import Style
from pygments.token import Token
from pygments.lexers import Python3Lexer
from pygments.formatters import Terminal256Formatter
from pygments.styles import get_all_styles

if __name__ == "__main__":
    path, lines, lineno = extract_source_lines_from_path_and_parts(sys.argv[1])
    
    code = dedent("".join(lines))
    results = highlight(code, Python3Lexer(), Terminal256Formatter(style="vim"))
    print(results, end="")
