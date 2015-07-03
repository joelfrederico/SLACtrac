import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

__all__ = ['Bunch']

class Bunch(object):
    def __init__(self,x,xp,y,yp,z,delta,parts=None):
        self._parts = np.zeros(6,np.size(x))

    def _get_x(self):
        return self._parts[0,:]
    def _set_x(self,val):
        self._parts[0,:] = val
    x = property(_get_x,_set_x)

    def hist_xy(self,ax=None,fig=None,bins=50):
        if ax is None:
            if fig is None:
                ax = plt.gca()
            else:
                gs = gridspec.GridSpec(1,1)
                ax = fig.add_subplot(gs[0,0])

        hst = ax.hist2d(self.x,self.y,bins=bins)

        return hst

    def prop(self,beamline,gamma=None):
        if gamma is None:
            gamma = beamline.gamma
