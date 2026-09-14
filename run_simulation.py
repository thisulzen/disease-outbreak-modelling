"""
Runs the full simulation pipeline without the Python 3.13 version gate.
Calls the same utilities as simulate_outbreak.py.
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from utils.simulation_utils import setup, build_city, run_risk_solver, run_vaccine_program, run_visualiser

def run(config_path):
    config = setup(config_path)
    city, graph, persons, patient_zero = build_city(config)
    risk_scores, risk_table = run_risk_solver(config, graph, patient_zero, persons)
    eligible = city.get_eligible_residents()
    vaccinated, total_benefit, total_used = run_vaccine_program(config, eligible)
    run_visualiser(config, graph, persons, patient_zero, risk_scores, risk_table, vaccinated, eligible)
    print("Done.")

if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else 'config.json'
    run(path)
