import numpy as np

N = int(1e4)

tau_error = 0.01
d_error = 0.02

c0 = 1 #m/s
d0 = 1 #meters

theta_arr = np.deg2rad([0, 30, 60, 90, 120, 150, 180])

results = []

for theta in theta_arr:
    f0 = np.cos(theta) #Hz
    tau0 = d0 * f0 / c0 #seconds

    scale_tau = (1 + 2 * tau_error * (np.random.rand(N) - 0.5))
    scale_d = (1 + 2 * d_error * (np.random.rand(N) - 0.5))

    vector_tau = tau0 * scale_tau
    vector_d = d0 * scale_d
    vector_f = c0 * vector_tau / vector_d

    is_valid_fvec = np.abs(vector_f) <= 1.0
    vector_f_valid = vector_f[is_valid_fvec]

    vector_theta = np.arccos(vector_f_valid)

    rel_error_theta = (vector_theta - theta) / theta
    max_rel_error_theta = np.max(np.abs(rel_error_theta))

    results.append((theta, max_rel_error_theta, is_valid_fvec.mean()))

for theta, max_rel_err, valid_frac in results:
    print(f"Theta: {np.rad2deg(theta):6.1f} deg | Maks relativ feil i vinkelestimatet: {max_rel_err * 100:.2f} % | Gyldige estimater: {valid_frac * 100:.2f} %")


