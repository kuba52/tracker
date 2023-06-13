from matplotlib import pyplot as plt
import numpy as np
import time as t
import csv

# wczytywanie pliku konfiguracyjnego
# 0 - brak wykresu, 1 - jest zapisywany, 2 - jest na żywo
# kolejność: x(t), y(t), y(x), vx(t), vy(t), v(t), ax(t), ay(t), a(t)
def config():
    f = open("config.txt", 'r')
    lines = f.readlines()
    plot = np.empty(len(lines), dtype = int)
    for i in range(0, len(lines)):
        plot[i] = int(lines[i])
    return plot

# Wczytywanie danych
def updater(last_file_position):
    f = open("data2.txt", 'r')
    f.seek(last_file_position)
    data = f.readlines()
    last_file_position = f.tell()
    end = False
    #print(len(data))
    if (len(data) > 0 and data[0] == '\n'):
        data = data[1:len(data)]
    if (len(data) > 0 and data[len(data) - 1] == "dupa"):
        end = True
        data = data[0: len(data) - 1]
    new_x = np.empty(len(data), dtype=float) # położenia w osi x w mm
    new_y = np.empty(len(data), dtype=float) # położenia w osi y w mm
    new_time = np.empty(len(data), dtype=float)
   
    for i in range(0, len(data)):
        s = data[i]
        coordinates = s.split() # x y t
        new_x[i] = float(coordinates[0])/10
        new_y[i] = float(coordinates[1])/10
        new_time[i] = float(coordinates[2])
    f.close()
    return last_file_position, new_x, new_y, new_time, end

# kalkulacja prędkości
def calculate_velocities(x, y, time, last_processed_index):
    if (len(x) == 0):
        e = np. empty(0, dtype = float)
        return last_processed_index, e, e, e
    if (last_processed_index == -1):
        v_x = np.empty(x.size - 1, dtype=float)
        v_y = np.empty(y.size - 1, dtype=float)
        v = np.empty(x.size - 1, dtype=float)
        last_processed_index = 0
    else:
        v_x = np.empty(x.size - 1 - last_processed_index, dtype=float)
        v_y = np.empty(y.size - 1 - last_processed_index, dtype=float)
        v = np.empty(x.size - 1 - last_processed_index, dtype=float)
    
    for i in range(last_processed_index, v_x.size + last_processed_index):
        time_step = time[i + 1] - time[i]
        v_x[i - last_processed_index] = (x[i + 1] - x[i])/time_step
        
        
    for i in range(last_processed_index, v_y.size + last_processed_index):
        time_step = time[i + 1] - time[i]
        v_y[i - last_processed_index] = (y[i + 1] - y[i])/time_step

    for i in range(0, v.size):
        v[i] = np.sqrt(v_x[i]**2 + v_y[i]**2)
        
    last_processed_index += v.size
    return last_processed_index, v_x, v_y, v

# kalkulacja przyspieszeń
def calculate_accelerations(v_x, v_y, v, last_processed_index):
    if (len(v) == 0):
        e = np. empty(0, dtype = float)
        return e, e, e
    if (last_processed_index < 0):
        last_processed_index = 0
    a_x = np.empty(v_x.size - 1 - last_processed_index, dtype=float)
    a_y = np.empty(v_y.size - 1 - last_processed_index, dtype=float)
    a = np.empty(v.size - 1 - last_processed_index, dtype=float)
    for i in range(last_processed_index, a.size + last_processed_index):
        time_step = time[i + 2] - time[i + 1]
        a_x[i - last_processed_index] = (v_x[i+1] - v_x[i])/time_step
        a_y[i - last_processed_index] = (v_y[i+1] - v_y[i])/time_step
        a[i - last_processed_index] = (v[i+1] - v_x[i])/time_step   
    return a_x, a_y, a
  
# tablica z informacjami konfiguracyjnymi  
plot = config() #

x = np.empty(0, dtype=float) # położenia w osi x w cm
y = np.empty(0, dtype=float) # położenia w osi y w cm
time = np.empty(0, dtype=float)
last_file_position = 0

# ostatni numer indeksu w tablicy x lub y, który brał udział w obliczeniach
last_processed_index = -1

