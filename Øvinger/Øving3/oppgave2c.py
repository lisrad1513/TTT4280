import numpy as np

N = int(1e4)

c = 343  # m/s
tau0 = 1.0 # seconds
d0 = 1.0  # meters
f0 = c * tau0 / d0 # Hz

tau_error = 0.01
d_error = 0.02

scale_tau = (1 + 2 * tau_error * (np.random.rand(N) - 0.5))
scale_d = (1 + 2 * d_error * (np.random.rand(N) - 0.5))

vector_tau = tau0 * scale_tau
vector_d = d0 * scale_d
vector_f = c * vector_tau / vector_d

rel_error = (vector_f - f0) / f0
max_rel_error = np.max(np.abs(rel_error))

print(f"Maks relativ feil i frekvensestimatet: {max_rel_error * 100:.2f} %")
print(f"Teoretisk relativ feil: {(tau_error + d_error) * 100:.2f} %")

