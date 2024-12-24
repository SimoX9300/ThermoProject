import numpy as np
import matplotlib.pyplot as plt

# Known parameters for Phase A
m_w = 0.1  # Mass of water in kg (example value)
cp = 4186  # Specific heat capacity of water in J/(kg°C)
cv = 4186  # Specific heat capacity at constant volume in J/(kg°C)
delta_T = 50  # Temperature change in °C (example value)
mevap = 0.01  # Mass of water evaporated in kg (example value)
h_fg = 2260e3  # Latent heat of vaporization in J/kg

# Phase A coefficients (using the exponential model from your best fit)
a_a = 100  # Coefficient for Phase A model (replace with actual value)
b_a = 0.1  # Coefficient for Phase A model (replace with actual value)

# Time range for Phase A (you can adjust the time range based on your experiment)
time_a = np.linspace(0, 10, 100)  # Time range in seconds

# Phase A pressure model using the exponential equation
def exponential_model(t, a, b):
    return a * np.exp(b * t)

# Calculate pressure for Phase A using the exponential model
pressure_a = exponential_model(time_a, a_a, b_a)

# Heat input calculation (Q = Q1 + Q2)
Q1 = m_w * cp * delta_T  # Sensible heat (Q1)
Q2 = mevap * h_fg  # Latent heat (Q2)
Q = Q1 + Q2  # Total heat added

# Change in internal energy (Delta U = m_w * c_v * delta_T)
delta_U = m_w * cv * delta_T

# Print results for Phase A
print(f"Phase A - Total heat input (Q): {Q:.2f} J")
print(f"Phase A - Change in internal energy (Delta U): {delta_U:.2f} J")
print(f"Phase A - Pressure at final time {time_a[-1]}s: {pressure_a[-1]:.2f} Pa")

# Plot Pressure vs Time for Phase A
plt.figure(figsize=(8, 6))
plt.plot(time_a, pressure_a, label=f'Phase A: P(t) = {a_a} * exp({b_a} * t)')
plt.xlabel('Time (s)')
plt.ylabel('Pressure (Pa)')
plt.title('Phase A: Pressure vs Time (Heat Input and Pressure Buildup)')
plt.legend(loc='upper left')
plt.grid(True)

# Annotate R² value (for this example, using a best fit model R²)
R2_value = 0.9506  # Replace with the actual R² from your regression analysis
plt.text(0.5, 0.9, f'R² = {R2_value:.4f}', transform=plt.gca().transAxes, fontsize=12, verticalalignment='top')

plt.show()
