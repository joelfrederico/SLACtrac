import os as _os
_on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not _on_rtd:
    import slactrac as _sltr
    import numpy as _np
    pass

from .beam import _store_emit


class GaussPartBeam(object):
    """
    Generates a Gaussian distribution of particles.

    Parameters
    ----------

    nparts : int
        Number of particles to use.
    q_tot : float
        Total charge of beam.
    E : float
        Average beam energy in GeV.
    sig_delta : float
        R.M.S. beam energy.
    beta : float
        Beam beta function.
    alpha : float
        Beam alpha function.
    emit : float
        Beam emittance.
    emit_n : float
        Normalized beam emittance.
    """
    def __init__(self, nparts, q_tot, E, sig_delta, sig_xi, beta, alpha, emit=None, emit_n=None):
        self._nparts    = _np.int(nparts)
        self._q_tot     = q_tot
        self._E         = E
        self._sig_delta = sig_delta
        self._sig_xi    = sig_xi
        self._beta      = beta
        self._alpha     = alpha
        _store_emit(self, emit=emit, emit_n=emit_n)

        cov      = _np.array([[self.beta, -self.alpha], [-self.alpha, (1+self.alpha**2)/self.beta]])*self.emit
        mean     = _np.array([0, 0])

        self._cov  = cov
        self._mean = mean

        coords   = _np.random.multivariate_normal(mean, cov, self.nparts)
        self._x  = coords[:, 0]
        self._xp = coords[:, 1]

        if sig_delta == 0:
            self._delta = _np.zeros(nparts)
        else:
            self._delta = _np.random.normal(scale=self.sig_delta, size=self.nparts)

        if sig_xi == 0:
            self._xi = _np.zeros(nparts)
        else:
            self._xi = _np.random.normal(scale=self.sig_xi, size=self.nparts)

    @property
    def sig_xi(self):
        """
        Std. dev. of :math:`\\xi`: :math:`\\sigma_\\xi`.
        """
        return self._sig_xi

    @property
    def xi(self):
        """
        Particle coordinates :math:`\\xi`.
        """
        return self._xi

    @property
    def mean(self):
        """
        Mean for x, x'.
        """
        return self._mean

    @property
    def cov(self):
        """
        Covariance for x, x'.
        """
        return self._cov

    @property
    def nparts(self):
        """
        Number of particles in the beam.
        """
        return self._nparts

    @property
    def x(self):
        """
        Particle coordinates :math:`x`.
        """
        return self._x

    @property
    def xp(self):
        """
        Particle coordinates :math:`x'`.
        """
        return self._xp

    @property
    def delta(self):
        """
        Particle coordinates :math:`\\delta`.
        """
        return self._delta

    @property
    def emit(self):
        """
        Beam emittance :math:`\\epsilon`.
        """
        return self._emit

    @property
    def E(self):
        """
        Beam energy in GeV.
        """
        return self._E

    @property
    def sig_delta(self):
        """
        Beam energy spread :math:`\\sigma_\\delta`.
        """
        return self._sig_delta

    @property
    def beta(self):
        """
        Beam beta :math:`\\beta`.
        """
        return self._beta

    @property
    def alpha(self):
        """
        Beam alpha :math:`\\alpha`.
        """
        return self._alpha
