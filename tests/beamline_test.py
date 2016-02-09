import unittest
import numpy as np
import slactrac as st
from .base import array_tol

order     = 1
length    = 1.3
angle     = 3*np.pi/180
rotate    = 90
name      = 'test'
K1        = 1.45
old_gamma = 20e3
new_gamma = 40e3


class slactrac_beamline_test(unittest.TestCase):
    def setUp(self):
        drift = st.Drift(length=length, order=order, name=name)
        bend  = st.Bend(length=length, angle=angle, order=order, rotate=rotate, name=name)
        quad  = st.Quad(length=length, K1=K1, order=order, name=name)
        focus = st.Focus(length=length, K1=K1, order=order, name=name)

        self.element_list = np.array([drift, bend, quad, focus])
        self.beamline = st.Beamline(element_list=self.element_list, gamma=old_gamma)

    def R_test(self):
        r = np.array([[ -9.99941917e-01 , -2.59089846e+00 , 0.00000000e+00  , 0.00000000e+00  , 0.00000000e+00 , 0.00000000e+00]   ,
                      [ -1.29782553e-02 , -1.03368538e+00 , 0.00000000e+00  , 0.00000000e+00  , 0.00000000e+00 , 0.00000000e+00]   ,
                      [  0.00000000e+00 , 0.00000000e+00  , 2.29368629e+00  , 8.05287080e+00  , 0.00000000e+00 , 1.87354446e-01]   ,
                      [  0.00000000e+00 , 0.00000000e+00  , -2.98277724e+00 , -1.00362111e+01 , 0.00000000e+00 , -2.20823842e-01]  ,
                      [  0.00000000e+00 , 0.00000000e+00  , 5.23359562e-02  , 1.02062889e-01  , 1.00000000e+00 , 5.93922549e-04]   ,
                      [  0.00000000e+00 , 0.00000000e+00  , 0.00000000e+00  , 0.00000000e+00  , 0.00000000e+00 , 1.00000000e+00]])
        # print(self.beamline.R-r)
        self.assertTrue(array_tol(self.beamline.R, r, 1e-7))

    def change_verbose_default_test(self):
        for element in self.beamline.elements:
            self.assertFalse(element.verbose)
        self.assertFalse(self.beamline.verbose)

    def change_verbose_true_test(self):
        self.beamline.change_verbose(verbose=True)
        for element in self.beamline.elements:
            self.assertTrue(element.verbose)
        self.assertTrue(self.beamline.verbose)

    def change_verbose_false_test(self):
        self.beamline.change_verbose(verbose=True)
        self.beamline.change_verbose(verbose=False)
        for element in self.beamline.elements:
            self.assertFalse(element.verbose)
        self.assertFalse(self.beamline.verbose)

    def gamma_test(self):
        self.beamline.gamma = new_gamma
        self.assertEqual(self.beamline.gamma, new_gamma)

        r = np.array([[ -5.99618165e-01 , -6.19118714e-01 , 0.00000000e+00  , 0.00000000e+00  , 0.00000000e+00 , 0.00000000e+00]   ,
                      [ -6.81419174e-01 , -2.37130802e+00 , 0.00000000e+00  , 0.00000000e+00  , 0.00000000e+00 , 0.00000000e+00]   ,
                      [  0.00000000e+00 , 0.00000000e+00  , 1.95355200e+00  , 7.55081334e+00  , 0.00000000e+00 , 9.79361938e-02]   ,
                      [  0.00000000e+00 , 0.00000000e+00  , -7.63864674e-01 , -2.44057981e+00 , 0.00000000e+00 , -2.48946792e-02]  ,
                      [  0.00000000e+00 , 0.00000000e+00  , 2.61769483e-02  , 5.10460211e-02  , 1.00000000e+00 , 1.48495903e-04]   ,
                      [  0.00000000e+00 , 0.00000000e+00  , 0.00000000e+00  , 0.00000000e+00  , 0.00000000e+00 , 1.00000000e+00]])
        # print(self.beamline.R)
        self.assertTrue(array_tol(self.beamline.R, r, 1e-7))


