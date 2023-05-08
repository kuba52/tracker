from matplotlib import pyplot as plt
import numpy as np

# from decimal import Decimal as D

# Wczytywanie danych
f = open("data.txt", 'r')
data = f.readlines()

x = np.empty(len(data), dtype=float) # położenia w osi x
y = np.empty(len(data), dtype=float) # położenia w osi y
time = np.empty(len(data), dtype=float)

for i in range(0, len(data)):
    s = data[i]
    coordinates = s.split() # x y t
    x[i] = float(coordinates[0])
    y[i] = float(coordinates[1])
    time[i] = float(coordinates[2])
f.close()


#x = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], dtype = float)
#y = np.array([0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5], dtype = float) 

#time_step = 0.05 

#time = np.linspace(start = 0, stop = time_step * x.size, num = x.size, endpoint = False)


# min and max values in an array may differ by less than ER and still will be considered constant
ER = 0.0001
# kalkulacja prędkości
v_x = np.arange(x.size - 1, dtype=float)
v_y = np.arange(y.size - 1, dtype=float)
v = np.arange(x.size - 1, dtype=float)
 

for i in range(0, v_x.size):
    time_step = time[i + 1] - time[i]
    v_x[i] = (x[i + 1] - x[i])/time_step
    
    
for i in range(0, v_y.size):
    time_step = time[i + 1] - time[i]
    v_y[i] = (y[i + 1] - y[i])/time_step

for i in range(0, v.size):
    v[i] = np.sqrt(v_x[i]**2 + v_y[i]**2)
    
# Czy prędkości są stałe

vx_const = np.max(v_x) - np.min(v_x) < ER
vy_const = np.max(v_y) - np.min(v_y) < ER

# kalkulacja przyspieszeń

a_x = np.arange(v_x.size - 1, dtype=float)
a_y = np.arange(v_y.size - 1, dtype=float)
a = np.arange(v.size - 1, dtype=float)

for i in range(0, a.size):
    time_step = time[i + 2] - time[i + 1]
    a_x[i] = (v_x[i+1] - v_x[i])/time_step
    a_y[i] = (v_y[i+1] - v_y[i])/time_step
    a[i] = (v[i+1] - v_x[i])/time_step
 
# Czy przyspieszenia są stałe
ax_const = np.max(a_x) - np.min(a_x) < ER
ay_const = np.max(a_y) - np.min(a_y) < ER
a_const = np.max(a) - np.min(a) < ER




# Rysowanie wykresu x(t)

fig = plt.figure("x[t]", layout="constrained")
plt.title('Wykres położenia (oś x) od czasu')
plt.plot(time, x,'go', markersize = '5')
plt.xlabel("t [s]")
plt.ylabel("x [m]")
plt.grid(True)
plt.legend()
plt.savefig("x(t).pdf")

# Rysowanie wykresu y(t)

fig = plt.figure("y[t]", layout="constrained")
plt.title('Wykres położenia (oś y) od czasu')
plt.plot(time, y,'go', markersize = '5')
plt.xlabel("t [s]")
plt.ylabel("y [m]")
plt.grid(True)
plt.legend()
plt.savefig("y(t).pdf")

# Rysowanie wykresu y(x)

fig = plt.figure("y[x]", layout="constrained")
plt.title('Wykres położenia w osi y od x')
plt.plot(x, y,'ro', markersize = '5')
plt.xlabel("x [m]")
plt.ylabel("y [m]")
plt.grid(True)
plt.legend()
plt.savefig("y(x).pdf")

# Rysowanie wykresu v_x(t)

fig = plt.figure("v_x[t]", layout="constrained")
plt.title('Wykres prędkości w osi x od czasu')
plt.plot(time[1:], v_x, 'bo', markersize = '5')
plt.xlabel("t [s]")
plt.ylabel(r'$v_x$ [$\frac{m}{s}$]')
plt.grid(True)
plt.legend()
if (vx_const):
    if (v_x[0] < 0):
        plt.ylim(v_x[0] * 2, v_x[0]/2)
    elif (v_x[0] > 0):
        plt.ylim(v_x[0]/2, v_x[0] * 2)
    else:
        plt.ylim(-1, 1)
