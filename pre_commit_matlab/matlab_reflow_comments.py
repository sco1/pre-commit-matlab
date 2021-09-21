import argparse
import textwrap
import typing as t
from collections import deque
from pathlib import Path


def _n_leading_spaces(line: str) -> int:
    return len(line) - len(line.lstrip())


def _dump_buffer(
    f: t.TextIO, buffer: deque, line_length: int, indent_level: int, is_block: bool = False
) -> deque:
    """
    Reflow the buffered line(s) to the specified line length, preserving the indent level.

    If `is_block` is true, lines will be prefixed by indentation only & not contain a `%` char.

    The buffer is cleared & returned after the new line(s) are written.
    """
    if is_block:
        initial = following = f"{' '*indent_level}"
    else:
        initial = f"{' '*indent_level}%"  # Don't include the initial leading space
        following = f"{' '*indent_level}% "

    reflowed_src = textwrap.fill(
        "".join(buffer),
        width=line_length,
        initial_indent=initial,
        subsequent_indent=following,
        break_on_hyphens=False,
    )
    reflowed_src = f"{reflowed_src}\n"
    f.write(reflowed_src)

    buffer.clear()
    return buffer


def _write_line(
    f: t.TextIO,
    line: str,
    buffer: deque,
    line_length: int,
    indent_level: int,
    is_block: bool = False,
) -> deque:
    """
    Write the provided source line after checking for buffered comments to empty.

    The buffer is cleared & returned after the new line(s) are written.
    """
    if buffer:
        buffer = _dump_buffer(f, buffer, line_length, indent_level, is_block)
    f.write(f"{line}\n")

    return buffer


def process_file(
    file: Path,
    line_length: int,
    ignore_indented: bool,
    alternate_capital_handling: bool,
    reflow_block_comments: bool,
) -> None:
    """
    Reflow comments (`%`) in the provided MATLAB file (`*.m`) to the specified line length.

    Blank comment lines are passed back into the reformatted source code.

    If `ignore_indented` is `True`, comments that contain inner indentation of at least two spaces
    is passed back into the reformatted source code as-is. Leading whitespace in the line is not
    considered.

    If `alternate_capital_handling` is `True`, if the line buffer has contents then a line beginning
    with a capital letter is treated as the start of a new comment block.

    If `reflow_block_comments` is `True`, the contents of a block comment (delimited by `%{` and
    `%}`) are reflowed. Per MATLAB's spec, the delimiters must be the only thing on their respective
    lines.

    View the README for code samples.
    """
    src = file.read_text().splitlines()
    with file.open("w") as f:
        buffer: deque = deque()
        indent_level = 0  # Number of leading spaces
        in_comment_block = False
        for line in src:
            lstripped_line = line.lstrip()

            # Check for the close of a block comment
            if reflow_block_comments and lstripped_line.startswith("%}"):
                # If we're exiting the block comment, reflow the contents & then write closing tag
                # If we're here then the indent level will already be set by the logic further down
                in_comment_block = False
                buffer = _write_line(f, line, buffer, line_length, indent_level, is_block=True)
                continue

            # If we're inside a comment block, lines will likely not begin with a %
            # Since we're dumping lines inside comment blocks as-is, we can short-circuit here
            if reflow_block_comments and in_comment_block:
                if buffer:
                    # If this isn't the first line in the text block we need to add a leading space
                    # to the line, otherwise it gets run into the last word from the previous line
                    buffer.append(f" {lstripped_line}")
                else:
                    buffer.append(lstripped_line)

                continue

            if lstripped_line.startswith("%"):
                # Comment line
                if not buffer:
                    # New buffer, set the indentation level for the incoming block
                    indent_level = _n_leading_spaces(line)

                # Check for the opening of a block comment
                if reflow_block_comments and lstripped_line.startswith("%{"):
                    # If we're entering a block comment, dump out any existing buffer & write the
                    # opening tag straight out
                    in_comment_block = True
                    buffer = _write_line(f, line, buffer, line_length, indent_level)
                    continue

                # Count the inner level of indentation of the comment itself to use for both the
                # empty comment line check and the ignore indent check
                # Only strip leading percent sign so inline percentages aren't mangled
                uncommented_line = lstripped_line.replace("%", "", 1).rstrip()
                inner_indent = _n_leading_spaces(uncommented_line)

                if inner_indent == 0:
                    # Blank line, write straight out
                    buffer = _write_line(f, line, buffer, line_length, indent_level)
                    continue

                if ignore_indented and inner_indent >= 2:
                    # Inner indented comment, write straight out
                    buffer = _write_line(f, line, buffer, line_length, indent_level)
                    continue

                # `uncommented_line` is likely to start with leading whitespace that we don't care
                # about for this check
                if alternate_capital_handling and uncommented_line.lstrip()[0].isupper():
                    # Comment line starts with a capital letter
                    # We want to treat this as the start of a new comment block, so if there is an
                    # existing buffer, dump it before adding the current line into a fresh buffer
                    if buffer:
                        buffer = _dump_buffer(f, buffer, line_length, indent_level)

                # If we're here, then we have a line eligible for reflowing so add it to the buffer
                buffer.append(uncommented_line)
                continue

            # Non-comment line, write straight out
            buffer = _write_line(f, line, buffer, line_length, indent_level)
        else:
            # EOF, Dump any remaining comments in the buffer (file ends in comments)
            if buffer:
                buffer = _dump_buffer(f, buffer, line_length, indent_level)


def main(argv: t.Optional[t.Sequence[str]] = None) -> None:  # pragma: no cover  # noqa: D103
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*", type=Path)
    parser.add_argument("--line-length", type=int, default=78)
    parser.add_argument("--ignore-indented", type=bool, default=True)
    parser.add_argument("--alternate-capital-handling", type=bool, default=False)
    parser.add_argument("--reflow-block-comments", type=bool, default=True)
    args = parser.parse_args(argv)

    for file in args.filenames:
        process_file(
            file,
            args.line_length,
            args.ignore_indented,
            args.alternate_capital_handling,
            args.reflow_block_comments,
        )


if __name__ == "__main__":  # pragma: no cover
    main()
