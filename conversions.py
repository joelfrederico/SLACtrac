electron_mc2_gev = 0.510998910e-3

def gamma2GeV(gamma):
	return gamma*electron_mc2_gev

def GeV2gamma(E):
	return E/electron_mc2_gev