plt.savefig("v_x(t).pdf")

# Rysowanie wykresu v_y(t)

fig = plt.figure("v_y[t]", layout="constrained")
plt.title('Wykres prędkości w osi y od czasu')
plt.plot(time[1:], v_y, 'bo', markersize = '5')
plt.xlabel("t [s]")
plt.ylabel(r'$v_y$ [$\frac{m}{s}$]')
plt.grid(True)
plt.legend()
if (vy_const):
    if (np.max(v_y) < 0):
        plt.ylim(v_y[0] * 2, v_y[0]/2)
    elif (np.min(v_y) > 0):
        plt.ylim(v_y[0]/2, v_y[0] * 2)
    else:
        plt.ylim(-1, 1)
plt.savefig("v_y(t).pdf")

# Rysowanie wykresu v(t)

fig = plt.figure("v[t]", layout="constrained")
plt.title('Wykres prędkości od czasu')
plt.plot(time[1:], v, 'bo', markersize = '5')
plt.xlabel("t [s]")
plt.ylabel(r'v [$\frac{m}{s}$]')
plt.grid(True)
plt.legend()
if (vy_const and vx_const):
    if (v[0] < 0):
        plt.ylim(v[0] * 2, v[0]/2)
    elif (v[0] > 0):
        plt.ylim(v[0]/2, v[0] * 2)
    else:
        plt.ylim(-1, 1)
plt.savefig("v(t).pdf")

# Rysowanie wykresu a_x(t)

fig = plt.figure("a_x[t]", layout="constrained")
plt.title('Wykres przyspieszenia w osi x od czasu')
plt.plot(time[2:], a_x, 'mo', markersize = '5')
plt.xlabel("t [s]")
plt.ylabel(r'$a_x$ [$\frac{m}{s^2}$]')
plt.grid(True)
plt.legend()
if (ax_const):
    if (np.max(a_x) < 0):
        plt.ylim(a_x[0] * 2, a_x[0]/2)
    elif (np.min(a_x) > 0):
        plt.ylim(a_x[0]/2, a_x[0] * 2)
    else:
        plt.ylim(-1, 1)
plt.savefig("a_x(t).pdf")

# Rysowanie wykresu a_y(t)

fig = plt.figure("a_y[t]", layout="constrained")
plt.title('Wykres przyspieszenia w osi y od czasu')
plt.plot(time[2:], a_y, 'mo', markersize = '5')
plt.xlabel("t [s]")
plt.ylabel(r'$a_y$ [$\frac{m}{s^2}$]')
plt.grid(True)
plt.legend()
if (ax_const):
    if (np.max(a_y) < 0):
        plt.ylim(a_y[0] * 2, a_y[0]/2)
    elif (np.min(a_y) > 0):
        plt.ylim(a_y[0]/2, a_y[0] * 2)
    else:
        plt.ylim(-1, 1)
plt.savefig("a_y(t).pdf")

# Rysowanie wykresu a(t)

fig = plt.figure("a[t]", layout="constrained")
plt.title('Wykres wartości przyspieszenia od czasu')
plt.plot(time[2:], a, 'mo', markersize = '5')
plt.xlabel("t [s]")
plt.ylabel(r'$a$ [$\frac{m}{s^2}$]')
plt.grid(True)
plt.legend()
if (ax_const):
    if (np.max(a) < 0):
        plt.ylim(a[0] * 2, a[0]/2)
    elif (np.min(a) > 0):
        plt.ylim(a[0]/2, a[0] * 2)
    else:
        plt.ylim(-1, 1)
plt.savefig("a(t).pdf")

plt.show()