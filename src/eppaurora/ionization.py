# coding: utf-8
# Copyright (c) 2020 Stefan Bender
#
# This file is part of pyeppaurora.
# pyeppaurora is free software: you can redistribute it or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation, version 2.
# See accompanying LICENSE file or http://www.gnu.org/licenses/gpl-2.0.html.
"""Atmospheric ionization rate parametrizations

Includes the atmospheric ionization rate parametrizations for auroral
and medium-energy electron precipitation, 100 eV--1 MeV.

.. [#] Roble and Ridley, Ann. Geophys., 5A(6), 369--382, 1987
.. [#] Fang et al., J. Geophys. Res., 113, A09311, 2008
.. [#] Fang et al., Geophys. Res. Lett., 37, L22106, 2010
"""

import numpy as np

POLY_F2008 = np.array([
	[ 3.49979e-1, -6.18200e-2, -4.08124e-2,  1.65414e-2],
	[ 5.85425e-1, -5.00793e-2,  5.69309e-2, -4.02491e-3],
	[ 1.69692e-1, -2.58981e-2,  1.96822e-2,  1.20505e-3],
	[-1.22271e-1, -1.15532e-2,  5.37951e-6,  1.20189e-3],
	[ 1.57018,     2.87896e-1, -4.14857e-1,  5.18158e-2],
	[ 8.83195e-1,  4.31402e-2, -8.33599e-2,  1.02515e-2],
	[ 1.90953,    -4.74704e-2, -1.80200e-1,  2.46652e-2],
	[-1.29566,    -2.10952e-1,  2.73106e-1, -2.92752e-2]
])

POLY_F2010 = np.array([
	[ 1.24616E+0,  1.45903E+0, -2.42269E-1,  5.95459E-2],
	[ 2.23976E+0, -4.22918E-7,  1.36458E-2,  2.53332E-3],
	[ 1.41754E+0,  1.44597E-1,  1.70433E-2,  6.39717E-4],
	[ 2.48775E-1, -1.50890E-1,  6.30894E-9,  1.23707E-3],
	[-4.65119E-1, -1.05081E-1, -8.95701E-2,  1.22450E-2],
	[ 3.86019E-1,  1.75430E-3, -7.42960E-4,  4.60881E-4],
	[-6.45454E-1,  8.49555E-4, -4.28581E-2, -2.99302E-3],
	[ 9.48930E-1,  1.97385E-1, -2.50660E-3, -2.06938E-3]
])

POLY_F2013 = np.array([
	[ 2.55050e+0,  2.69476e-1, -2.58425e-1,  4.43190e-2],
	[ 6.39287e-1, -1.85817e-1, -3.15636e-2,  1.01370e-2],
	[ 1.63996e+0,  2.43580e-1,  4.29873e-2,  3.77803e-2],
	[-2.13479e-1,  1.42464e-1,  1.55840e-2,  1.97407e-3],
	[-1.65764e-1,  3.39654e-1, -9.87971e-3,  4.02411e-3],
	[-3.59358e-2,  2.50330e-2, -3.29365e-2,  5.08057e-3],
	[-6.26528e-1,  1.46865e+0,  2.51853e-1, -4.57132e-2],
	[ 1.01384e+0,  5.94301e-2, -3.27839e-2,  3.42688e-3],
	[-1.29454e-6, -1.43623e-1,  2.82583e-1,  8.29809e-2],
	[-1.18622e-1,  1.79191e-1,  6.49171e-2, -3.99715e-3],
	[ 2.94890e+0, -5.75821e-1,  2.48563e-2,  8.31078e-2],
	[-1.89515e-1,  3.53452e-2,  7.77964e-2, -4.06034e-3]
])

vpolyval = np.vectorize(np.polyval, signature='(m,n),()->(n)')


def rr1987(energy, flux, scale_height, rho):
	"""Atmospheric electron energy dissipation Roble and Ridley, 1987

	Equations (typo corrected) taken from Fang et al., 2008.

	Parameters
	----------
	energy: array_like (M,...)
		Characteristic energy E_0 [keV] of the Maxwellian distribution.
	flux: array_like (M,...)
		Integrated energy flux Q_0 [keV / cm² / s¹]
	scale_height: array_like (N,...)
		The atmospheric scale heights [cm].
	rho: array_like (N,...)
		The atmospheric mass density [g / cm³]

	Returns
	-------
	en_diss: array_like (M,N)
		The dissipated energy profiles.

	References
	----------

	.. [#] Roble and Ridley, Ann. Geophys., 5A(6), 369--382, 1987
	"""
	_c1 = 2.11685
	_c2 = 2.97035
	_c3 = 2.09710
	_c4 = 0.74054
	_c5 = 0.58795
	_c6 = 1.72746
	_c7 = 1.37459
	_c8 = 0.93296

	beta = (rho * scale_height / (4 * 1e-6))**(1 / 1.65)  # RR 1987, p. 371
	y = beta / energy  # Corrected in Fang et al. 2008 (4)
	f_y = (_c1 * (y**_c2) * np.exp(-_c3 * (y**_c4)) +
		_c5 * (y**_c6) * np.exp(-_c7 * (y**_c8)))
	# Corrected in Fang et al. 2008 (2)
	en_diss = 0.5 * flux / scale_height * f_y
	return en_diss


