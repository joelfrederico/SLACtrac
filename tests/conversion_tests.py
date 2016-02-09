import unittest
import slactrac as st

E = 20.35
gamma = 39824


class conversion_tests(unittest.TestCase):
    def GeV2gamma_test(self):
        gamma = st.GeV2gamma(E)
        test  = 39823.95833089439
        delta = 0
        print('Evaluated: {}'.format(gamma))
        print('Delta: {}'.format(gamma-test))
        self.assertAlmostEqual(gamma, test, delta)

    def GeV2joule_test(self):
        joule = st.GeV2joule(E)
        test  = 3.2604293097750004e-09
        delta = 0
        print('Evaluated: {}'.format(joule))
        print('Delta: {}'.format(joule-test))
        self.assertAlmostEqual(joule, test, delta)

    def eV2joule_test(self):
        joule = st.eV2joule(E*1e9)
        test  = 3.2604293097750002e-09
        delta = 1e-15
        print('Evaluated: {}'.format(joule))
        print('Delta: {}'.format(joule-test))
        self.assertAlmostEqual(joule, test, delta=delta)

    def gamma2GeV_test(self):
        En    = st.eV2joule(gamma)
        test  = 6.3805079524560005e-15
        delta = 1e-21
        print('Evaluated: {}'.format(En))
        print('Delta: {}'.format(En-test))
        self.assertAlmostEqual(En, test, delta=delta)
