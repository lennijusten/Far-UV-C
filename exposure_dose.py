# Far UV-C lamp exposure calculations
# Lennart Justen

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Person dimensions
h_stand = 1.83  # m (assuming 6ft individual)
h_sit = 1.42  # m (assuming 6ft individual)

# Office dimensions
h_office = 2.46  # height of small office room (m)
r_office = 0.61  # distance from vertical lamp axis (m). Varies on room-by-room basis.

# Meeting room dimensions
h_mroom = h_office  # same height as small offices (m)
r_mroom = 1.23  # max distance from center table (m)

# Kitchen
h_kibeam = 2.57  # height of I-beams in the kitchen (m)
h_kceil = 3.05  # height kitchen ceiling (m)
r_ibeam = 2.29  # distance between I-beams (m)

# Lamp sepcs at peak irradiance (r=0). See
# https://www.ushio.com/files/specifications/care222-filtered-far-uv-c-excimer-lamp-module-technical-data-sheet.pdf
p_narrow = np.array([14, 6.2, 2.2])  # Ushio Care222 B1 (narrow) specs (mW/cm^2).
p_wide = np.array([1.9, 0.8, 0.3])  # Ushio Care222 B1.5 (wide) specs(mW/cm^2)

# Fit intensity curve to Ushio irradiance data
h = np.array([1, 1.5, 2.5])  # vertical distance from lamp center (m)
r = 0  # peak irradiance

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


# Exposure calculations

def exposure_dose(r, h, t, lamp='B1'):
    # r = horizontal distance from lamp center (m)
    # h = vertical distance from lamp center (m)
    # t = time of exposure (in hours)
    # lamp {B1, B.15} where B1 is narrow and B1.5 is wide

    if lamp == 'B1':
        P = 175.76 / 1000  # Lamp power from fit
    elif lamp == 'B1.5':
        P = 23.67 / 1000
    else:
        return 'Lamp code is invalid {B1, B1.5}'

    # calculate irradiance
    d = np.sqrt(r ** 2 + h ** 2)
    I = intensity(d, P)

    # calculate dose (mJ/cm^2)
    return I * (t * 60 * 60)


# 8h exposure dose for the head of a 6ft tall person standing at peak irradiance in small office under B1 lamp
dose1 = exposure_dose(0, h_office - h_stand, 8, lamp='B1')

# 8h exposure dose for the head of a 6ft tall person sitting at peak irradiance in small office under B1 lamp
dose2 = exposure_dose(0, h_office - h_sit, 8, lamp='B1')

# 8h exposure dose for the head of a 6ft tall person standing in small office under center-ceiling B1 lamp
dose3 = exposure_dose(r_office, h_office - h_stand, 8, lamp='B1')

# 8h exposure dose for the head of a 6ft tall person sitting in small office under center-ceiling B1 lamp
dose4 = exposure_dose(r_office, h_office - h_sit, 8, lamp='B1')
