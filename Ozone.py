import matplotlib.pyplot as plt
import numpy as np

# Lamp specs
P = 12  # lamp power (W)
wl = 222 * 10**-9 # wavelength (m)

# Room dimensions
height = 2.5  # m
width1 = 3  # m
width2 = 4  # m

area = width1*width2  # m2
vol = width1*width2*height  # m3

# Inputs
f1 = 1.12 * 10 ** 19  # flux at 1 mW/m2 (units = photons m-2 s-1) | from Jose email
I = 0.0713  # Irradiation at 1.3m above the floor, 0m from the center of the beam:(W m-2)


def approx_irradiation(P, area):
    # Returns average irradiation per unit area (W m-2)
    return P/area

# I = approx_irradiation(P, area)

def flux(I, wl):
    # Returns photon flux per unit area (m-2 s-1)
    h = 6.626*10**-34  # Plank's constant (m2 kg s-1)
    c =2.998*10**8  # speed of light (m s-1)
    return (I*wl)/(h*c)

f2 = flux(I,wl)

def do3_dt(flux):
    # Returns O3 generation per second (molecule m-3 s-1)
    # flux = photon flux (m-3 s-1)
    sigma_o2 = 4.2 * 10 ** -28  # O2 absorption cross-section at 222 nm and room temp (m2/molec)
    Co2 = 5.016 * 10 ** 24  # concentration of O2 in the air (molec/m3)
    return 2 * flux * Co2 * sigma_o2


def ppb_dt(do3_dt):
    # Returns ppb of ozone generation per second (ppb/s)
    # Assumptions: 1 atm, 298 K, and constant O2 concentration (do2/dt=0)
    ppb_conversion_factor = 1/(2.46*10**16)  # m3/molecule
    return ppb_conversion_factor*do3_dt


print('ppb/s at 1 mW/cm2 = {}'.format(round(ppb_dt(do3_dt(f1)), 3)))
print('ppb/s with 12 W ({} mW/cm2) lamp = {}'.format(P/area/10, round(ppb_dt(do3_dt(f2)), 3)))

# Plotting ---------------------------------------------------

t = np.linspace(0,4*60, 100)  # time in seconds for plotting
O3_concentration1 = np.array([ppb_dt(do3_dt(f1))*i*60 for i in t])
O3_concentration2 = np.array([ppb_dt(do3_dt(f2))*i*60 for i in t])


# plt.plot(t, O3_concentration1, label='No ventilation (1 mW/cm^2)')
plt.plot(t, O3_concentration2, label='No ventilation (7.13 μW/cm^2)')
plt.plot(t, [70]*len(t), c='#9d9d9d', linestyle='--', label='EPA limit')
plt.xlabel('Time (min)')
plt.ylabel('Ozone concentration (ppb)')
plt.legend()
plt.show()
