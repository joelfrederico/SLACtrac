import scipy as sp
import numpy as np
from driftmat import driftmat
from baseclass import baseclass

class Quad(baseclass):
	def __init__(self,length=0,K1=0,order=1):
		self._order = int(order)
		self._type = 'quad'
		self._length = float(length)
		self._K1 = float(K1)
		# print 'K1 is {}'.format(K1)
		self._R = None

	def _Rfunc(self):
		self._R = quadmat(L=self._length,K1=self._K1,order=self._order)

	# Works for gamma, E= gamma * mc^2.
	def _change_E(self,old_gamma,new_gamma):
		self._K1 *= old_gamma / new_gamma
		# print self._K1
		if ( not self._R == None ):
			self._Rfunc()

	def _change_K(self,K1):
		self._K1 = K1
		if ( not self._R == None ):
			self._Rfunc()

	def __setattr__(self,name,value):
		# Generally, set attribute
		super(Quad,self).__setattr__(name,value)

		# If 'elements' changes, calc R matrix after.
		if name=='_K1':
			print 'Recalculating R matrix for quad...'
			self._Rfunc()

def quadmat(K1=0,L=0,order=1):
	if ( K1 == 0 ):
		R = driftmat(L,order)
	else:
		rtK = np.sqrt(np.abs(K1))
		rtK_L = rtK * L
		# print rtK_L
		sin_rtK_L = np.sin(rtK_L)
		cos_rtK_L = np.cos(rtK_L)
		sinh_rtK_L = np.sinh(rtK_L)
		cosh_rtK_L = np.cosh(rtK_L)
		R_f = np.array(
				[[ cos_rtK_L    , sin_rtK_L/rtK ],
				[  -rtK*sin_rtK_L , cos_rtK_L   ]]
			)
		R_d = np.array(
				[[ cosh_rtK_L   , sinh_rtK_L/rtK ],
				[  rtK*sinh_rtK_L , cosh_rtK_L   ]]
			)

		if ( K1 > 0 ):
			R = np.zeros([6,6])
			R[0:2,0:2] = R_f
			R[2:4,2:4] = R_d
			R[4:6,4:6] = np.identity(2)
		elif ( K1 < 0 ):
			R = np.zeros([6,6])
			R[0:2,0:2] = R_d
			R[2:4,2:4] = R_f
			R[4:6,4:6] = np.identity(2)
	return R