def rr1987_mod(energy, flux, scale_height, rho):
	"""Atmospheric electron energy dissipation Roble and Ridley, 1987

	Equations (typo corrected) taken from Fang et al., 2008.
	Modified polynomial values to get closer to Fang et al., 2008,
	origin unknown.

	Parameters
	----------
	energy: array_like (M,...)
		Characteristic energy E_0 [keV] of the Maxwellian distribution.
	flux: array_like (M,...)
		Integrated energy flux Q_0 [keV / cm² / s¹]
	scale_height: array_like (N,...)
		The atmospheric scale heights [cm].
	rho: array_like (N,...)
		The atmospheric mass density [g / cm³]

	Returns
	-------
	en_diss: array_like (M,N)
		The dissipated energy profiles.

	References
	----------

	.. [#] Roble and Ridley, Ann. Geophys., 5A(6), 369--382, 1987
	"""
	# Modified polynomial, origin unknown
	_c1 = 3.233
	_c2 = 2.56588
	_c3 = 2.2541
	_c4 = 0.7297198
	_c5 = 1.106907
	_c6 = 1.71349
	_c7 = 1.8835444
	_c8 = 0.86472135

	# Fang et al., 2008, Eq. (4)
	y = (rho * scale_height / (4.6 * 1e-6))**(1 / 1.65) / energy
	f_y = (_c1 * (y**_c2) * np.exp(-_c3 * (y**_c4)) +
		_c5 * (y**_c6) * np.exp(-_c7 * (y**_c8)))
	# energy dissipated [keV]
	en_diss = 0.5 * flux / scale_height * f_y
	return en_diss


def fang2008(energy, flux, scale_height, rho, pij=POLY_F2008):
	"""Atmospheric electron energy dissipation from Fang et al., 2008

	Ionization profile parametrization as derived in Fang et al., 2008 [#]_.

	Parameters
	----------
	energy: array_like (M,...)
		Characteristic energy E_0 [keV] of the Maxwellian distribution.
	flux: array_like (M,...)
		Integrated energy flux Q_0 [keV / cm² / s¹]
	scale_height: array_like (N,...)
		The atmospheric scale height(s) [cm].
	rho: array_like (N,...)
		The atmospheric densities [g / cm³], corresponding to the scale heights.

	Returns
	-------
	en_diss: array_like (M,N)
		The dissipated energy profile(s).

	References
	----------

	.. [#] Fang et al., J. Geophys. Res., 113, A09311, 2008, doi: 10.1029/2008JA013384
	"""
	def _f_y(_cc, _y):
		# Fang et al., 2008, Eq. (6)
		_c = _cc.reshape((8, -1))
		return (_c[0] * (_y**_c[1]) * np.exp(-_c[2] * (_y**_c[3])) +
			_c[4] * (_y**_c[5]) * np.exp(-_c[6] * (_y**_c[7])))
	# Fang et al., 2008, Eq. (7)
	_cs = np.exp(vpolyval(pij[:, ::-1].T, np.log(energy))).T
	# Fang et al., 2008, Eq. (4)
	y = (rho * scale_height / (4e-6))**(1 / 1.65) / energy
	f_y = _f_y(_cs, y)
	# Fang et al., 2008, Eq. (2)
	en_diss = 0.5 * f_y * flux / scale_height
	return en_diss


def fang2010_mono(energy, flux, scale_height, rho, pij=POLY_F2010):
	r"""Atmospheric electron energy dissipation from Fang et al., 2010

	Parametrization for mono-energetic electrons [#]_.

	Parameters
	----------
	energy: array_like (M,...)
		Characteristic energy E_0 [keV] of the Maxwellian distribution.
	flux: array_like (M,...)
		Integrated energy flux Q_0 [keV / cm² / s¹]
	scale_height: array_like (N,...)
		The atmospheric scale heights.
	rho: array_like (N,...)
		The atmospheric densities, corresponding to the scale heights.

	Returns
	-------
	en_diss: array_like (M,N)
		The dissipated energy profile(s).

	References
	----------

	.. [#] Fang et al., Geophys. Res. Lett., 37, L22106, 2010, doi: 10.1029/2010GL045406
	"""
	def _f_y(_cc, _y):
		# Fang et al., 2008, Eq. (6), Fang et al., 2010 Eq. (4)
		_c = _cc.reshape((8, -1))
		return (_c[0] * (_y**_c[1]) * np.exp(-_c[2] * (_y**_c[3])) +
			_c[4] * (_y**_c[5]) * np.exp(-_c[6] * (_y**_c[7])))
	# Fang et al., 2010, Eq. (5)
	_cs = np.exp(vpolyval(pij[:, ::-1].T, np.log(energy))).T
	# Fang et al., 2010, Eq. (1)
	y = 2. / energy * (rho * scale_height / (6e-6))**(0.7)
	f_y = _f_y(_cs, y)
	# Fang et al., 2008, Eq. (2)
	en_diss = f_y * flux / scale_height
	return en_diss


