import numpy as np

V = 240  # m^3
S = 10 #m^2
c = 343  #m/s

#Calculate K
K = (24 * V * np.log(10))/(c * S)

#Defining reverberation times
T_60_uten = [4.28, 4.28, 4.13, 3.76, 4.14, 4.33, 4.10, 4.21]
T_60_med = [3.14, 3.15, 3.92, 3.65, 3.35, 3.89, 3.79, 3.32]

#Calculate means
mean_uten = np.mean(T_60_uten)
mean_med = np.mean(T_60_med)

#Calculate standard deviations
std_uten = np.std(T_60_uten)
std_med = np.std(T_60_med)

#Calculate absorption coefficient
alpha = K * (1/mean_med - 1/mean_uten)

#Calculate standard deviation of alpha
std_aplha = K * np.sqrt((std_med**2/mean_med**4) + (std_uten**2/mean_uten**4))

#Print results
print(f"Absorpsjonskoeffisient: {alpha:.4f} ± {std_aplha:.4f}")
