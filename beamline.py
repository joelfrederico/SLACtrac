# import scipy as _sp
import numpy as _np
from baseclass import baseclass
import copy as _copy
from twiss import Twiss as _Twiss

class Beamline(baseclass):
	_type    = 'beamline'
	_order   = int(1)
	def __init__(self,element_list,gamma,twiss):
		self._gamma   = float(gamma)
		# print len(element_list)
		self.twiss = twiss
		self.elements = _np.array([])

		for element in element_list:
			self.elements = _np.append(self.elements,_copy.deepcopy(element))
		for element in self.elements:
			# element._gamma = self._gamma
			if ( element._order > self._order ):
				self._order = element._order

	# Define property length
	def _get_length(self):
		length = 0
		for element in self.elements:
			length += element._length
		return length
	length = property(_get_length,doc='The length of the beamline.')

	# Define transfer matrix R property
	def _getR(self):
		R = _np.identity(6)
		for i,element in enumerate(self.elements):
			R = _np.dot(element.R,R)
		return R
	R = property(_getR,doc='The transfer matrix R for the beamline.')

	# Define gamma property for beamlines
	# If you change gamma, it changes for all elements
	def _get_gamma(self):
		return self._gamma
	def _set_gamma(self,gamma):
		for element in self.elements:
			# Changes energy of element
			element.change_E(self._gamma,gamma)
		self._gamma = gamma
	gamma = property(_get_gamma,_set_gamma)

	def _get_twiss_end(self):
		return self.twiss.transport(self.R)
	twiss_end = property(_get_twiss_end)