def fang2010_spec_int(ens, dfluxes, scale_height, rho, pij=POLY_F2010, axis=-1):
	r"""Integrate over a given energy spectrum

	Integrates over the mono-energetic parametrization `q` from Fang et al., 2010
	using the given differential particle spectrum `phi`:

	:math:`\int_\text{spec} \phi(E) q(E, Q) E \text{d}E`

	Parameters
	----------
	ens: array_like (M,...)
		Central (bin) energies of the spectrum
	dfluxes: array_like (M,...)
		Differential particle fluxes in the given bins
	scale_height: array_like (N,...)
		The atmospheric scale heights
	rho: array_like (N,...)
		The atmospheric densities, corresponding to the
		scale heights.

	Returns
	-------
	en_diss: array_like (N)
		The dissipated energy profile(s).
	"""
	ediss_f10 = fang2010_mono(
		ens[None, None, :],
		dfluxes,
		scale_height[..., None],
		rho[..., None],
		pij=pij,
	)
	return np.trapz(ediss_f10 * ens, ens, axis=axis)


def maxwell_general(en, en_0=10.):
	"""Maxwell number flux spectrum as in Fang2008 [1]

	Defined in Fang et al., JGR 2008, Eq. (1).

	Parameters
	----------
	en: float
		Energy in [keV]
	en_0: float, optional
		Characteristic energy in [keV], i.e. mode of the distribution.
		Default: 10 keV

	Returns
	-------
	phi: float
		Differential hemispherical number flux in [keV-1 cm-2 s-1]
		([keV] or scaled by 1 keV-2 cm-2 s-1, e.g. ).
	"""
	return en * np.exp(-en / en_0)


def maxwell_pflux(en, en_0=10.):
	"""Maxwell particle flux spectrum as in Fang2008 [1]

	Defined in Fang et al., JGR 2008, Eq. (1).
	The total precipitating energy flux is fixed to 1 keV cm-2 s-1,
	multiply by Q_0 [keV cm-2 s-1] to scale the particle flux.

	Parameters
	----------
	en: float
		Energy in [keV]
	en_0: float, optional
		Characteristic energy in [keV], i.e. mode of the distribution.
		Default: 10 keV.

	Returns
	-------
	phi: float
		Hemispherical differential particle flux in [keV-1 cm-2 s-1]
		([kev-2] scaled by unit energy flux).
	"""
	return 0.5 / en_0**3 * maxwell_general(en, en_0)


def fang2010_maxw_int(energy, flux, scale_height, rho, bounds=(0.1, 300.), nstep=128, pij=POLY_F2010):
	"""
	Integrate the mono-energetic parametrization over a Maxwellian

	Parameters
	----------
	bounds: tuple, optional
		(min, max) [keV] of the integration range to integrate the Maxwellian.
		Make sure that this is appropriate to encompass the spectrum.
		Default: (0.1, 300.)
	nsteps: int, optional
		Number of integration steps, default: 128.
	"""
	bounds_l10 = np.log10(bounds)
	ens = np.logspace(*bounds_l10, num=nstep)
	dflux = flux * maxwell_pflux(ens[:, None], energy)
	return fang2010_spec_int(ens, dflux.T, scale_height, rho, pij=pij, axis=-1)


def fang2013_protons(energy, flux, scale_height, rho, pij=POLY_F2013):
	def _f_y(_cc, _y):
		# Fang et al., 2008, Eq. (6), Fang et al., 2010 Eq. (4)
		# Fang et al., 2013, Eqs. (6), (7)
		_c = _cc.reshape((12, -1))
		return (
			_c[0] * (_y**_c[1]) * np.exp(-_c[2] * (_y**_c[3])) +
			_c[4] * (_y**_c[5]) * np.exp(-_c[6] * (_y**_c[7])) +
		  	_c[8] * (_y**_c[9]) * np.exp(-_c[10] * (_y**_c[11]))
		)
	# Fang et al., 2013, Eqs. (6), (7)
	_cs = np.exp(vpolyval(pij[:, ::-1].T, np.log(energy))).T
	# Fang et al., 2013, Eq. (5)
	y = 7.5 / energy * (1e4 * rho * scale_height)**(0.9)
	f_y = _f_y(_cs, y)
	# Fang et al., 2013, Eq. (3)
	en_diss = f_y * flux / scale_height
	return en_diss