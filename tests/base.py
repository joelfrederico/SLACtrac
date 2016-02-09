import unittest
import numpy as np
import types


def array_tol(meas, ref, tol):
    return np.all(meas - ref < tol)


def change_E(self, old_gamma, new_gamma):
    self.element.change_E(old_gamma, new_gamma)
    return self
