import matplotlib.pyplot as plt

v0 = 0.5
t0 = 0
t_s = [t0]
v_mps = [v0]
deltat = 0.02
t = t0
v = v0
acc = 0

while t_s[-1] < 3:
    acc = (3 * v) ** 2
    v = v - acc * deltat
    t = t + deltat
    t_s += [t]
    v_mps += [v]

plt.plot(t_s, v_mps, '.')
plt.show()
