﻿import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Constants
cp = 4.18  # Specific heat capacity of water at constant pressure (kJ/kg*K)
cv = 2.09  # Specific heat capacity of water at constant volume (kJ/kg*K)
hfg = 2257  # Latent heat of vaporization of water (kJ/kg)
g = 9.81  # Acceleration due to gravity (m/s^2)
Patm = 101.325  # Atmospheric pressure (kPa)
mw = 0.1  # Mass of water (kg)
mevap = 0.01  # Mass of water evaporated (kg)
A = 0.01  # Cross-sectional area of piston (m^2)
mpiston = 1.0  # Mass of piston (kg)
heat_rate = 10  # Heat input rate (kJ/s)
time_total = 10  # Total simulation time (s)

# Simulate Phase 1: Heat input and pressure buildup
def simulate_phase1(time_steps):
    Q = np.zeros(time_steps)
    T = np.zeros(time_steps)
    P = np.zeros(time_steps)
    for t in range(1, time_steps):
        Q[t] = Q[t - 1] + heat_rate * (1 / time_steps)
        T[t] = Q[t] / (mw * cp)
        P[t] = Patm + (Q[t] / (mw * cv))
    return Q, T, P

# Function to compute R² value
def compute_r_squared(x, y, model, params):
    y_pred = model(x, *params)
    ss_total = np.sum((y - np.mean(y))**2)
    ss_residual = np.sum((y - y_pred)**2)
    r_squared = 1 - (ss_residual / ss_total)
    return r_squared

# Define models for fitting
def linear(x, a, b):
    return a * x + b

def quadratic(x, a, b, c):
    return a * x**2 + b * x + c

def exponential(x, a, b, c):
    return a * np.exp(b * x) + c

# Fit models to the pressure data
def fit_models(time, P_phase1):
    # Linear fit
    popt_linear, _ = curve_fit(linear, time, P_phase1)
    r2_linear = compute_r_squared(time, P_phase1, linear, popt_linear)

    # Quadratic fit
    popt_quadratic, _ = curve_fit(quadratic, time, P_phase1)
    r2_quadratic = compute_r_squared(time, P_phase1, quadratic, popt_quadratic)

    # Exponential fit
    popt_exponential, _ = curve_fit(exponential, time, P_phase1, p0=[1, 0.1, 1])
    r2_exponential = compute_r_squared(time, P_phase1, exponential, popt_exponential)

    # Select the best model based on R²
    best_model = "Linear" if r2_linear > max(r2_quadratic, r2_exponential) else \
                 "Quadratic" if r2_quadratic > r2_exponential else "Exponential"
    
    return popt_linear, r2_linear, popt_quadratic, r2_quadratic, popt_exponential, r2_exponential, best_model

# Plot the pressure data and fitted models
def plot_fitted_models(time, P_phase1, popt_linear, r2_linear, popt_quadratic, r2_quadratic, popt_exponential, r2_exponential, best_model):
    plt.figure(figsize=(10, 6))
    plt.plot(time, P_phase1, label="Pressure Data (Phase 1)", color='black', marker='o', linestyle='None')

    # Plot linear fit
    plt.plot(time, linear(time, *popt_linear), label="Linear Fit", color='red')

    # Plot quadratic fit
    plt.plot(time, quadratic(time, *popt_quadratic), label="Quadratic Fit", color='blue')

    # Plot exponential fit
    plt.plot(time, exponential(time, *popt_exponential), label="Exponential Fit", color='green')

    # Add R² values and best model text in the upper-right corner
    plt.text(0.95, 0.95, f"R² (Linear): {r2_linear:.4f}", color='red', fontsize=12, ha='right', va='top', transform=plt.gca().transAxes)
    plt.text(0.95, 0.90, f"R² (Quadratic): {r2_quadratic:.4f}", color='blue', fontsize=12, ha='right', va='top', transform=plt.gca().transAxes)
    plt.text(0.95, 0.85, f"R² (Exponential): {r2_exponential:.4f}", color='green', fontsize=12, ha='right', va='top', transform=plt.gca().transAxes)
    plt.text(0.95, 0.80, f"Best Fitting Model: {best_model}", color='black', fontsize=14, ha='right', va='top', weight='bold', transform=plt.gca().transAxes)

    plt.xlabel("Time (s)")
    plt.ylabel("Pressure (kPa)")
    plt.title("Pressure vs Time with Fitted Models and R² Values")
    plt.legend()
    plt.tight_layout()
    plt.show()

# Simulation setup
time_steps = 1000  # Ensure total simulation time is correctly divided into phases
time = np.linspace(0, time_total, time_steps)

# Phase 1 simulation (using your given simulation data)
Q, T, P_phase1 = simulate_phase1(time_steps)

# Fit models to Phase 1 pressure data
popt_linear, r2_linear, popt_quadratic, r2_quadratic, popt_exponential, r2_exponential, best_model = fit_models(time, P_phase1)

# Plot the data and fitted models with R² values and the best model
plot_fitted_models(time, P_phase1, popt_linear, r2_linear, popt_quadratic, r2_quadratic, popt_exponential, r2_exponential, best_model)
