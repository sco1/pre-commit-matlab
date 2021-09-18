from pathlib import Path
from textwrap import dedent

import pytest

from pre_commit_matlab import matlab_reflow_comments

ALTERNATE_CAPITAL_HANDLING_TEST_CASES = [
    (
        dedent(
            """\
            % This is a really long and descriptive one liner comment that has some information about things and stuff
            % But it also has an intentional line break into a comment that starts with a capital letter
            """
        ),
        dedent(
            """\
            % This is a really long and descriptive one liner comment that has some information about things and
            % stuff
            % But it also has an intentional line break into a comment that starts with a capital letter
            """
        ),
        dedent(
            """\
            % This is a really long and descriptive one liner
            % comment that has some information about things
            % and stuff
            % But it also has an intentional line break into a
            % comment that starts with a capital letter
            """
        ),
    ),
    (
        dedent(
            """\
            function findgroundlevelpressure(dataObj)
            % FINDGROUNDLEVELPRESSURE Plots the raw pressure data and
            % prompts the user to window the region of the plot where the
            % sensor is at ground level. The average pressure from this
            % windowed region is used to update the object's pressure_groundlevel
            % private property.
            % The object's pressure altitude is also
            % recalculated using the updated ground level pressure.
            h.fig = figure;
            """
        ),
        dedent(
            """\
            function findgroundlevelpressure(dataObj)
            % FINDGROUNDLEVELPRESSURE Plots the raw pressure data and prompts the user to window the region of
            % the plot where the sensor is at ground level. The average pressure from this windowed region is
            % used to update the object's pressure_groundlevel private property.
            % The object's pressure altitude is also recalculated using the updated ground level pressure.
            h.fig = figure;
            """
        ),
        dedent(
            """\
            function findgroundlevelpressure(dataObj)
            % FINDGROUNDLEVELPRESSURE Plots the raw pressure
            % data and prompts the user to window the region
            % of the plot where the sensor is at ground level.
            % The average pressure from this windowed region
            % is used to update the object's
            % pressure_groundlevel private property.
            % The object's pressure altitude is also
            % recalculated using the updated ground level
            % pressure.
            h.fig = figure;
            """
        ),
    ),
]


@pytest.mark.parametrize(
    ("in_src", "truth_100_width", "truth_50_width"), ALTERNATE_CAPITAL_HANDLING_TEST_CASES
)
def test_alternate_capital_handling(  # noqa: D103
    tmp_path: Path, in_src: str, truth_100_width: str, truth_50_width: str
) -> None:
    sample_file = tmp_path / "sample_src.m"

    # Check 100 width
    sample_file.write_text(in_src)
    matlab_reflow_comments.process_file(
        sample_file, 100, ignore_indented=True, alternate_capital_handling=True
    )
    assert sample_file.read_text() == truth_100_width

    # Check 50 width
    sample_file.write_text(in_src)
    matlab_reflow_comments.process_file(
        sample_file, 50, ignore_indented=True, alternate_capital_handling=True
    )
    assert sample_file.read_text() == truth_50_width
