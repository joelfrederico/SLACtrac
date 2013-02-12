import scipy as sp
import numpy as np
from baseclass import baseclass

class Drift(baseclass):
	def __init__(self,length=0,order=1):
		self._type = 'drift'
		self._length = float(length)
		self._order = int(order)

	def _Rfunc(self):
		self._R = driftmat(self._length,self._order)

	def _change_E(self,old_gamma,new_gamma):
		if not ( self._R == None ):
			self._Rfunc()

def driftmat(l=0,order=1):
	R_small = np.array(
			[[ 1 , l ],
			[  0 , 1 ]]
		)
	R = np.zeros([6,6])
	R[0:2,0:2] = R[2:4,2:4] = R_small
	R[4:6,4:6] = np.identity(2)
	return R