v_x = np.arange(0, dtype=float)
v_y = np.arange(0, dtype=float)
v = np.arange(0, dtype=float)

a_x = np.arange(0, dtype=float)
a_y = np.arange(0, dtype=float)
a = np.arange(0, dtype=float)

vx_const = True
vy_const = True
ax_const = True
ay_const = True
a_const = True
# min and max values in an array may differ by less than ER and still will be considered constant
ER = 0.0001

end = False
sleep_time = 3

while(not end):   
    
    # Aktualizacja współrzędnych czasoprzestrzennych
    last_file_position, new_x, new_y, new_time, end = updater(last_file_position)
    x = np.concatenate((x, new_x))
    y = np.concatenate((y, new_y))
    time = np.concatenate((time, new_time))
    
    # Aktualizacja wartości prędkości
    new_last_processed_index, new_vx, new_vy, new_v = calculate_velocities(x, y, time, last_processed_index)
    v_x = np.concatenate((v_x, new_vx))
    v_y = np.concatenate((v_y, new_vy))
    v = np.concatenate((v, new_v))
    
    # Czy prędkości są stałe
    if (vx_const and len(v_x) != 0):
        vx_const = np.max(v_x) - np.min(v_x) < ER
    if (vy_const and len(v_y) != 0):
        vy_const = np.max(v_y) - np.min(v_y) < ER
    
    # kalkulacja przyspieszeń
    new_ax, new_ay, new_a = calculate_accelerations(v_x, v_y, v, last_processed_index - 1)
    a_x = np.concatenate((a_x, new_ax))
    a_y = np.concatenate((a_y, new_ay))
    a = np.concatenate((a, new_a))
    
    last_processed_index = new_last_processed_index
    # Czy przyspieszenia są stałe
    if (ax_const and len(a_x) != 0):
        ax_const = np.max(a_x) - np.min(a_x) < ER
    if (ay_const and len(a_y) != 0):
        ay_const = np.max(a_y) - np.min(a_y) < ER
    if(a_const and len(a) != 0):
        a_const = np.max(a) - np.min(a) < ER
    
    
    # Rysowanie wykresu x(t)
    #plt.ion()
    
    if (plot[0] > 0):
        fig = plt.figure("x[t]", layout="constrained")
        plt.title('Wykres położenia (oś x) od czasu')
        plt.plot(time, x,'go', markersize = '5')
        plt.xlabel("t [s]")
        plt.ylabel("x [cm]")
        plt.grid(True)
        plt.legend()
        plt.savefig("x(t).pdf")
        if (plot[0] == 2):
            fig.show()
            plt.pause(0.1)
        if (plot[0] == 1):
            plt.close(fig)
    
    # Rysowanie wykresu y(t)
    
    if (plot[1] > 0):
        fig = plt.figure("y[t]", layout="constrained")
        plt.title('Wykres położenia (oś y) od czasu')
        plt.plot(time, y,'go', markersize = '5')
        plt.xlabel("t [s]")
        plt.ylabel("y [cm]")
        plt.grid(True)
        plt.legend()
        plt.savefig("y(t).pdf")
        if (plot[1] == 2):
            fig.show()
            plt.pause(0.1)
        if (plot[1] == 1):
            plt.close(fig)
    
    # Rysowanie wykresu y(x)
    
    if (plot[2] > 0):
        fig = plt.figure("y[x]", layout="constrained")
        plt.title('Wykres położenia w osi y od x')
        plt.plot(x, y,'ro', markersize = '5')
        plt.xlabel("x [cm]")
        plt.ylabel("y [cm]")
        plt.grid(True)
        plt.legend()
        plt.savefig("y(x).pdf")
        if (plot[2] == 2):
            fig.show()
            plt.pause(0.1)
        if (plot[2] == 1):
            plt.close(fig)
    # Rysowanie wykresu v_x(t)
    
    if (plot[3] > 0):
        fig = plt.figure("v_x[t]", layout="constrained")
        plt.title('Wykres prędkości w osi x od czasu')
        plt.plot(time[1:], v_x, 'bo', markersize = '5')
        plt.xlabel("t [s]")
        plt.ylabel(r'$v_x$ [$\frac{cm}{s}$]')
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
        if (plot[3] == 2):
            fig.show()
            plt.pause(0.1)
        else:
            plt.close(fig)
    
    # Rysowanie wykresu v_y(t)
    
    if (plot[4] > 0):
        fig = plt.figure("v_y[t]", layout="constrained")
        plt.title('Wykres prędkości w osi y od czasu')
        plt.plot(time[1:], v_y, 'bo', markersize = '5')
        plt.xlabel("t [s]")
        plt.ylabel(r'$v_y$ [$\frac{cm}{s}$]')
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
        if (plot[4] == 2):
            fig.show()
            plt.pause(0.1)
        else:
            plt.close(fig)
    # Rysowanie wykresu v(t)
    
    if (plot[5] > 0):
        fig = plt.figure("v[t]", layout="constrained")
        plt.title('Wykres prędkości od czasu')
        plt.plot(time[1:], v, 'bo', markersize = '5')
        plt.xlabel("t [s]")
        plt.ylabel(r'v [$\frac{cm}{s}$]')
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
        if (plot[5] == 2):
            fig.show()
            plt.pause(0.1)
        else:
            plt.close(fig)
    # Rysowanie wykresu a_x(t)
    
    if (plot[6] > 0):
        fig = plt.figure("a_x[t]", layout="constrained")
        plt.title('Wykres przyspieszenia w osi x od czasu')
        plt.plot(time[2:], a_x, 'mo', markersize = '5')
        plt.xlabel("t [s]")
        plt.ylabel(r'$a_x$ [$\frac{cm}{s^2}$]')
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
        if (plot[6] == 2):
            fig.show()
            plt.pause(0.1)
        else:
            plt.close(fig)
    # Rysowanie wykresu a_y(t)
    
    if (plot[7] > 0):
        fig = plt.figure("a_y[t]", layout="constrained")
        plt.title('Wykres przyspieszenia w osi y od czasu')
        plt.plot(time[2:], a_y, 'mo', markersize = '5')
        plt.xlabel("t [s]")
        plt.ylabel(r'$a_y$ [$\frac{cm}{s^2}$]')
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
        if (plot[7] == 2):
            fig.show()
            plt.pause(0.1)
        else:
            plt.close(fig)
    # Rysowanie wykresu a(t)
    
    if (plot[8] > 0):
        fig = plt.figure("a[t]", layout="constrained")
        plt.title('Wykres wartości przyspieszenia od czasu')
        plt.plot(time[2:], a, 'mo', markersize = '5')
        plt.xlabel("t [s]")
        plt.ylabel(r'$a$ [$\frac{cm}{s^2}$]')
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
        if (plot[8] == 2):
            fig.show()
            plt.pause(0.1)
        else:
            plt.close()
    #plt.show()
    t.sleep(sleep_time)

# zapisz dane o położeniach
header = ['x(t)', 'y(t)', 't']
with open('xy.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)

    # write the header
    writer.writerow(header)
    
    for i in range (0, x.size):
        row = np.empty(3, dtype=float)
        row[0] = x[i]
        row[1] = y[i]
        row[2] = time[i]
        # write the data
        writer.writerow(row)

#zapisz dane o prędkościach    
header = ['v_x(t)', 'v_y(t)', 'v(t)', 't']
with open('v.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)

    # write the header
    writer.writerow(header)
    
    for i in range (0, v.size):
        row = np.empty(4, dtype=float)
        row[0] = v_x[i]
        row[1] = v_y[i]
        row[2] = v[i]
        row[3] = time[i + 1]
        # write the data
        writer.writerow(row)

#zapisz dane o przyspieszeniach         
header = ['a_x(t)', 'a_y(t)', 'a(t)', 't']
with open('a.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)

    # write the header
    writer.writerow(header)
    
    for i in range (0, a.size):
        row = np.empty(4, dtype=float)
        row[0] = a_x[i]
        row[1] = a_y[i]
        row[2] = a[i]
        row[3] = time[i + 2]
        # write the data
        writer.writerow(row)