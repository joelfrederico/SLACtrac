import unittest
import numpy as np
import slactrac as st

class slactrac_drift_test(unittest.TestCase):
    def setUp(self):
        self._l     = 1.3
        self._order = 1
        self._name  = 'testdrift'
        self._drift = st.Drift(length=self._l, order=self._order, name=self._name)

    def R_test(self):
        r = np.array([[1, self._l, 0, 0, 0, 0],
                      [0, 1, 0, 0, 0, 0],
                      [0, 0, 1, self._l, 0, 0],
                      [0, 0, 0, 1, 0, 0],
                      [0, 0, 0, 0, 1, 0],
                      [0, 0, 0, 0, 0, 1]
                      ])
        self.assertTrue(np.array_equal(self._drift.R, r))