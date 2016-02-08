import unittest
import numpy as np
import slactrac as st
from .base import slactrac_element_base
from .base import array_tol

order  = 1
l      = 1.3
angle  = 3*np.pi/180
rotate = 90
name   = 'test'
K1     = 1.45


class slactrac_drift_test(slactrac_element_base, unittest.TestCase):
    def setUp(self):
        self.basic_setup(length=l, order=order, name=name)

        self.element = st.Drift(length=self._l, order=self._order, name=self._name)

    def R_test(self):
        r = np.array([[1, self._l, 0, 0, 0, 0],
                      [0, 1, 0, 0, 0, 0],
                      [0, 0, 1, self._l, 0, 0],
                      [0, 0, 0, 1, 0, 0],
                      [0, 0, 0, 0, 1, 0],
                      [0, 0, 0, 0, 0, 1]
                      ])
        self.assertTrue(np.array_equal(self.element.R, r))


class slactrac_bend_test(slactrac_element_base, unittest.TestCase):
    def setUp(self):
        self._l      = l
        self._order  = order
        self._angle  = angle
        self._rotate = rotate
        self._name   = 'testdrift'
        self.element = st.Bend(length=self._l, angle=self._angle, order=self._order, rotate=self._rotate, name=self._name)

    def angle_test(self):
        self.assertEqual(self.element.angle, self._angle)

    def rotate_test(self):
        self.assertEqual(self.element.rotate, self._rotate)

    def R_test(self):
        r = np.array([[  1.00000000e+00,   1.30000000e+00,   0.00000000e+00,
                         0.00000000e+00,   0.00000000e+00,   0.00000000e+00],
                      [ -1.65725745e-11,   1.00000000e+00,   0.00000000e+00,
                         0.00000000e+00,   0.00000000e+00,   0.00000000e+00],
                      [  0.00000000e+00,   0.00000000e+00,   9.98629535e-01,
                         1.29940608e+00,   0.00000000e+00,   3.40261456e-02],
                      [  0.00000000e+00,   0.00000000e+00,  -2.10792635e-03,
                         9.98629535e-01,   0.00000000e+00,   5.23359562e-02],
                      [  0.00000000e+00,   0.00000000e+00,   5.23359562e-02,
                         3.40261456e-02,   1.00000000e+00,   5.93922549e-04],
                      [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
                         0.00000000e+00,   0.00000000e+00,   1.00000000e+00]])

        self.assertTrue(array_tol(self.element.R, r, 1e-10))


class slactrac_quad_test(slactrac_element_base, unittest.TestCase):
    def setUp(self):
        self.basic_setup(length=l, order=order, name=name)

        self.element = st.Quad(length=l, K1=K1, order=order, name=name)

class slactrac_focus_test(slactrac_element_base, unittest.TestCase):
    def setUp(self):
        self.basic_setup(length=l, order=order, name=name)

        self.element = st.Focus(length=l, K1=K1, order=order, name=name)
