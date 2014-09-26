import numpy as _np
from baseclass import baseclass

class Drift(baseclass):
	def __init__(self,length=0,order=1,name=None):
		self.name   = name
		self._type   = 'drift'
		self._length = _np.float64(length)
		self._order  = int(order)

	# Define transfer matrix property R
	def _get_R(self):
		return driftmat(self._length,self._order)
	R = property(_get_R)

	def change_E(self,old_gamma,new_gamma):
		pass

	def _get_length(self,verbose=False):
		if verbose:
			print 'This is a drift matrix'
		return self._length
	def _set_length(self,value):
		print 'Length changing for element ({}) from {} to {}'.format(self.name,self._length,value)
		self._length = _np.float64(value)
	length = property(fget=_get_length,fset=_set_length)

def driftmat(l=0,order=1):
	R_small = _np.array(
			[[ 1 , l ],
			[  0 , 1 ]]
		)
	R_small = _np.float_(R_small)

	R = _np.zeros([6,6])
	R[0:2,0:2] = R[2:4,2:4] = R_small
	R[4:6,4:6] = _np.float_(_np.identity(2))
	return R
