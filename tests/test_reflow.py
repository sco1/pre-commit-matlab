from pathlib import Path
from textwrap import dedent

import pytest

from pre_commit_matlab import matlab_reflow_comments

FORMATTING_TEST_CASES = [
    (
        "only comments",
        dedent(
            """\
            % XBMINI is a MATLAB class definition providing the user with a set of
            % methods to parse and analyze raw data files output by GCDC XBmini
            % datalogger
            """
        ),
        dedent(
            """\
            % XBMINI is a MATLAB class definition providing the user with a set of methods to parse and analyze
            % raw data files output by GCDC XBmini datalogger
            """
        ),
        dedent(
            """\
            % XBMINI is a MATLAB class definition providing
            % the user with a set of methods to parse and
            % analyze raw data files output by GCDC XBmini
            % datalogger
            """
        ),
    ),
    (
        "only comments w/blank comment line",
        dedent(
            """\
            % XBMINI is a MATLAB class definition providing the user with a set of
            % methods to parse and analyze raw data files output by GCDC XBmini
            % datalogger
            %
            % Initialize an xbmini object using an absolute filepath to the raw
            % log file:
            """
        ),
        dedent(
            """\
            % XBMINI is a MATLAB class definition providing the user with a set of methods to parse and analyze
            % raw data files output by GCDC XBmini datalogger
            %
            % Initialize an xbmini object using an absolute filepath to the raw log file:
            """
        ),
        dedent(
            """\
            % XBMINI is a MATLAB class definition providing
            % the user with a set of methods to parse and
            % analyze raw data files output by GCDC XBmini
            % datalogger
            %
            % Initialize an xbmini object using an absolute
            % filepath to the raw log file:
            """
        ),
    ),
    (
        "only comments w/indented",
        dedent(
            """\
            % XBMINI is a MATLAB class definition providing the user with a set of
            % methods to parse and analyze raw data files output by GCDC XBmini
            % datalogger
            %
            % Initialize an xbmini object using an absolute filepath to the raw
            % log file:
            %
            %     myLog = xbmini(filepath);
            """
        ),
        dedent(
            """\
            % XBMINI is a MATLAB class definition providing the user with a set of methods to parse and analyze
            % raw data files output by GCDC XBmini datalogger
            %
            % Initialize an xbmini object using an absolute filepath to the raw log file:
            %
            %     myLog = xbmini(filepath);
            """
        ),
        dedent(
            """\
            % XBMINI is a MATLAB class definition providing
            % the user with a set of methods to parse and
            % analyze raw data files output by GCDC XBmini
            % datalogger
            %
            % Initialize an xbmini object using an absolute
            % filepath to the raw log file:
            %
            %     myLog = xbmini(filepath);
            """
        ),
    ),
    (
        "code & comments",
        dedent(
            """\
            function findgroundlevelpressure(dataObj)
            % FINDGROUNDLEVELPRESSURE Plots the raw pressure data and
            % prompts the user to window the region of the plot where the
            % sensor is at ground level. The average pressure from this
            % windowed region is used to update the object's pressure_groundlevel
            % private property. The object's pressure altitude is also
            % recalculated using the updated ground level pressure.
            h.fig = figure;
            """
        ),
        dedent(
            """\
            function findgroundlevelpressure(dataObj)
            % FINDGROUNDLEVELPRESSURE Plots the raw pressure data and prompts the user to window the region of
            % the plot where the sensor is at ground level. The average pressure from this windowed region is
            % used to update the object's pressure_groundlevel private property. The object's pressure altitude
            % is also recalculated using the updated ground level pressure.
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
            % pressure_groundlevel private property. The
            % object's pressure altitude is also recalculated
            % using the updated ground level pressure.
            h.fig = figure;
            """
        ),
    ),
    (
        "code & comments, mixed levels",
        dedent(
            """\
            classdef xbmini < handle & AirdropData
                % XBMINI is a MATLAB class definition providing the user with a set of
                % methods to parse and analyze raw data files output by GCDC XBmini
                % datalogger

                methods
                    function findgroundlevelpressure(dataObj)
                        % FINDGROUNDLEVELPRESSURE Plots the raw pressure data and
                        % prompts the user to window the region of the plot where the
                        % sensor is at ground level. The average pressure from this
                        % windowed region is used to update the object's pressure_groundlevel
                        % private property. The object's pressure altitude is also
                        % recalculated using the updated ground level pressure.
                        h.fig = figure;
                    end
                end
            """
        ),
        dedent(
            """\
            classdef xbmini < handle & AirdropData
                % XBMINI is a MATLAB class definition providing the user with a set of methods to parse and
                % analyze raw data files output by GCDC XBmini datalogger

                methods
                    function findgroundlevelpressure(dataObj)
                        % FINDGROUNDLEVELPRESSURE Plots the raw pressure data and prompts the user to window the
                        % region of the plot where the sensor is at ground level. The average pressure from this
                        % windowed region is used to update the object's pressure_groundlevel private property.
                        % The object's pressure altitude is also recalculated using the updated ground level
                        % pressure.
                        h.fig = figure;
                    end
                end
            """
        ),
        dedent(
            """\
            classdef xbmini < handle & AirdropData
                % XBMINI is a MATLAB class definition
                % providing the user with a set of methods to
                % parse and analyze raw data files output by
                % GCDC XBmini datalogger

                methods
                    function findgroundlevelpressure(dataObj)
                        % FINDGROUNDLEVELPRESSURE Plots the
                        % raw pressure data and prompts the
                        % user to window the region of the
                        % plot where the sensor is at ground
                        % level. The average pressure from
                        % this windowed region is used to
                        % update the object's
                        % pressure_groundlevel private
                        % property. The object's pressure
                        % altitude is also recalculated using
                        % the updated ground level pressure.
                        h.fig = figure;
                    end
                end
            """
        ),
    ),
    (
        "hyphens",
        dedent(
            """\
            % This is a really long comment line with some stuff and also a hyphenated word that hits the-boundary
            """
        ),
        dedent(
            """\
            % This is a really long comment line with some stuff and also a hyphenated word that hits
            % the-boundary
            """
        ),
        dedent(
            """\
            % This is a really long comment line with some
            % stuff and also a hyphenated word that hits
            % the-boundary
            """
        ),
    ),
    (
        "Inline percent signs",
        dedent(
            """\
            % This is 100% a comment with a percent sign
            """
        ),
        dedent(
            """\
            % This is 100% a comment with a percent sign
            """
        ),
        dedent(
            """\
            % This is 100% a comment with a percent sign
            """
        ),
    ),
]


@pytest.mark.parametrize(
    ("case_name", "in_src", "truth_100_width", "truth_50_width"), FORMATTING_TEST_CASES
)
def test_comment_reflow(  # noqa: D103
    tmp_path: Path, case_name: str, in_src: str, truth_100_width: str, truth_50_width: str
) -> None:
    sample_file = tmp_path / "sample_src.m"

    # Check 100 width
    sample_file.write_text(in_src)
    matlab_reflow_comments.process_file(
        sample_file,
        100,
        ignore_indented=True,
        alternate_capital_handling=False,
        reflow_block_comments=True,
    )
    assert sample_file.read_text() == truth_100_width

    # Check 50 width
    sample_file.write_text(in_src)
    matlab_reflow_comments.process_file(
        sample_file,
        50,
        ignore_indented=True,
        alternate_capital_handling=False,
        reflow_block_comments=True,
    )
    assert sample_file.read_text() == truth_50_width
