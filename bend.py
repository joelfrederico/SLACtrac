import scipy as sp
import numpy as np
from driftmat import driftmat
from baseclass import baseclass

class Bend(baseclass):
	def __init__(self,length=0,angle=0,order=1):
		self._type = 'bend'
		self._length = length
		self._order = order
		self._angle = angle
		self._R = None

	def _Rfunc(self):
		self._R = bendmat(
				length=self._length,
				angle=self._angle,
				order=self._order
				)

	def _change_E(self,old_gamma,new_gamma):
		self._angle *= old_gamma / new_gamma
		if ( not self._R == None ):
			self._Rfunc()

def bendmat(
		length=0,
		angle=0,
		order=1,
		fse=0,
		K1=0,
		K2=0
	   ):

	if (( length==0 ) or ( angle==0 )):
		return driftmat(length,order)

	h     = angle/length            # /* coordinate system curvature */
	ha    = h*(1+fse)               # /* actual curvature due to bending field */
	n     = -K1/np.square(h)              # /* field index */
	beta  = K2/2/pow(h,3)            # /* sextupole index */
	gamma = 0

	t0=length
	nh = n*h
	betah2 = beta*np.square(h)
	gammah3 = gamma*pow(h,3)
	
	# M = sbend_matrix(length, h, ha, n*h, beta*sqr(h), gamma*pow3(h), order)
	h2 = h*h
	ha2 = ha*ha

	kx2 = -(h2 - 2*h*ha + nh*ha)
	ky2 = nh*ha
	ky2_is_zero = (ky2==0)
	kx2_is_zero = (kx2==0)

	small3 = pow(1e-16, 1./3.)

	if (np.sqrt(abs(kx2))*t0<small3):
		kx2 = np.square(small3/t0)
		if (kx2):
			kx2 = np.sign(kx2)*kx2


	if (kx2>0.0):
			kx = np.sqrt(kx2)
			cx = np.cos(kx*t0)
			sx = np.sin(kx*t0)/kx
	elif (kx2<0.0):
			kx = np.sqrt(-kx2)
			cx = np.cosh(kx*t0)
			sx = np.sinh(kx*t0)/kx


	if (abs(ky2)<small3):
		ky2 = np.square(small3/t0)
		if (ky2):
			ky2 = np.sign(ky2)*ky2

	if (ky2>0.0):
			ky = np.sqrt(ky2)
			cy = np.cos(ky*t0)
			sy = np.sin(ky*t0)/ky
	elif (ky2<0.0):
			ky = np.sqrt(-ky2)
			cy = np.cosh(ky*t0)
			sy = np.sinh(ky*t0)/ky

	R = np.identity(6)
	if (h!=0):
		R[0][0] = R[1][1] = cx;
		R[0][1] = sx;
		R[0][2] = R[0][3] = R[0][4] = 0;
		R[0][5] = -ha*(cx-1)/kx2;
		R[1][0] = -sx*kx2;
		R[1][2] = R[1][3] = R[1][4] = 0;
		R[1][5] = sx*ha;
		R[2][2] = R[3][3] = cy;
		R[2][3] = sy;
		R[2][0] = R[2][1] = R[2][4] = R[2][5] = 0;
		R[3][2] =  - sy*ky2;
		R[3][0] = R[3][1] = R[3][4] = R[3][5] = 0;
		R[4][0] = h*sx;
		R[4][1] = -(h*(cx - 1))/kx2;
		R[4][2] = R[4][3] = 0;
		R[4][5] = (h*ha*(t0 - sx))/kx2;
	else:
		# /* steering corrector */
		R[0][0] = R[1][1] = R[2][2] = R[3][3] = 1;
		R[0][1] = R[2][3] = t0;
		R[0][5] = C[0] + t0*sin(ha*t0);
		R[1][5] = t0*ha*cos(ha*t0);

	R[5][0] = R[5][1] = R[5][2] = R[5][3] = R[5][4] = 0;
	R[4][4] = R[5][5] = 1;
 
	
	return R
