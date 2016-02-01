import os as _os
_on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not _on_rtd:
    import slactrac as _sltr
    import numpy as _np
    pass


def _store_emit(self, emit=None, emit_n=None):
    if (emit is None) and (emit_n is None):
        raise TypeError('Either emit or emit_n must be specified.')
    elif (emit is not None) and (emit_n is not None):
        raise TypeError('Emit and emit_n cannot be specified simultaneously.')
    elif emit is not None:
        self._emit = emit
    elif emit_n is not None:
        self._emit = emit_n/_sltr.GeV2gamma(self.E)
    else:
        raise TypeError('Something has gone wrong.')


class BeamBase(object):
    def __init__(self, nb0, E=20.35, dE=0.01, emit=None, emit_n=None):
        self._store_defaults(nb0, E, dE)
        _store_emit(emit=emit, emit_n=emit_n)

    def _store_defaults(self, nb0, E, dE):
        self._nb0 = nb0
        self._E   = E
        self._dE  = dE

    @property
    def nb0(self):
        """
        On-axis beam density.
        """
        return self._nb0

    @property
    def E(self):
        """
        Beam energy in GeV.
        """
        return self._E

    @property
    def dE(self):
        """
        Beam energy spread.
        """
        return self._dE

    @property
    def emit(self):
        """
        Beam emittance :math:`\\epsilon`.
        """
        return self._emit

    @property
    def emit_n(self):
        """
        Normalized beam emittance :math:`\\gamma \\epsilon`.
        """
        return self._emit*_sltr.GeV2gamma(self.E)


class RoundBeam(BeamBase):
    """
    Creates a beam with circularly-symmetric properties.

    Parameters
    ----------

    nb0 : float
        On-axis beam density.
    s_r : float
        The beam RMS width :math:`\\sigma_r`.
    E : float
        Beam energy in GeV.
    dE : float
        Beam energy spread.
    """
    def __init__(self, nb0, s_r, E=20.35, dE=0.01):
        super().__init__(nb0=nb0, E=E, dE=dE)
        self._s_r = s_r

    @property
    def s_r(self):
        """
        The beam RMS width :math:`\\sigma_r`.
        """
        return self._s_r


class EllipseBeam(BeamBase):
    """
    Creates an ellipsoidal beam.
    
    Either the set of parameters `sx`, `sxp`, and `sxxp` must be used; or `beta`, `alpha`, and `emit` or `emit_n` must be used.

    Parameters
    ----------

    nb0 : float
        On-axis beam density.
    E : float
        Beam energy in GeV.
    dE : float
        Beam energy spread.
    sx : float, optional
        Beam moment where :math:`\\text{sx}^2 = \\langle x^2 \\rangle`.
    sxp : float, optional
        Beam moment where :math:`\\text{sxp}^2 = \\langle x'^2 \\rangle`.
    sxxp : float, optional
        Beam moment where :math:`\\text{sxxp} = \\langle x x' \\rangle`.
    beta : float, optional
        Courant-Snyder parameter :math:`\\beta`.
    alpha : float, optional
        Courant-Snyder parameter :math:`\\alpha`.
    emit : float, optional
        Beam emittance :math:`\\epsilon`.
    emit_n : float, optional
        Normalized beam emittance :math:`\\gamma \\epsilon`.
    """
    def __init__(self, nb0, E=20.35, dE=0.01, sx=None, sxp=None, sxxp=None, beta=None, alpha=None, emit=None, emit_n=None):
        self._store_defaults(nb0, E, dE)
        try:
            self.set_Courant_Snyder(beta=beta, alpha=alpha, emit=emit, emit_n=emit_n)
        except:
            self.set_moments(sx=sx, sxp=sxp, sxxp=sxxp)

    def set_moments(self, sx, sxp, sxxp):
        """
        Sets the beam moments directly.

        Parameters
        ----------
        sx : float
            Beam moment where :math:`\\text{sx}^2 = \\langle x^2 \\rangle`.
        sxp : float
            Beam moment where :math:`\\text{sxp}^2 = \\langle x'^2 \\rangle`.
        sxxp : float
            Beam moment where :math:`\\text{sxxp} = \\langle x x' \\rangle`.
        """
        self._sx   = sx
        self._sxp  = sxp
        self._sxxp = sxxp
        emit = _np.sqrt(sx**2 * sxp**2 - sxxp**2)
        self._store_emit(emit=emit)

    @property
    def sx(self):
        """
        Beam moment where :math:`\\text{sx}^2 = \\langle x^2 \\rangle`.
        """
        return self._sx

    @property
    def sxp(self):
        """
        Beam moment where :math:`\\text{sxp}^2 = \\langle x'^2 \\rangle`.
        """
        return self._sxp

    @property
    def sxxp(self):
        """
        Beam moment where :math:`\\text{sxxp} = \\langle x x' \\rangle`.
        """
        return self._sxxp

    def set_Courant_Snyder(self, beta, alpha, emit=None, emit_n=None):
        """
        Sets the beam moments indirectly using Courant-Snyder parameters.

        Parameters
        ----------
        beta : float
            Courant-Snyder parameter :math:`\\beta`.
        alpha : float
            Courant-Snyder parameter :math:`\\alpha`.
        emit : float
            Beam emittance :math:`\\epsilon`.
        emit_n : float
            Normalized beam emittance :math:`\\gamma \\epsilon`.
        """

        self._store_emit(emit=emit, emit_n=emit_n)
        
        self._sx   = _np.sqrt(beta*self.emit)
        self._sxp  = _np.sqrt((1+alpha**2)/beta*self.emit)
        self._sxxp = -alpha*self.emit

    @property
    def beta(self):
        """
        Courant-Snyder parameter :math:`\\beta`.
        """
        beta = _np.sqrt(self.sx)/self.emit
        return beta

    @property
    def alpha(self):
        """
        Courant-Snyder parameter :math:`\\alpha`.
        """
        alpha = -self.sxxp/self.emit
        return alpha
