import scipy as sp
import numpy as np
from baseclass import baseclass
import copy

class Beamline(baseclass):
	def __init__(self,element_list=None,gamma=None,twisspars=[None,None]):
		self._type    = 'beamline'
		self._length  = float(0)
		self._order   = int(1)
		self._gamma   = float(gamma)
		self.R        = None
		# print len(element_list)
		self.elements = np.array([])
		self.twiss = twiss(twisspars[0],twisspars[1])

		for element in element_list:
			self.elements = np.append(self.elements,copy.deepcopy(element))
		for element in self.elements:
			element._gamma = self._gamma
			self._length += element._length
			if ( element._order > self._order ):
				self._order = element._order

		# Preserve settings
		self._history = np.array([self])

	def calc_mat(self):
		self.R = np.identity(6)
		T = np.array([[self.twiss.beta,-self.twiss.alpha],[-self.twiss.alpha,self.twiss.gamma]])
		self.betaf = np.zeros(len(self.elements)+1)
		self.betaf[0] = self.twiss.beta
		for i,element in enumerate(self.elements):
		# for element in self.elements:
			element._Rfunc()
			self.R = np.dot(element._R,self.R)
			T2 = np.dot(np.dot(self.R[0:2,0:2],T),np.transpose(self.R[0:2,0:2]))
			self.betaf[i+1] = T2[0,0]

	def change_energy(self,gamma):
		temp = self._history
		self = self._history[0]
		self._history = temp
		for element in self.elements:
			element._change_E(self._gamma,gamma)
			element._gamma = gamma
		self._gamma = gamma
		if not (self.R == None):
			self.calc_mat()
		# Add new settings to the history
		self._history = np.append(self._history,self)

	def reset(self):
		temp = self._history
		self = self._history[0]
		self._history = np.append(temp,self)

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
			self.gamma  = (1+np.power(self.alpha,2))/self.beta
			self._valid = True
