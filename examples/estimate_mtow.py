import numpy as np
import openmdao.api as om

from AVTOL.Weights.Groups import MTOWEstimation

if __name__ == '__main__':

	# --- eVTOL 1: Wingless Multirotor --- #

	pass

	# --- eVTOL 2: Lift+Cruise --- #
	# General parameters
	evtol2_params = {}
	evtol2_params['evtol_config'] 			= 'lift+cruise'
	evtol2_params['N_rotors_lift'] 			= 6
	evtol2_params['N_rotors_cruise'] 		= 1
	evtol2_params['rotor_lift_solidity'] 	= 0.13
	evtol2_params['rotor_cruise_solidity']	= 0.13
	evtol2_params['hover_FM'] 				= 0.75
	# Wing parameters
	# evtol2_params['Cd0'] = 0.0397
	evtol2_params['wing_AR'] 				= 10.0
	# Battery parameters
	evtol2_params['battery_rho'] 			= 280.0 # Wh/kg
	evtol2_params['battery_eff'] 			= 0.85
	evtol2_params['battery_max_discharge'] 	= 0.8
	# Design parameters
	evtol2_weight 			= 1500.0 # kg
	evtol2_r_rotor_lift		= 1.2 # m
	evtol2_r_rotor_cruise 	= 0.9 # m
	evtol2_cruise_speed 	= 55.0 # m/s
	evtol2_wing_area 		= 6.4 # m**2
	evtol2_rotor_J 			= 1.0

	# Conditions
	evtol2_params['AoA_cruise']				= 5.0 # deg
	evtol2_params['rho_air'] 				= 1.225 # kg/m**3
	evtol2_params['gravitational_accel'] 	= 9.81 # kg/m**3

	# --- Mission requirements --- #
	n_missions		= 1
	flight_ranges 	= [5000.0] # m
	hover_times 	= [240.0] # s

	# --- MTOW Estimation for Wingless Multirotor --- #
	pass

	# --- MTOW Estimation for Lift+Cruise --- #
	mtow_list2 = np.zeros(n_missions)

	for i in range(n_missions):
		prob = om.Problem()
		indeps = prob.model.add_subsystem('indeps', om.IndepVarComp(), promotes=['*'])
		indeps.add_output('flight_distance', flight_ranges[i], units='m')
		indeps.add_output('hover_time', hover_times[i], units='s')
		indeps.add_output('eVTOL|W_takeoff', evtol2_weight, units='kg')
		indeps.add_output('eVTOL|Cruise_speed', evtol2_cruise_speed, units='m/s')
		indeps.add_output('Rotor|radius_lift', evtol2_r_rotor_lift, units='m')
		indeps.add_output('Rotor|radius_cruise', evtol2_r_rotor_cruise, units='m')
		indeps.add_output('eVTOL|S_wing', evtol2_wing_area, units='m**2')
		indeps.add_output('Rotor|J', evtol2_rotor_J)
		
		prob.model.add_subsystem('mtow_estimation',
								  MTOWEstimation(evtol_options=evtol2_params, use_solver=False),
								  promotes_inputs=['*'],
								  promotes_outputs=['*'])

		prob.setup(check=False)
		prob.run_model()

	print(f'energy_cnsmp =', prob.get_val('energy_cnsmp', 'W*h'))
	print(f'W_battery =', prob.get_val('Weights|Battery'))
	print(f'W_Rotors =', prob.get_val('Weights|Rotors'))
	print(f'W_motors =', prob.get_val('Weights|Motors'))
















		