import numpy as np
import openmdao.api as om

class FurnishingWeight(om.ExplicitComponent):
	"""
	Computes furninshing and equipment weight
	Inputs:
		eVTOL|W_takeoff : total take-off weight [kg]
	Outputs:
		Weights|Furnishings : weight of all furnishings and equipment [kg]
	Notes:
		> Value for coefficient K
			low_estimate	: 6.0
			avg_estimate	: 13.0
			high_estimate	: 23.0
	Source:
		Prouty, R. W., Helicopter Performance, Stability, and Control, Krieger, 2002.
	"""
	def setup(self):
		self.add_input('eVTOL|W_takeoff', units='kg', desc='Total take-off weight')
		self.add_output('Weights|Furnishings', units='kg', desc='Weight of all furnishings')
		self.declare_partials('Weights|Furnishings', 'eVTOL|W_takeoff')

	def compute(self, inputs, outputs):
		W_takeoff = inputs['eVTOL|W_takeoff'] # in [kg]

		# Calculating W_furnishings
		kg_to_lb = 2.20462**1.3
		lb_to_kg = 0.453592

		K_low = 6.0
		K_avg = 13.0
		K_high = 23.0

		W_furnishings = K_avg * (W_takeoff/1000.0)**1.3 * kg_to_lb * lb_to_kg

		outputs['Weights|Furnishings'] = W_furnishings # in [kg]

	def compute_partials(self, inputs, partials):
		W_takeoff = inputs['eVTOL|W_takeoff'] # in [kg]

		# Calculating dWfurn_dWtakeoff
		kg_to_lb = 2.20462**1.3
		lb_to_kg = 0.453592

		K_low = 6.0
		K_avg = 13.0
		K_high = 23.0

		dWfurn_dWtakeoff = K_avg * 1.3 * W_takeoff**0.3 * (1/1000.0)**1.3 * kg_to_lb * lb_to_kg
		partials['Weights|Furnishings', 'eVTOL|W_takeoff'] = dWfurn_dWtakeoff
