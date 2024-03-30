# vbelt: The VASP user toolbelt.
# Copyright (C) 2023  Théo Cavignac
# Licensed under EUPL
import collections
from .outcar_utils import get_float


def normal_end(file):
    for line in file:
        if line.startswith(" General timing and accounting informations"):
            return True
    return False


def converged(oszicar, outcar, tol=None):
    with open(outcar) as f:
        if tol is None:
            _tol = get_float(f, "EDIFF ", after="stopping", expect_equal=True)
            if _tol is None:
                raise ValueError("Could not find the EDIFF tolerance.")
        else:
            _tol = tol
        if not normal_end(f):
            return False, _tol, None

    with open(oszicar) as f:
        t = tail(f, 2)
        second_to_last = next(t)
        last = next(t)

    try:
        ediff = float(second_to_last.split()[3])
    except ValueError:
        return False, _tol, None

    return ((abs(ediff) < _tol and "F=" in last), _tol, abs(ediff))


def tail(it, n):
    return iter(collections.deque(it, maxlen=n))
