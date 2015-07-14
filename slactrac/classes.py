import numpy as np

__all__ = ['Bunch']


class Bunch(object):
    """
    A class representing a bunch of particles. (Unfinished)
    """
    def __init__(self, x, xp, y, yp, z, delta, parts=None):
        self._parts = np.zeros(6, np.size(x))

    @property
    def x(self):
        """
        An array of x coordinates for particles.
        """
        return self._parts[0, :]

    @x.setter
    def x(self, val):
        self._parts[0, :] = val

    def prop(self, beamline, gamma=None):
        """
        Propagates the bunch down a *beamline*. (Unfinished)
        """
        if gamma is None:
            gamma = beamline.gamma
