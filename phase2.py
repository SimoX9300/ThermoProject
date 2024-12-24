import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import trapz  # for numerical integration

# Example data (replace with your actual data)
time = np.array([0, 1, 2, 3, 4, 5])  # Time in seconds
area = 0.01  # Cross-sectional area of the piston (m^2)

# Assumed exponential model parameters for pressure (you should replace these with your actual parameters)
a = 100  # Initial pressure (Pa)
b = 0.1  # Rate constant (s^-1)

# Exponential pressure model: P(t) = a * exp(b * time)
pressure = a * np.exp(b * time)

# Assumed piston movement over time (in meters) for each time step, depending on pressure (this can be adjusted as per your setup)
height_change = np.array([0.02, 0.03, 0.04, 0.05, 0.06, 0.07])  # Example piston movement in meters for each time step

# Ensure the time and height arrays are of compatible sizes for the integration
# Using the first n-1 values to match the length of the integration
work = trapz(pressure[:-1] * area * height_change[:-1], time[:-1])  # Integrating over time

# Plotting exponential pressure vs. time for visual inspection
plt.figure(figsize=(10, 6))
plt.plot(time, pressure, label=f'Exponential Model: P(t) = {a} * exp({b} * t)', color="blue")
plt.xlabel("Time (s)")
plt.ylabel("Pressure (Pa)")
plt.title("Pressure vs. Time during Phase 2 (Exponential Model)")
plt.legend()
plt.grid(True)
plt.show()

# Print the total work done by the system
print(f"Total work done by the system: {work:.2f} J")
