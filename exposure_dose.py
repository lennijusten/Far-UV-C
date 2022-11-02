# Far UV-C lamp exposure calculations
# Lennart Justen

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Fixed
h_room = 2.46  # m
h_stand = 1.83  # m (assuming 6ft individual)
h_sit = 1.42  # m (assuming 6ft individual)
r_stand = 0.61  # m (assuming 2ft radius from lamp center)
r_sit = 0.61  # m (assuming 2ft radius from lamp center)

# Lamp sepcs at peak irradiance (r=0). See
# https://www.ushio.com/files/specifications/care222-filtered-far-uv-c-excimer-lamp-module-technical-data-sheet.pdf
p_narrow = np.array([14, 6.2, 2.2])  # Ushio Care222 B1 (narrow) specs (mW/cm^2).
p_wide = np.array([1.9, 0.8, 0.3])  # Ushio Care222 B1.5 (wide) specs(mW/cm^2)

# Variable
h = np.array([1, 1.5, 2.5])  # vertical distance from lamp center (m)
r = 0

# For peak irradiation, r=0, so distance from lamp d = h
d = np.sqrt(r ** 2 + h ** 2)


def intensity(d, P):  # d = distance from lamp, P = lamp power
    return P / (4 * np.pi * d ** 2)


# fit curve
P_narrow_fit, _ = curve_fit(intensity, d, p_narrow)
P_wide_fit, _ = curve_fit(intensity, d, p_wide)

dist_plot = np.linspace(0, 2.8, 100)
p_narrow_calc = intensity(dist_plot, P_narrow_fit[0])
p_wide_calc = intensity(dist_plot, P_wide_fit[0])

plt.plot(d, p_narrow, 'o', c='C0')
plt.plot(dist_plot, p_narrow_calc, c='C0', label='Narrow (B1)')

plt.plot(d, p_wide, 'o', c='C1')
plt.plot(dist_plot, p_wide_calc, c='C1', label='Wide (B1.5)')

plt.xlim([0.25, 2.8])
plt.ylim([0, 50])
plt.xlabel('Distance from lamp ($m$)')
plt.ylabel('Irradiance ($\mu W/cm^2$)')
plt.legend()
plt.show()


def exposure_dose(r, h, t, lamp='B1'):
    # r = horizontal distance from lamp center (m)
    # h = vertical distance from lamp center (m)
    # t = time of exposure (in hours)
    # lamp {B1, B.15} where B1 is narrow and B1.5 is wide

    if lamp == 'B1':
        P = 175.76/1000  # Lamp power from fit
    elif lamp == 'B1.5':
        P = 23.67/1000
    else:
        return 'Lamp code is invalid {B1, B1.5}'

    # calculate irradiance
    d = np.sqrt(r**2 + h**2)
    I = intensity(d, P)

    # calculate dose (mJ/cm^2)
    return I * (t*60*60)


# 8h exposure dose for the head of a 6ft tall person standing at peak irradiance in small office under B1 lamp
dose1 = exposure_dose(0, h_room-h_stand, 8, lamp='B1')

# 8h exposure dose for the head of a 6ft tall person sitting at peak irradiance in small office under B1 lamp
dose2 = exposure_dose(0, h_room-h_sit, 8, lamp='B1')

# 8h exposure dose for the head of a 6ft tall person standing in small office under center-ceiling B1 lamp
dose3 = exposure_dose(r_stand, h_room-h_stand, 8, lamp='B1')

# 8h exposure dose for the head of a 6ft tall person sitting in small office under center-ceiling B1 lamp
dose4 = exposure_dose(r_sit, h_room-h_sit, 8, lamp='B1')