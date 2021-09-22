[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pre-commit-matlab)](https://pypi.org/project/pre-commit-matlab/)
[![PyPI](https://img.shields.io/pypi/v/pre-commit-matlab)](https://pypi.org/project/pre-commit-matlab/)
[![PyPI - License](https://img.shields.io/pypi/l/pre-commit-matlab?color=magenta)](https://github.com/sco1/pre-commit-matlab/blob/master/LICENSE)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/sco1/pre-commit-matlab/main.svg)](https://results.pre-commit.ci/latest/github/sco1/pre-commit-matlab/main)
[![lint-and-test](https://github.com/sco1/pre-commit-matlab/actions/workflows/lint_test.yml/badge.svg?branch=main)](https://github.com/sco1/pre-commit-matlab/actions/workflows/lint_test.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)
# pre-commit-matlab
A collection of [pre-commit](https://pre-commit.com/) hooks for MATLAB

Ok... it's just one hook so far but maybe someday there will be more 😃

## Using pre-commit-matlab with pre-commit
Add this to your `.pre-commit-config.yaml`

```yaml
-   repo: https://github.com/sco1/pre-commit-matlab
    rev: v1.2.0
    hooks:
    -   id: matlab-reflow-comments
        args: [--line-length=100]
```

## Hooks
### `matlab-reflow-comments`
Reflow inline comments (lines beginning with `%`) or block comments (delimited by `%{` and `%}`) in MATLAB file(s) (`*.m`) to the specified line length.

Blank comment lines are passed back into the reformatted source code.

* Use `--line-length` to specify line length. (Default: `75`)
* Use `--reflow-block-comments` to control block comment reflow. (Default: `True`)
* Use `--ignore-indented` to ignore comments with inner indentation. (Default: `True`)
  * **NOTE:** This logic *is not* applied to the contents of a block comment.
* Use `--alternate-capital-handling` to treat comment lines that begin with a capital letter as the start of a new comment block. (Default: `False`)
  * **NOTE:** This logic *is not* applied to the contents of a block comment.

If `ignore-indented` is `True`, comments that contain inner indentation of at least two spaces is passed back into the reformatted source code as-is. Leading whitespace in the line is not considered.

For example:

```matlab
    % This is not indented
% This is not indented
%  This is indented
%    This is indented
```

If `alternate-capital-handling` is `True`, if the line buffer has contents then a line beginning with a capital letter is treated as the start of a new comment block.

For example:

```matlab
% This is a comment line
% This is a second comment line that will not be reflowed into the previous line
```

**NOTE:** As an opinionated flag, this may lead to false positives so it is off by default. If enabled, pay close attention to the resulting diff to ensure that your comments are being reflowed as desired.
