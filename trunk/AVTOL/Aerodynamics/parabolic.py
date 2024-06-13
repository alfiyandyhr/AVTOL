import numpy as np
import openmdao.api as om

class WingedCruiseDrag(om.ExplicitComponent):
	"""
	Computes the drag of a winged configuration in cruise.
	Parameters:
		Cd0		: minimum Cd of the polar drag (coefficient of parasitic drag)
		rho_air	: air density [kg/m**3]
		wing_AR	: wing aspect ratio
	Inputs:
		Aero|Lift
		eVTOL|S_wing
		eVTOL|Speed
	Outputs:
		Aero|Drag
		Aero|CL_cruise
	Notes:
		> Based on a simple parabolic drag polar equations
		> Oswald efficiency is in the function of wing aspect ratio (typically ~0.8)
		> The wing should be un-swept.
	Source:

	"""
	def initialize(self):
		self.options.declare('rho_air', default=1.225, desc='Air density')
		self.options.declare('Cd0', types=float, desc='Minimum Cd of the polar drag')
		self.options.declare('wing_AR', types=float, desc='Wing aspect ratio')

	def setup(self):
		self.add_input('Aero|Lift', units='N', desc='Lift generated by the wing')
		self.add_input('eVTOL|Speed', units='m/s', desc='Cruise speed')
		self.add_input('eVTOL|S_wing', units='m**2', desc='Wing reference area')
		self.add_output('Aero|Drag', units='N', desc='Drag of a winged configuration')
		self.add_output('Aero|CL_cruise', desc='Lift coefficient')
		self.declare_partials('*', '*')

	def compute(self, inputs, outputs):
		rho_air = self.options['rho_air']
		CD0 = self.options['Cd0']
		wing_AR = self.options['wing_AR']
		L = inputs['Aero|Lift']
		v = inputs['eVTOL|Speed']
		S_wing = inputs['eVTOL|S_wing']

		# Raymer's formula for non-swept wing (Oswald efficiency)
		wing_e = 1.78 * (1 - 0.045 * wing_AR^0.68) - 0.64

		q = 0.5 * rho_air * v**2 	 					# dynamic pressure
		CL = L/(q * S_wing)								# lift coefficient
		CD = CD0 + CL**2 / (np.pi * wing_e * wing_AR)	# drag coefficient
		outputs['Aero|Drag'] = q * S_wing * CD			# drag
		outputs['Aero|CL_cruise'] = CL

	def compute_partials(self, inputs, partials):
		rho_air = self.options['rho_air']
		CD0 = self.options['Cd0']
		wing_AR = self.options['wing_AR']
		L = inputs['Aero|Lift']
		v = inputs['eVTOL|Speed']
		S_wing = inputs['eVTOL|S_wing']

		# Raymer's formula for non-swept wing (Oswald efficiency)
		wing_e = 1.78 * (1 - 0.045 * wing_AR^0.68) - 0.64

		q = 0.5 * rho_air * v**2 	 					# dynamic pressure
		CL = L/(q * S_wing)								# lift coefficient
		dq_dv = rho_air * v
		dCL_dL = 1/(q * S_wing)
		dCL_dq = -L/(S_wing * q**2)
		dCL_dS = -L/(q * S_wing**2)
		
		CD = CD0 + CL**2 / (np.pi * wing_e * wing_AR)	# drag coefficient
		dCD_dCL = 2*CL / (np.pi * wing_e * wing_AR)
		dD_dq = S_wing * CD
		dD_dS = q * CD
		dD_dCD = q * S_wing

		partials['Aero|Drag', 'Aero|Lift'] = dD_dCD * dCD_dCL * dCL_dL
		partials['Aero|Drag', 'eVTOL|S_wing'] = dD_dS + dD_dCD * dCD_dCL * dCL_dS
		partials['Aero|Drag', 'eVTOL|Speed'] = (dD_dCD*dCD_dCL*dCL_dq + dD_dq) * dq_dv
		partials['Aero|CL_cruise', 'Aero|Lift'] = dCL_dL
		partials['Aero|CL_cruise', 'eVTOL|S_wing'] = dCL_dS
		partials['Aero|CL_cruise', 'eVTOL|Speed'] = dCL_dq * dq_dv