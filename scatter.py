import numpy as _np
from baseclass import baseclass
import copy as _copy
from Twiss import Twiss as _Twiss
import warnings

class Scatter(baseclass):
	_type = 'scatter'
	_order = 1
	def __init__(self,thickness=0,radlength=1,name=None,verbose=False):
		self.name   = name
		self.verbose = verbose
		self._x      = thickness
		self._X0     = radlength

	def theta_rms(self,energy_GeV):
		x_div_X0 = self._x/self._X0
		theta = 13.6e-3/energy_GeV * _np.sqrt(x_div_X0) * (1+0.038*_np.log(x_div_X0))
		return theta
	# theta_rms = property(_get_theta_rms)

	def _get_R(self):
		warnings.warn('This scatter element does not have an R matrix: returning identity instead',UserWarning,stacklevel=3)
		return _np.identity(6)
	R = property(_get_R)

	def change_E(self,old_gamma,new_gamma):
		pass
