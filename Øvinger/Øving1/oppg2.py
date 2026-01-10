import numpy as np

#Oppgave 2
maalinger = [20.4, 20.4, 20.4, 20.2, 20.4, 20.3, 20.4, 20.5, 20.4, 20.4, 20.4, 20.4, 20.1, 20.3, 20.3, 20.2, 20.3, 20.2, 20.3, 20.3]
n = len(maalinger)

#Oppgave 2
#Oppgave 2 a) 95% konfidensintervall
x_bar = np.mean(maalinger)
z = 1.96 #95%
s = np.std(maalinger)

CI_plus = x_bar + (z * (s / np.sqrt(n)))
CI_minus = x_bar - (z * (s / np.sqrt(n)))

print(f"95% konfidensintervall med 20 målinger: [{round(CI_minus, 3)}, {round(CI_plus, 3)}]")

#Oppgave 2 c)
maalinger_ti = maalinger[0:10]
n_ti = len(maalinger_ti)

x_bar_ti = np.mean(maalinger_ti)
z_ti = 1.96 #95%
s_ti = np.std(maalinger)

CI_plus_ti = x_bar_ti + (z_ti * (s_ti / np.sqrt(n_ti)))
CI_minus_ti = x_bar_ti - (z_ti * (s_ti / np.sqrt(n_ti)))

print(f"95% konfidensintervall med 10 målinger: [{round(CI_minus_ti, 3)}, {round(CI_plus_ti, 3)}]")

