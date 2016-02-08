import unittest
import numpy as np


class slactrac_element_base(object):
    def basic_setup(self, length, order, name):
        self._l       = length
        self._order   = order
        self._name    = name

    @property
    def element(self):
        return self._element

    @element.setter
    def element(self, val):
        self._element = val

    def name_test(self):
        self.assertEqual(self.element.name, self._name)

    def order_test(self):
        self.assertEqual(self.element.order, self._order)


def array_tol(meas, ref, tol):
    return np.all(meas - ref < tol)
