import logging
logger=logging.getLogger(__name__)

__all__ = ['BDES2K']

def BDES2K(bdes,quad_length,energy):
	Brho = energy/0.029979
	K = bdes/(Brho*quad_length)
	logger.debug('Converted BDES: {bdes}, quad length: {quad_length}, energy: {energy} to K: {K}'.format(
		bdes        = bdes,
		quad_length = quad_length,
		energy      = energy,
		K           = K
		)
		)

	return K

