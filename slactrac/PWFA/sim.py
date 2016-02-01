import os as _os
_on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not _on_rtd:
    import slactrac as _sltr
    import numpy as _np
    pass

from .plasma import Plasma as _Plasma
from .particles import GaussPartBeam as _GaussPartBeam
import scipy.constants as spc


class SimBeam(object):
    """
    Simulates beam particles in a plasma, given certain initial conditions.

    Parameters
    ----------

    plasma : 
    E0 : float
        Mean beam energy.
    n_p_cgs : float
        Plasma density in CGS units.
    nparts : int
        Number of particles to use in simulation
    beta_mismatch : float
        Factor to mismatch distribution in beta by.
    s_pts : int
        Number of points to simulate in s.
    """
    def __init__(self, plasma, beam, E0, n_p_cgs, nparts, beta_mismatch, s_pts):
        self._E0            = E0
        self._n_p_cgs       = n_p_cgs
        self._nparts        = nparts
        self._beta_mismatch = beta_mismatch
        self._s_pts         = s_pts
        self._plasma        = plasma
        self._beam          = beam

        # ==================================
        # Set up coordinate arrays
        # ==================================
        s = _np.linspace(0, 20*2*_np.pi*self.plasma.beta_matched(E0), s_pts)
        self._s = s
        y = _np.empty([nparts, s.shape[0], 2])
        self._phi = _np.empty([nparts, s.shape[0]])
        
        # ==================================
        # Defaults of motion
        # ==================================
        k0 = self.plasma.k_ion(E0)
        rtk0 = _np.sqrt(k0)

        k_xi = _np.sqrt(spc.elementary_charge**2 * self._n_p_cgs / (4*_np.pi*spc.epsilon_0*spc.electron_mass*spc.speed_of_light**2) ) / _np.cos(self.beam.xi) 

        self._k_xi = k_xi
        
        # ==================================
        # Get particle coordinates
        # ==================================
        for i, delta in enumerate(self.beam.delta):
            E = self.beam.E * (1+delta)
            plas = _Plasma(n_p_cgs=self._n_p_cgs/(_np.cos(k_xi[i] * self.beam.xi[i])**2))
            k = plas.k_ion(E)
            # k = self.plasma.k_ion(E)
            rtk = _np.sqrt(k)
            x0 = self.beam.x[i]
            xp0 = self.beam.xp[i]
            # y0 = [beam.xp[i], beam.x[i]]
            # y[i, :, :] = sp.integrate.odeint(self.ion_force, y0, s, args=(E,))
            y[i, :, 0] = -x0*rtk*_np.sin(rtk*s) + xp0*_np.cos(rtk*s)
            y[i, :, 1] = x0*_np.cos(rtk*s) + xp0*_np.sin(rtk*s)/rtk
            self._phi[i, :] = _np.mod((rtk-rtk0)*s+_np.pi, 2*_np.pi) - _np.pi
        
        # ==================================
        # Extract particle coordinates
        # ==================================
        self._x = y[:, :, 1]
        self._xp = y[:, :, 0]

    @property
    def k_xi(self):
        """
        Ion focusing wavenumber :math:`k_\\xi`.
        """
        return self._k_xi


    @property
    def phi(self):
        """
        Particle phases :math:`\\phi`.
        """
        return self._phi

    @property
    def beam(self):
        """
        Initial beam object.
        """
        return self._beam

    @property
    def plasma(self):
        """
        Initial plasma object.
        """
        return self._plasma

    @property
    def s(self):
        """
        Coordinates of beam (:math:`s`).
        """
        return self._s
    
    @property
    def x(self):
        """
        Coordinates of beam (:math:`x`).
        """
        return self._x

    @property
    def xp(self):
        """
        Coordinates of beam (:math:`x'`).
        """
        return self._xp

    # ==================================
    # Integrate particles
    # ==================================
    def ion_force(self, y, t, E):
        xp = y[0]
        x  = y[1]
        return [-self.plasma.k_ion(E)*x, xp]

    @property
    def spotsq(self):
        """
        The beam variance :math:`\\langle x^2 \\rangle`.
        """
        return _np.mean(self.x**2, axis=0)

    @property
    def divsq(self):
        """
        The beam divergence :math:`\\langle x'^2 \\rangle`.
        """
        return _np.mean(self.xp**2, axis=0)

    @property
    def xxp(self):
        """
        The beam correlation :math:`\\langle x x' \\rangle`.
        """
        return _np.mean(self.x*self.xp, axis=0)
    
    @property
    def emit_measured(self):
        """
        The beam emittance :math:`\\langle x x' \\rangle`.
        """
        return _np.sqrt(self.spotsq*self.divsq-self.xxp**2)
