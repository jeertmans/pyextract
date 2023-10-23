"""
Command line interface (CLI) for pyextract.

To use it, please install the ``cli`` extra with ``pip install pyextract[cli]``.
"""


import math
import textwrap
from typing import Optional, Sequence

import click
from pygments import highlight
from pygments.formatters import Terminal256Formatter
from pygments.lexers import Python3Lexer
from pygments.styles import get_all_styles

from . import extract_source_lines_from_node_id

STYLES = list(get_all_styles())


def list_styles(ctx: click.Context, param: click.Parameter, value: bool) -> None:
    """List all supported styles from Pygments."""
    if value:
        click.echo("Supported styles:")
        click.echo(textwrap.indent("\n".join(STYLES), "- "))
        ctx.exit(0)


@click.command()
@click.argument("node_ids", nargs=-1, required=True)
@click.option("-l", "--lineno", "show_lineno", is_flag=True, help="Show line number.")
@click.option("-f", "--filename", "show_filename", is_flag=True, help="Show filename.")
@click.option(
    "--dedent/--no-dedent", default=True, help="Remove leading indendation from code."
)
@click.option(
    "-s",
    "--style",
    type=click.Choice(STYLES),
    metavar="STYLE",
    default="default",
    help="Set color highlighting style. "
    "Use '--list-styles' to see all possible values.",
)
@click.option(
    "--color/--no-color",
    " / --nc",
    type=bool,
    default=None,
    help="Force showing or hiding colors and other styles. By "
    "default, it will remove color if the output does not look like "
    "an interactive terminal.",
)
@click.option(
    "--list-styles",
    is_flag=True,
    expose_value=False,
    callback=list_styles,
    help="List all supported styles and exit.",
)
def main(
    node_ids: Sequence[str],
    show_lineno: bool,
    show_filename: bool,
    dedent: bool,
    style: str,
    color: Optional[bool],
):
    """Extract code fragments from node ids."""
    for _i, node_id in enumerate(node_ids):
        path, lines, lineno = extract_source_lines_from_node_id(node_id)

        code = "".join(lines)

        if dedent:
            code = textwrap.dedent(code)

        code = highlight(code, Python3Lexer(), Terminal256Formatter(style=style))

        if show_lineno:
            lines = code.splitlines()
            length = math.ceil(math.log10(len(lines) + lineno - 1))
            lines = [
                click.style(f"{num:{length}d}", fg="green") + ": " + line
                for num, line in enumerate(lines, start=lineno)
            ]
            code = "\n".join(lines)

        if show_filename:
            code = textwrap.indent(
                code, click.style(str(path), fg="red") + (":" if show_lineno else ": ")
            )

        click.echo(code, color=color)  # , nl=i < len(node_ids) - 1)


if __name__ == "__main__":
    main()
