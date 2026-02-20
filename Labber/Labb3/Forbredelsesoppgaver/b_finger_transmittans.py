import numpy as np

def finnC():
    muabo = np.genfromtxt("ELSYSS6/Sensor/Labber/Labb3/Optikk-lab-filer-26/muabo.txt", delimiter=",")
    muabd = np.genfromtxt("ELSYSS6/Sensor/Labber/Labb3/Optikk-lab-filer-26/muabd.txt", delimiter=",")

    red_wavelength = 600 # Replace with wavelength in nanometres
    green_wavelength = 520 # Replace with wavelength in nanometres
    blue_wavelength = 460 # Replace with wavelength in nanometres

    wavelength = np.array([red_wavelength, green_wavelength, blue_wavelength])

    def mua_blood_oxy(x): return np.interp(x, muabo[:, 0], muabo[:, 1])
    def mua_blood_deoxy(x): return np.interp(x, muabd[:, 0], muabd[:, 1])

    bvf = 0.01 # Blood volume fraction, average blood amount in tissue
    oxy = 0.8 # Blood oxygenation

    # Absorption coefficient ($\mu_a$ in lab text)
    # Units: 1/m
    mua_other = 25 # Background absorption due to collagen, et cetera
    mua_blood = (mua_blood_oxy(wavelength)*oxy # Absorption due to
                + mua_blood_deoxy(wavelength)*(1-oxy)) # pure blood
    mua = mua_blood*bvf + mua_other

    # reduced scattering coefficient ($\mu_s^\prime$ in lab text)
    # the numerical constants are thanks to N. Bashkatov, E. A. Genina and
    # V. V. Tuchin. Optical properties of skin, subcutaneous and muscle
    # tissues: A review. In: J. Innov. Opt. Health Sci., 4(1):9-38, 2011.
    # Units: 1/m
    musr = 100 * (17.6*(wavelength/500)**-4 + 18.78*(wavelength/500)**-0.22)

    # mua and musr are now available as shape (3,) arrays
    # Red, green and blue correspond to indexes 0, 1 and 2, respectively

    C = np.sqrt(3*(musr+mua)*mua)

    return C


fingerLisa = 7 # mm, målt med skyvelære
fingerEven = 14.3 # mm, målt med skyvelære

C = finnC()

T_lisa = np.exp(-C * fingerLisa * 1e-3) # Convert mm to m
T_even = np.exp(-C * fingerEven * 1e-3) # Convert mm to m

print(f"Transmittance for Lisa's finger ({fingerLisa} mm):")
print(f"\t Red light: {T_lisa[0]:.2e}")
print(f"\t Green light: {T_lisa[1]:.2e}")
print(f"\t Blue light: {T_lisa[2]:.2e}")
print(f"Transmittance for Even's finger ({fingerEven} mm):")
print(f"\t Red light: {T_even[0]:.2e}")
print(f"\t Green light: {T_even[1]:.2e}")
print(f"\t Blue light: {T_even[2]:.2e}")