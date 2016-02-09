import unittest
import numpy as np
import slactrac as st
from .base import array_tol
from .base import *  # noqa

beta     = 1e-2
alpha    = 0.3
emit_n   = 50e-6
gamma_en = 39824


class slactrac_BeamParams_test(unittest.TestCase):
    def setUp(self):
        self.beamparams = st.BeamParams(beta=beta, alpha=alpha, emit_n=emit_n, gamma_en=gamma_en)

    def T_test(self):
        test = np.array([[  1.00000000e-02 , -3.00000000e-01]  ,
                         [ -3.00000000e-01 , 1.09000000e+02]])
        T = self.beamparams.T
        print(T)
        print(T-test)
        self.assertTrue(array_tol(test, T, 1e-323))

    def avg_xxp_test(self):
        test  = -3.76657292085e-10
        avg_xxp = self.beamparams.avg_xxp
        delta = 1e-21
        print(avg_xxp)
        print(avg_xxp-test)
        self.assertAlmostEqual(avg_xxp, test, delta=delta)

basic_setup(slactrac_BeamParams_test, testname='beamparams', beta=beta, alpha=alpha)
