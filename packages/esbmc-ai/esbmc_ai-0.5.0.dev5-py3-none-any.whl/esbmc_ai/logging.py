# Author: Yiannis Charalambous

"""Logging module for verbose printing."""

from os import get_terminal_size
import esbmc_ai.config as config

verbose: int = 0


def set_verbose(level: int) -> None:
    """Sets the verbosity level."""
    global verbose
    verbose = level


def printv(m) -> None:
    """Level 1 verbose printing."""
    if verbose > 0:
        print(m)


def printvv(m) -> None:
    """Level 2 verbose printing."""
    if verbose > 1:
        print(m)


def printvvv(m) -> None:
    """Level 3 verbose printing."""
    if verbose > 2:
        print(m)


def print_horizontal_line(verbosity: int) -> None:
    if verbosity >= config.verbose:
        try:
            printvv("-" * get_terminal_size().columns)
        except OSError:
            pass
