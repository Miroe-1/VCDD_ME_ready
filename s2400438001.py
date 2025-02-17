"""
Student: Miro Eloranta
Student ID: S2400438001

This script calculates braking and side forces based on the Magic Formula.
"""

import argparse  # Command-line argument parsing
import numpy as np  # math calculations
import matplotlib.pyplot as plt  # for graphs
from scipy.constants import g  # gravity (9.81 m/s^2)

# Magic Formula parameters
B_VALUE = 10.5  # stiffness coefficient (range 8-12)
C_VALUE = 1.9   # shape factor (range 1.6-2.2)
D_VALUE = 1.2   # peak power (N) (range 1-1.3)
E_VALUE = 0.97  # curvature coefficient (range 0.85-1)


def compute_vertical_load(vehicle_mass: float) -> float:
    """
    Calculating vertical load (fz) for every wheel

    :param vehicle_mass: vehicle total weight (kg)
    :return: force per wheel (N)
    """
    return (vehicle_mass * g) / 4  # sharing the force to four wheels


def magic_formula(kappa: np.ndarray, B: float, C: float, D: float, E: float) -> np.ndarray:
    """
    Pacejkan Magic Formula model to calculate tire forces.

    :param kappa: longitudinal slip (0-1)
    :param B: stiffness coefficient
    :param C: shape factor
    :param D: peak force
    :param E: curvature coefficient
    :return: calculated forces (N)
    """
    return D * np.sin(C * np.arctan(B * kappa - E * (B * kappa - np.arctan(B * kappa))))


def graph_tire_forces(slip: float, mass: float, friction_values: list):
    """
    Graph is showing tire braking and lateral forces in relation to longitudinal slip.

    :param slip: longitudinal slip (%) (0-100)
    :param mass: vehicle weight (kg)
    :param friction_values: list of friction coefficients (0-1)
    """
    kappa_values = np.linspace(0, slip / 100, 200)  # change percentages to decimals (0-1)
    fz = compute_vertical_load(mass)  # calculate vertical force fz

    plt.figure(figsize=(8, 5))

    # Loop through different friction values to generate multiple curves
    for mu in friction_values:
        forces = magic_formula(kappa_values, B_VALUE, C_VALUE, D_VALUE, E_VALUE) * fz * mu
        plt.plot(kappa_values * 100, forces, label=f"μ={mu}")

    # lets do the graph and I used this website to get reference for the graph:
    # ( https://courses.mooc.fi/org/uh-cs/courses/
    # data-analysis-with-python-2023-2024/chapter-3/matplotlib)
    #COPY
    plt.xlabel("Longitudinal slip (%)")
    plt.ylabel("Force (N)")
    plt.title("Tire braking and lateral forces in relation to longitudinal slip")

    plt.xlim(0, 100)  # X-axis 0-100%
    #END COPY
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.7)  # light extra grid
    plt.savefig("tire_force_plot_multiple.png")
    plt.show()


# Command-line argument parsing
parser = argparse.ArgumentParser(description="Tire force calculation using the Magic Formula")

# Argument definitions
parser.add_argument("slip", type=float, help="Longitudinal slip (0-100%)")
parser.add_argument("weight", type=float, help="Vehicle weight (kg)")

# Parse arguments
args = parser.parse_args()

# Input value check
if not 0 <= args.slip <= 100:
    raise ValueError("Error: Slip must be between 0 and 100%.")
if args.weight <= 0:
    raise ValueError("Error: Vehicle weight must be positive.")

# Define four different friction values for multiple plots
friction_values = [0.2, 0.4, 0.6, 0.8]  # Different friction values (μ)

# Calling function with command-line arguments
graph_tire_forces(args.slip, args.weight, friction_values)

#driving code with command: py s2400438001.py slip weight
