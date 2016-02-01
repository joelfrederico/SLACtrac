import os as _os
_on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not _on_rtd:
    import scipy.constants as _spc
    import scipy.special as _spsp
    import numpy as _np
    import scipy as _sp

    # ============================
    # Constants
    # ============================
    e      = _spc.e               # Elementary charge
    c      = _spc.speed_of_light  # Speed of light
    e0     = _spc.epsilon_0       # Vacuum permittivity
    amu    = _spc.atomic_mass     # AMU in kg

from .ions import Ions as _Ions
import logging as _logging
_logger = _logging.getLogger(__name__)


class Ions1D(_Ions):
    """
    A class to facilitate calculating ion motion in PWFA ion columns due to planar, infinitely-long gaussian beams.

    .. versionadded:: 1.7
    """
    def __init__(self, species, N_e, sig_x, sig_y, sig_xi, r0_big=None, n_samp=1000, order=5, rtol=None, atol=None):
        # ============================
        # Experiment Parameters
        # ============================
        super().__init__(dims=1, species=species, N_e=N_e, sig_xi=sig_xi, rtol=rtol, atol=atol)
        if sig_x < sig_y:
            raise ValueError('Assumption that (sig_x = {}) > (sig_y = {}) not met.'.format(sig_x, sig_y))
        else:
            self._sig_x  = sig_x   # Transverse R.M.S. width
            self._sig_y  = sig_y   # Transverse R.M.S. width

    def lambda_large(self, y0):
        """
        The wavelength for large (:math:`r_0 < \\sigma_r`) oscillations.
        """
        return 4*_np.sqrt(2*y0/self.k)

    # ============================
    # Omega for large r(0)
    # ============================
    # def omega_big(self, r0):
    #     omega_r0 = _np.sqrt(_np.pi*self.k/2)
    #     return omega_r0/_np.sqrt(r0)

    # ============================
    # Scale factor function
    # ============================
    def h(self, q):
        return 1

    @property
    def sig_x(self):
        """
        The R.M.S. width :math:`\\sigma_x`.
        """
        return self._sig_x

    @property
    def sig_y(self):
        """
        The R.M.S. width :math:`\\sigma_y`.
        """
        return self._sig_y

    @property
    def nb0(self):
        """
        On-axis beam density :math:`n_{b,0}`.
        """
        return self.N_e / (4*_np.sqrt(3) * _np.pi * self.sig_x * self.sig_y * self.sig_xi)

    @property
    def k(self):
        """
        Driving force term: :math:`r'' = -k \\left( \\frac{1-e^{-r^2/2{\\sigma_r}^2}}{r} \\right)`
        """
        try:
            return self._k
        except AttributeError:
            self._k = _np.sqrt(_np.pi/8) * e**2 * self.nb0 * self.sig_y / ( e0 * self.m * c**2)
            return self._k

    @property
    def k_small(self):
        """
        Small-angle driving force term: :math:`r'' = -k_{small} r`.

        Note: :math:`k_{small} = \\frac{k}{2{\\sigma_r^2}}`
        """
        return self.k * _np.sqrt(2/_np.pi) / self.sig_y
        # return e**2 * self.nb0 / (2 * e0 * self.m * c**2)

    # ============================
    # Force equation
    # ============================
    def _yp2(self, y):
        return -self.k*_spsp.erf(y/(_np.sqrt(2)*self.sig_y))
    
    # ============================
    # Derivative of force eq.
    # ============================
    def _delyp2(self, y):
        return - (self.k * _np.sqrt(2/_np.pi)/self.sig_y) * _np.exp(-y**2/(2*self.sig_y**2))

    # ============================
    # First-order ODE system
    # ============================
    def _func(self, y, t):
        return [self._yp2(y[1]), y[0]]

    # ============================
    # Gradient for 1st-order ODE
    # ============================
    def _gradient(self, y, t):
        return [[0, self._delyp2(y[1])], [1, 0]]

    @property
    def q_label(self):
        return 'y'
