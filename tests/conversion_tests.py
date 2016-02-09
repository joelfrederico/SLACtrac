import unittest
import slactrac as st

E = 20.35
gamma = 39824


class conversion_tests(unittest.TestCase):
    def GeV2gamma_test(self):
        gamma = st.GeV2gamma(E)
        self.assertEqual(gamma, 39823.95833089439)

    def GeV2joule_test(self):
        joule = st.GeV2joule(E)
        self.assertEqual(joule, 3.2604293097750004e-09)

    def eV2joule_test(self):
        joule = st.eV2joule(E*1e9)
        test = 3.2604293097750002e-09
        print(joule-test)
        self.assertAlmostEqual(joule, test, delta=1e-24)

    def gamma2GeV_test(self):
        En    = st.eV2joule(gamma)
        test  = 6.3805079524560005e-15
        delta = 0
        print(En-test)
        self.assertAlmostEqual(En, test, delta=delta)
