import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.colors
from mpl_toolkits.mplot3d.axes3d import Axes3D
import numpy as np

# Power specs from fit in exposure_dose.py
P_narrow = 175.76
P_wide = 23.67

# Person dimensions
z_stand = 1.83  # m (assuming 6ft individual)
z_sit_office = 1.42  # m (assuming 6ft individual). Varies by chair setting.

# Office dimensions
z_office = 2.46  # height of small office room (m)
x_office = 0.61  # distance from vertical lamp axis (m). Varies on room-by-room basis.

# origin is at upper left hand corner of the room such that lamp is at z = 0
xaxis = np.linspace(-1, 1, 100)
yaxis = np.linspace(-1, 1, 100)
zaxis = np.linspace(0, 2.5, 100)


def intensity(x, y, z, P):  # d = distance from lamp, P = lamp power
    d = np.sqrt(x**2 + y**2 + z**2)
    return P / (4 * np.pi * d ** 2)


I = intensity(xaxis[:,None,None], yaxis[None,:,None],zaxis[None,None,:], P_narrow)

def exposure_dose(x, y, z, t=8, lamp='B1'):
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

    I = intensity(x, y, z, P)

    # calculate dose (mJ/cm^2)
    return I * (t * 60 * 60)


dose = exposure_dose(xaxis[:,None,None], yaxis[None,:,None],zaxis[None,None,:])


def euclidean_exposure(xaxis, yaxis, z, max_height=z_office, t=8, lamp = 'B1'):
    X, Y = np.meshgrid(xaxis, yaxis)

    fig = plt.figure(figsize=(15,25))
    ax = fig.add_subplot(111, projection='3d')
    fig.subplots_adjust(bottom=-0.05, top=1.05)

    norm = matplotlib.colors.Normalize(vmin=0, vmax=1000)

    for level in z:
        dose = exposure_dose(xaxis[:,None,None], yaxis[None,:,None], max_height-level, t, lamp)

        ax.plot_surface(X, Y, level * np.ones(X.shape), facecolors=plt.cm.inferno_r(norm(dose)))

    m = cm.ScalarMappable(cmap=plt.cm.inferno_r, norm=norm)
    m.set_array([])
    # ax.set_xlabel('X (m)')
    # ax.set_ylabel('Y (m)')
    # ax.set_zlabel('Z (m)')

    ax.tick_params(labelsize=30, pad=20)
    ax.set_xticks([])
    ax.set_yticks([1.0, 0.5, 0, -0.5, -1], ['0.0', '0.5', '1.0', '1.5', '2.0'])

    ax.set_box_aspect(aspect=(2.5, 2.5, 4))
    ax.set_zlim3d([0, 2.5])
    plt.savefig('3D_exposure.png', dpi=300)
    plt.show()

    _, ax1 = plt.subplots()
    plt.colorbar(m, ax=ax1)
    # Hide grid lines
    ax1.grid(False)
    # Hide axes ticks
    ax1.set_xticks([])
    ax1.set_yticks([])
    plt.savefig('colorbar.png', dpi=300)
    plt.show()


euclidean_exposure(xaxis, yaxis, [z_stand, z_sit_office, 0])
# euclidean_exposure(xaxis, yaxis, [z_stand, z_sit_office])


