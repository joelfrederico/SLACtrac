import os as _os
_on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not _on_rtd:
    import numpy as _np
    import slactrac as _sltr
    import scipy.constants as _spc
    import periodictable as _pt
    from .plasma import Plasma as _Plasma
else:
    import unittest.mock as _mock
    _pt = _mock.MagicMock()


class Match(object):
    """
    Given a *plasma* of type :class:`Plasma <scisalt.PWFA.Plasma>` and a beam of energy *E* in GeV and normalized emittance *emit_n* in SI units, calculates match parameters
    """
    def __init__(self, plasma, E, emit_n):
        self.plasma = plasma
        self.E = E
        self.emit_n = emit_n

    @property
    def gamma(self):
        """
        Relativistic :math:`\\gamma` of beam
        """
        return _sltr.GeV2gamma(self.E)

    @gamma.setter
    def gamma(self, value):
        self.E = _sltr.gamma2GeV(value)

    @property
    def emit_n(self):
        """
        Normalized emittance of beam :math:`\\epsilon_n = \\gamma\\epsilon`
        """
        return self.emit * self.gamma

    @emit_n.setter
    def emit_n(self, value):
        self._emit = value / self.gamma

    @property
    def emit(self):
        """
        Emittance of the beam, :math:`\\epsilon = \\sqrt{ \\langle x^2 \\rangle \\langle {x'}^2 \\rangle - \\langle x x' \\rangle^2 }`
        """
        return self._emit

    @property
    def sigma(self):
        """
        Spot size of matched beam :math:`\\left( \\frac{2 E \\varepsilon_0 }{ n_p e^2 } \\right)^{1/4} \\sqrt{\\epsilon}`
        """
        return _np.power(2*_sltr.GeV2joule(self.E)*_spc.epsilon_0 / (self.plasma.n_p * _np.power(_spc.elementary_charge, 2)) , 0.25) * _np.sqrt(self.emit)

    def beta(self, E):
        """
        :math:`\\beta` function of matched beam
        """
        return 1.0 / _np.sqrt(self.plasma.k_ion(E))
        # return 1.0 / _np.sqrt(2)

    @property
    def sigma_prime(self):
        """
        Divergence of matched beam
        """
        return _np.sqrt(self.emit/self.beta(self.E))


class MatchPlasma(object):
    """
    Given a beam of energy *E* in GeV with normalized emittance
    *emit_n* in SI units and spot size *sigma*, calculates plasma
    parameters

    Parameters
    ----------
    E : float
        Beam energy in GeV.
    emit_n : float
        Specified beam emittance :math:`\\epsilon`.
    sigma : float
        Specified beam spot size :math:`\\sigma`.
    """
    def __init__(self, E, emit_n, sigma):
        self.E = E
        self.emit_n = emit_n
        self.sigma = sigma

    @property
    def gamma(self):
        """
        Relativistic :math:`\\gamma` of beam
        """
        return _sltr.GeV2gamma(self.E)

    @gamma.setter
    def gamma(self, value):
        self.E = _sltr.gamma2GeV(value)

    @property
    def emit_n(self):
        """
        Specified beam emittance :math:`\\epsilon`.
        """
        return self.emit * self.gamma

    @emit_n.setter
    def emit_n(self, value):
        """
        Specified normalized beam emittance :math:`\\gamma \\epsilon`.
        """
        self.emit = value / self.gamma

    @property
    def beta(self):
        """
        The Courant-Snyder parameter :math:`\\beta` that is matched.
        """
        return self.sigma**2/self.emit

    @property
    def n_p(self):
        """
        The plasma density in SI units.
        """
        return 2*_sltr.GeV2joule(self.E)*_spc.epsilon_0 / (self.beta*_spc.elementary_charge)**2

    @property
    def n_p_cgs(self):
        """
        The plasma density in CGS units.
        """
        return self.n_p*1e-6

    @property
    def plasma(self, species=_pt.hydrogen):
        """
        The matched :class:`Plasma`.
        """
        return _Plasma(self.n_p, species=species)
