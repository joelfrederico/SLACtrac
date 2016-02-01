import os as _os
_on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not _on_rtd:
    import scipy.constants as _spc
    import numpy as _np
    import scipy as _sp

    # ============================
    # Constants
    # ============================
    e      = _spc.e               # Elementary charge
    c      = _spc.speed_of_light  # Speed of light
    e0     = _spc.epsilon_0       # Vacuum permittivity
    amu    = _spc.atomic_mass     # AMU in kg


class Ions(object):
    def __init__(self, dims, species, N_e, sig_xi, rtol=None, atol=None):
        self._dims    = dims
        self._species = species
        self._N_e     = N_e
        self._sig_xi  = sig_xi
        self._rtol = rtol
        self._atol = atol

    @property
    def rtol(self):
        return self._rtol

    @property
    def atol(self):
        return self._atol

    @property
    def species(self):
        """
        The species of gas used (see :class:`periodictable.core.Element`).

        For instance:

            >>> periodictable.hydrogen
        """
        return self._species
    
    @property
    def dims(self):
        """
        Number of dimensions.
        """
        return self._dims

    @property
    def lambda_small(self):
        """
        The wavelength for small (:math:`r_0 < \\sigma_r`) oscillations.
        """
        return 2*_np.pi/_np.sqrt(self.k_small)

    # ============================
    # Omega for large q(0)
    # ============================
    def omega_big(self, q0):
        return 2*_np.pi/self.lambda_large(q0)

    @property
    def m(self):
        """
        Ion mass.
        """
        return amu * self.species.mass

    @property
    def A(self):
        """
        Ion mass in units of AMU.
        """
        return self.species.mass

    @property
    def N_e(self):
        """
        Number of electrons in bunch.
        """
        return self._N_e

    @property
    def sig_xi(self):
        """
        Longitudinal R.M.S. width :math:`\\sigma_\\xi`.
        """
        return self._sig_xi

    def q(self, x, q0):
        """
        Numerically solved trajectory function for initial conditons :math:`q(0) = q_0` and :math:`q'(0) = 0`.
        """
        y1_0 = q0
        y0_0 = 0
        y0   = [y0_0, y1_0]

        y = _sp.integrate.odeint(self._func, y0, x, Dfun=self._gradient, rtol=self.rtol, atol=self.atol)

        return y[:, 1]

    @property
    def q_label(self):
        return 'q'
