import unittest
import numpy as np
import slactrac as st
from .base import *  # noqa

order     = 1
l         = 1.3
angle     = 3*np.pi/180
rotate    = 90
name      = 'test'
K1        = 1.45
old_gamma = 20e3
new_gamma = 40e3




class slactrac_drift_test(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setUp(self):
        self.element = st.Drift(length=self._length, order=self._order, name=self._name)

    def R_test(self):
        r = np.array([[1, self._length, 0, 0, 0, 0],
                      [0, 1, 0, 0, 0, 0],
                      [0, 0, 1, self._length, 0, 0],
                      [0, 0, 0, 1, 0, 0],
                      [0, 0, 0, 0, 1, 0],
                      [0, 0, 0, 0, 0, 1]
                      ])
        self.assertTrue(np.array_equal(self.element.R, r))

basic_setup(slactrac_drift_test, length=l, order=order, name=name)


class slactrac_bend_test(unittest.TestCase):
    def setUp(self):
        self.element = st.Bend(length=self._length, angle=self._angle, order=self._order, rotate=self._rotate, name=self._name)

    def angle_test(self):
        self.assertEqual(self.element.angle, self._angle)

    def rotate_test(self):
        self.assertEqual(self.element.rotate, self._rotate)

    def R_test(self):
        r = np.array([[  1.00000000e+00 , 1.30000000e+00 , 0.00000000e+00  , 0.00000000e+00 , 0.00000000e+00 , 0.00000000e+00],
                      [ -1.65725745e-11 , 1.00000000e+00 , 0.00000000e+00  , 0.00000000e+00 , 0.00000000e+00 , 0.00000000e+00],
                      [ 0.00000000e+00  , 0.00000000e+00 , 9.98629535e-01  , 1.29940608e+00 , 0.00000000e+00 , 3.40261456e-02],
                      [ 0.00000000e+00  , 0.00000000e+00 , -2.10792635e-03 , 9.98629535e-01 , 0.00000000e+00 , 5.23359562e-02],
                      [ 0.00000000e+00  , 0.00000000e+00 , 5.23359562e-02  , 3.40261456e-02 , 1.00000000e+00 , 5.93922549e-04],
                      [ 0.00000000e+00  , 0.00000000e+00 , 0.00000000e+00  , 0.00000000e+00 , 0.00000000e+00 , 1.00000000e+00]])

        self.assertTrue(array_tol(self.element.R, r, 1e-10))

    def change_E_test(self):
        self   = change_E(self, old_gamma, new_gamma)
        ref    = 0.0261799387799
        tested = self.element.angle
        delta  = ref * 1e-12
        print('Calculated: {}, Reference: {}, Percent delta: {}'.format(tested, ref, (tested-ref)/ref))
        self.assertAlmostEqual(tested, ref, delta=delta)

basic_setup(slactrac_bend_test, length=l, order=order, name=name, angle=angle, rotate=rotate)


class slactrac_quad_test(unittest.TestCase):
    def setUp(self):
        self.element = st.Quad(length=l, K1=K1, order=order, name=name)

    def change_E_test(self):
        self = change_E(self, old_gamma, new_gamma)
        # print(self.element.K1)
        self.assertEqual(self.element.K1, 0.725)

basic_setup(slactrac_quad_test, length=l, order=order, name=name)


class slactrac_focus_test(unittest.TestCase):
    def setUp(self):
        self.element = st.Focus(length=l, K1=K1, order=order, name=name)

    def change_E_test(self):
        self   = change_E(self, old_gamma, new_gamma)
        ref    = 0.725
        tested = self.element.K1
        print('Calculated: {}, Reference: {}'.format(tested, ref))
        self.assertEqual(tested, ref)

basic_setup(slactrac_focus_test, length=l, K1=K1, order=order, name=name)

thickness = 50e-6
radlength = 12e-2


class slactrac_scatter_test(unittest.TestCase):
    def setUp(self):
        self.element = st.Scatter(thickness=thickness, radlength=radlength, name=name)

    def theta_rms_test(self):
        self   = change_E(self, old_gamma, new_gamma)
        tested = self.element.theta_rms(20.35)
        ref    = 9.607004924134313e-06
        delta  = 0
        print('Calculated: {}, Reference: {}'.format(tested, ref))
        self.assertAlmostEqual(tested, ref, delta=delta)

    def change_E_test(self):
        import inspect
        # self.assertTrue(hasattr(self.element.
        # self.assertAlmostEqual(self.element.K1, ref, places=13)

basic_setup(slactrac_scatter_test, thickness=thickness, radlength=radlength, name=name)
