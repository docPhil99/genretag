# genretag
A simple script that changes all the genre tags (via taglib) in a directory. The tags are set via flags on the command line. Run `genretag -h` for help.


You need to install taglib system library.

`sudo apt get taglib1-dev` on Debian based systems. This needs to version 2, some older repo have version 1, in which case downgrade to `pytaglib==2.1.0` in the `pyproject.toml`. Alternatively, see here: https://github.com/supermihi/pytaglib

To install
```
uv tool install .
```
This creates a system wide install. Run with the command `genretag`


