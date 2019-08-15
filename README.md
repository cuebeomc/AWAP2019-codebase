# AWAP 2019 Codebase

[8/15/2019] Changing name to create distinction between AWAP2019 repo.

Repository for AWAP 2019 game development.

## Development

For development work, work in the `src/awap2019/awap2019` directory. Currently in need of additional bots and visualizer.

To test experimental changes to the package, run `pip install -e ../src/awap2019` from the `test` directory and change test/ accordingly.

## Testing

Run `pip install awap2019`, which should automatically install the latest instance of our code base that is on PyPi. In the `test` directory, feel free to work with your own `player1/team.py` or `player2/team.py`. Feel free to use these files to also unit test, and report any bugs.

Note that `test/test.py` uses `absl-py`, so run `pip install absl-py` before running `python test.py`. Run `python test.py --help` for valid flags.
