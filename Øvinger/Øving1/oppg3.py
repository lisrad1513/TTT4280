import numpy as np

#Oppgave 3
#Oppgave 3 a) Maks, min og standardavvik på R
R = 1000
R_plus = R * 1.01
R_min = R * 0.99
R_std = np.std([R_min, R_plus])


print(f"Oppgave 3, deloppgave a)")
print(f"Maks verdi R: {round(R_plus, 3)} Ω")
print(f"Minuns verdi R: {round(R_min, 3)} Ω")
print(f"Standardavvik R: {round(R_std, 3)} Ω")
print(f"\n")

#Oppgave 3 b) Relativt standardavvik
s_R = (R_plus - R_min)/np.sqrt(12) #Standardavvik for uniform fordeling
m_R = R
RS = s_R / m_R
print(f"Oppgave 3, deloppgave b)")
print(f"Relativ standardavvik: {round(RS * 100, 2)}%")
print(f"\n")

#Oppgave 3 d) Standaravvik
delta_r = 10
r_values = 1000 + 2*delta_r * (np.random.rand(100000) - 0.5)
relative_std = np.std(r_values, ddof=1)/np.mean(r_values)

print(f"Oppgave 3, deloppgave d)")
print(f"Relativ standardavvik: {round(relative_std * 100, 2)}%")

