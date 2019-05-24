# Pandocode

`pandocode` is a pandoc filter that converts Python _(-like)_ code to LaTeX-Pseudocode.  
It can also be used as a standalone program.

## Usage

### Standalone
Outputs the resulting LaTeX code to console

**Run:**  
`./pandocode.pyz <file>`  
or  
`pandocode <file>`

### Filter
Converts every code-block of type _pseudo_ to LaTeX

**Run:**  
`pandoc --filter /path/to/pandocode.pyz <infile.md> -o <outfile>`  
or  
`pandoc --filter pandocode <infile.md> -o <outfile>`

## Building
- Install dependencies from `requirements.txt` and `make-requirements.txt`
    - `pip3 install -r requirements.txt -r make-requirements.txt`
    - or `pip3 install --user -r requirements.txt -r make-requirements.txt`
- Run `make`
- _Optional:_ Run `sudo make install`
    - This will install `pandocode.pyz` to `/usr/bin/pandocode`

#### Use PyPy3 instead of CPython
- Use `pypy3 -m pip` indead of `pip3`
    - If pip is missing, install it with `pypy3 -m ensurepip` or `pypy3 -m ensurepip --user`
- Run `make PY=pypy3` instead of `make`

#### Without PyLint:
If you want to build without running pylint:
- Don't install `make-requirements.txt`
- Run `make PYLINT=$(which true)` instead of `make`

## Control sequences
Pandocode allows the use of the following control sequences inside the code:

#### Begin/End
Syntax:
- `#$begin`
- `#$end`

If a begin sequence is found, Pandocode ignores any code that is outside of a pair of begin/end control sequences.  
If the end of the code is reached and no end sequence is encountered, all code from the begin sequence on is included.

#### Add
Syntax:
- `#$+ <text>`

Includes `<text>` as a line in the code before code processing.

#### Remove
Syntax:
- `#$-`

Removes the next line before code processing.

#### Replace
Syntax:
- `#$= <text>`

Replaces the next line by `<text>` before code processing.

#### Raw
Syntax:
- `:: <LaTeX>`

When encountered during processing, instead of processing this line, `:: ` gets removed and `<LaTeX>` is appended to the output.  
This can be used as `<text>` in any control sequence that is processed before code processing.

Example:  
`#$= :: <LaTeX>`  
Replaces the next line by raw LaTeX

## External Code

Pandocode is tested to be working with [pandoc-include-code](https://github.com/owickstrom/pandoc-include-code)

    ---
    header-includes:
      - \usepackage{algorithm}
      - \usepackage[noend]{algpseudocode}
    ---

    ```{.pseudo include=code.py}
    ```
