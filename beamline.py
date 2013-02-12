import scipy as sp
import numpy as np
from baseclass import baseclass

class Beamline(baseclass):
	def __init__(self,element_list=None,gamma=None):
		self._type = 'beamline'
		self._length  = float(0)
		self._order   = int(1)
		self._gamma   = float(gamma)
		self.R = None
		self.elements = np.array(element_list)
		
		for element in self.elements:
			element._gamma = self._gamma
			self._length += element._length
			if ( element._order > self._order ):
				self._order = element._order

		# Preserve settings
		self._history = np.array([self])

	def calc_mat(self):
		self.R = np.identity(6)
		for element in self.elements:
			element._Rfunc()
			self.R = np.dot(element._R,self.R)

	def change_energy(self,gamma):
		temp = self._history
		self = self._history[0]
		self._history = temp
		for element in self.elements:
			element._change_E(self._gamma,gamma)
		self._gamma = gamma
		if not (self.R == None):
			self.calc_mat()
		# Add new settings to the history
		self._history = np.append(self._history,self)

	def reset(self):
		temp = self._history
		self = self._history[0]
		self._history = np.append(temp,self)
