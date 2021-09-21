from pathlib import Path
from textwrap import dedent

import pytest

from pre_commit_matlab import matlab_reflow_comments

BLOCK_COMMENT_TEST_CASES = [
    (
        True,
        dedent(
            """\
            %{
            This is a really long and descriptive block comment that has some
            information about things and stuff and also spans multiple lines
            %}
            """
        ),
        dedent(
            """\
            %{
            This is a really long and descriptive block comment that has some information about things and stuff
            and also spans multiple lines
            %}
            """
        ),
        dedent(
            """\
            %{
            This is a really long and descriptive block
            comment that has some information about things and
            stuff and also spans multiple lines
            %}
            """
        ),
    ),
    (
        True,
        dedent(
            """\
            %{
            This is a really long and descriptive block comment that has some
            information about things and stuff and also spans multiple lines
            %}
            function asdf = foo()
                asdf = 1;
            end
            """
        ),
        dedent(
            """\
            %{
            This is a really long and descriptive block comment that has some information about things and stuff
            and also spans multiple lines
            %}
            function asdf = foo()
                asdf = 1;
            end
            """
        ),
        dedent(
            """\
            %{
            This is a really long and descriptive block
            comment that has some information about things and
            stuff and also spans multiple lines
            %}
            function asdf = foo()
                asdf = 1;
            end
            """
        ),
    ),
    (
        True,
        dedent(
            """\
            function asdf = foo()
                % Hello this is an inline comment
                %{
                This is a really long and descriptive block comment that has some
                information about things and stuff and is indented and also spans
                multiple lines
                %}
                asdf = 1;
            end
            """
        ),
        dedent(
            """\
            function asdf = foo()
                % Hello this is an inline comment
                %{
                This is a really long and descriptive block comment that has some information about things and
                stuff and is indented and also spans multiple lines
                %}
                asdf = 1;
            end
            """
        ),
        dedent(
            """\
            function asdf = foo()
                % Hello this is an inline comment
                %{
                This is a really long and descriptive block
                comment that has some information about things
                and stuff and is indented and also spans
                multiple lines
                %}
                asdf = 1;
            end
            """
        ),
    ),
    (
        False,
        dedent(
            """\
            %{
            a = zeros(10, 1);
            for ii = 1:10
                a[ii] = ii;
            end
            %}
            """
        ),
        dedent(
            """\
            %{
            a = zeros(10, 1);
            for ii = 1:10
                a[ii] = ii;
            end
            %}
            """
        ),
        dedent(
            """\
            %{
            a = zeros(10, 1);
            for ii = 1:10
                a[ii] = ii;
            end
            %}
            """
        ),
    ),
]


@pytest.mark.parametrize(
    (
        "should_reflow",
        "in_src",
        "truth_100_width",
        "truth_50_width",
    ),
    BLOCK_COMMENT_TEST_CASES,
)
def test_block_comment_reflow(  # noqa: D103
    tmp_path: Path,
    should_reflow: bool,
    in_src: str,
    truth_100_width: str,
    truth_50_width: str,
) -> None:
    sample_file = tmp_path / "sample_src.m"

    # Check 100 width
    sample_file.write_text(in_src)
    matlab_reflow_comments.process_file(
        sample_file,
        100,
        ignore_indented=True,
        alternate_capital_handling=False,
        reflow_block_comments=should_reflow,
    )
    assert sample_file.read_text() == truth_100_width

    # Check 50 width
    sample_file.write_text(in_src)
    matlab_reflow_comments.process_file(
        sample_file,
        50,
        ignore_indented=True,
        alternate_capital_handling=False,
        reflow_block_comments=should_reflow,
    )
    assert sample_file.read_text() == truth_50_width
