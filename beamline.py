# import scipy as _sp
import numpy as _np
from baseclass import baseclass
import copy as _copy

class Beamline(baseclass):
	_type    = 'beamline'
	_order   = int(1)
	def __init__(self,element_list=None,gamma=None,twisspars=[None,None]):
		self._gamma   = float(gamma)
		# print len(element_list)
		self.twiss = twiss(twisspars[0],twisspars[1])
		self.elements = _np.array([])

		for element in element_list:
			self.elements = _np.append(self.elements,_copy.deepcopy(element))
		for element in self.elements:
			element._gamma = self._gamma
			if ( element._order > self._order ):
				self._order = element._order

		# Preserve settings
		self._history = _np.array([self])

	# Define property length
	def get_length(self):
		length = 0
		for element in self.elements:
			length += element._length
		return length
	length = property(get_length,doc='The length of the beamline.')

	# Define transfer matrix R property
	def getR(self):
		R = _np.identity(6)
		T = _np.array([[self.twiss.beta,-self.twiss.alpha],[-self.twiss.alpha,self.twiss.gamma]])
		self.betaf = _np.zeros(len(self.elements)+1)
		self.betaf[0] = self.twiss.beta
		for i,element in enumerate(self.elements):
			# element._Rfunc()
			R = _np.dot(element.R,R)
			T2 = _np.dot(_np.dot(R[0:2,0:2],T),_np.transpose(R[0:2,0:2]))
			self.betaf[i+1] = T2[0,0]
		return R
	R = property(getR,doc='The transfer matrix R for the beamline.')

	# Define gamma property for beamlines
	# If you change gamma, it changes for all elements
	def get_gamma(self):
		return self._gamma
	def set_gamma(self,gamma):
		for element in self.elements:
			# Changes energy of element
			element.change_E(self._gamma,gamma)
		self._gamma = gamma
	gamma = property(get_gamma,set_gamma)

class twiss:
	def __init__(self,beta=None,alpha=None):
		if beta == None:
			self.alpha  = 0
			self.beta   = 0
			self.gamma  = 0
			self._valid = False
		else:
			self.alpha  = alpha
			self.beta   = beta
			self.gamma  = (1+_np.power(self.alpha,2))/self.beta
			self._valid = True
