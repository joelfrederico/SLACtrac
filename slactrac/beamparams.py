import os as _os
on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not on_rtd:
    import numpy as _np


class BeamParams(object):
    """
    Calculates Courant-Snyder parameters and beam properties in a self-consistent manner.

    Parameters
    ----------

    beta : float
        Beta function value in meters.
    alpha : float
        Alpha function value.
    emit : float
        Emittance in SI units.
    emit_n : float
        Normalized emittance in SI units.
    gamma_en : float
        Relativistic gamma :math:`\\gamma`
    spotsize : float
        RMS of :math:`x` coordinate.
    divergence : float
        RMS of :math:`x'` coordinate.
    r : float
        The average correlation of :math:`x` and :math:`x'`.
    avg_xxp : float
        The average correlation of :math:`x` and :math:`x'`.
    """
    def __repr__(self):
        return '<{} at {}; beta={}, alpha={}>'.format(self.__class__.__module__, hex(id(self)), self.beta, self.alpha)

    def __init__(self,
            beta=None, alpha=None, emit=None, emit_n=None, gamma_en=None,
            spotsize=None, divergence=None, r=None, avg_xxp=None):
        # If not enough info for Twiss
        emit_norm_insufficient = (emit_n is None) or (gamma_en is None)
        emit_geom_insufficient = emit is None
        emit_insufficient      = (emit_geom_insufficient and emit_norm_insufficient)
        shape_insufficient     = (beta is None) or (alpha is None)
        twiss_insufficient     = (shape_insufficient or emit_insufficient)
        moments_insufficient   = (spotsize is None) or (divergence is None) or ( (r is None) and (avg_xxp is None) )

        # Validation that there's enough info to construct everything
        if twiss_insufficient and moments_insufficient:
            raise ValueError('Not enough information to construct Twiss values')

        if twiss_insufficient:
            if avg_xxp is not None:
                emit = _np.sqrt(spotsize**2 * divergence**2 - avg_xxp**2)
                corr_sign = _np.sign(avg_xxp)
            elif r is not None:
                emit = spotsize * divergence * _np.sqrt(1-r**2)
                corr_sign = _np.sign(r)
            else:
                raise ValueError('Missing avg_xxp/r term')
            beta = spotsize**2/emit
            gamma = divergence**2/emit
            alpha = -corr_sign * _np.sqrt(gamma*beta-1)
        else:
            def _get_geom_emit(emit=None, emit_n=None, gamma=None):
                if emit is None and emit_n is None:
                    raise ValueError('Did not specify an emittance!')
                if emit is not None and emit_n is not None:
                    raise ValueError('Specified too many emittance values!')
                if emit_n is not None:
                    # print emit_n
                    emit = _np.float64(emit_n)/_np.float64(gamma)
                else:
                    emit = _np.float64(emit)
                return emit
            emit = _get_geom_emit(emit=emit, emit_n=emit_n, gamma=gamma_en)

        self.beta  = _np.float64(beta)
        self.alpha = _np.float64(alpha)
        self.emit  = _np.float64(emit)

    def set_emit_n(self, emit_n, gamma):
        """
        Set the normalized emittance of the beam.
        """
        self.emit = _np.float64(emit_n/gamma)

    # Definte beta property
    # Validate beta > 0
    @property
    def beta(self):
        """
        The beta function of the beam.
        """
        return self._beta

    @beta.setter
    def beta(self, value):
        if not (value > 0):
            raise ValueError('Beta must be greater than zero: requested beta={}.'.format(value))
        self._beta = value

    @property
    def alpha(self):
        """
        The alpha function of the beam.
        """
        return self._alpha

    @alpha.setter
    def alpha(self, value):
        self._alpha = value

    @property
    def betastar(self):
        """
        The minimum beta function of the beam in vacuum.
        """
        return 1.0/self.gamma

    @property
    def sstar(self):
        """
        The distance from the minimum beta function of the beam in vacuum.
        """
        return self.alpha/self.gamma

    # Define gamma property
    # Derived from beta and alpha
    @property
    def gamma(self):
        """
        The gamma function of the beam
        """
        return (1+_np.power(self.alpha, 2))/self.beta

    # Define T matrix
    # Derived from beta, alpha, and gamma
    @property
    def T(self):
        """
        The beam T matrix.
        """
        return _np.array([[self.beta, -self.alpha], [-self.alpha, self.gamma]])

    # Define transport method
    # Returns new twiss given R matrix.
    def transport(self, R):
        """
        Given a transport matrix *R*, return the new beam parameters.

        Returns :class:`slactrac.BeamParams`.
        """
        T2 = _np.dot(_np.dot(R, self.T), _np.transpose(R))
        betaf = T2[0, 0]
        alphaf = -T2[0, 1]
        return BeamParams(beta=betaf, alpha=alphaf, emit=self.emit)

    # Define spotsize method
    @property
    def spotsize(self):
        """
        The RMS size of the beam.
        """
        return _np.sqrt(self.beta*self.emit)

    @property
    def divergence(self):
        """
        The divergence of the beam.
        """
        return _np.sqrt(self.gamma*self.emit)

    @divergence.setter
    def divergence(self, value):
        self.emit = value**2/self.gamma

    @property
    def avg_xxp(self):
        """
        The average of coordinates :math:`x` and :math:`x'`.
        """
        return -self.alpha*self.emit

    @property
    def minspotsize(self):
        """
        The RMS size of the beam at its smallest in vacuum.
        """
        return _np.sqrt(self.betastar*self.emit)
