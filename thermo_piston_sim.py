import numpy as np
import matplotlib.pyplot as plt
from vpython import canvas, box, cylinder, vector, rate

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

# Simulate Phase 2: Piston movement and work done
def simulate_phase2(P_phase1, time_steps):
    h = np.zeros(time_steps)
    W = np.zeros(time_steps)
    P = np.zeros(time_steps)
    for t in range(1, time_steps):
        P[t] = P_phase1[-1] + mpiston * g / A
        h[t] = h[t - 1] + (P[t] * A / (mpiston * g)) * (1 / time_steps)
        W[t] = W[t - 1] + P[t] * A * h[t]
    return P, h, W

# Plot simulation results
def plot_results(time, Q, T, P1, P2, h, W):
    plt.figure(figsize=(12, 8))
    # Heat and temperature
    plt.subplot(2, 2, 1)
    plt.plot(time, Q, label="Heat Input Q (kJ)")
    plt.plot(time, T, label="Temperature T (C)")
    plt.xlabel("Time (s)")
    plt.ylabel("Value")
    plt.title("Heat and Temperature")
    plt.legend()

    # Pressure Phase 1
    plt.subplot(2, 2, 2)
    plt.plot(time, P1, label="Pressure Phase 1 P (kPa)")
    plt.xlabel("Time (s)")
    plt.ylabel("Pressure (kPa)")
    plt.title("Pressure Buildup in Phase 1")
    plt.legend()

    # Piston movement
    plt.subplot(2, 2, 3)
    plt.plot(time, h, label="Piston Displacement h (m)")
    plt.xlabel("Time (s)")
    plt.ylabel("Height (m)")
    plt.title("Piston Movement in Phase 2")
    plt.legend()

    # Work done
    plt.subplot(2, 2, 4)
    plt.plot(time, W, label="Work Done W (kJ)")
    plt.xlabel("Time (s)")
    plt.ylabel("Work (kJ)")
    plt.title("Work Done in Phase 2")
    plt.legend()

    plt.tight_layout()
    plt.show()

# Simulate the piston-cylinder system using VPython
def vpython_simulation(h, time_steps):
    # VPython setup
    scene = canvas(title="Piston-Cylinder System", width=800, height=600)
    cylinder_body = cylinder(pos=vector(0, 0, 0), axis=vector(0, 0.2, 0), radius=0.05, color=vector(0.6, 0.6, 0.6))
    piston = box(pos=vector(0, 0.1, 0), size=vector(0.1, 0.02, 0.1), color=vector(0.8, 0.2, 0.2))

    # Animate piston movement
    for t in range(time_steps):
        rate(100)  # Control animation speed
        piston.pos.y = 0.1 + h[t]  # Update piston position

# Simulation setup
time_steps = 1000  # Ensure total simulation time is correctly divided into phases
time = np.linspace(0, time_total, time_steps)

# Phase 1 simulation
Q, T, P_phase1 = simulate_phase1(time_steps)

# Phase 2 simulation
P_phase2, h, W = simulate_phase2(P_phase1, time_steps)

# Plot results
plot_results(time, Q, T, P_phase1, P_phase2, h, W)

# VPython simulation
vpython_simulation(h, time_steps)
