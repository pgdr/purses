#!/usr/bin/env python
import argparse

try:
    import pandas as pd

    pd.set_option("display.max_colwidth", None)  # disable truncation
    pd.set_option("display.width", 10 ** 10)  # 10**10=inf for all practical purposes
except ImportError:
    pass  # Well actually, you don't really _need_ pandas, I guess...

from .bindings import binding
from .controller import Controller
from .model import Model


def load(tabular, bindings=None, delimiter=None):
    """Load the tabular data into curses.

    The tabular data can be a filename to a csv file or a Pandas dataframe.
    Launches a curses view.

    """
    if delimiter is None:
        delimiter = ","  # default Pandas behavior

    name = ""
    if isinstance(tabular, str):
        import pandas as pd

        name = tabular
        tabular = pd.read_csv(tabular, delimiter=delimiter)
    model = Model(tabular, name)
    cntrl = Controller(model)

    if bindings is None:
        bindings = {}
    bindings_ = {}
    bindings_.update(binding.bindings)
    bindings_.update(bindings)
    cntrl.add_handlers(bindings_)
    cntrl.run()  # npyscreen event loop, calls Controller.main


def _setup_args():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("csv", help="The path to the csv file")
    arg_parser.add_argument("--delimiter", help="Choose delimiter")
    options, _ = arg_parser.parse_known_args()
    return options


def main():
    options = _setup_args()
    load(options.csv, delimiter=options.delimiter)


if __name__ == "__main__":
    main()

__version__ = "0.0.13"
__all__ = ["binding", "load"]
