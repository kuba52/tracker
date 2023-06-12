import numpy as np
import cv2
import time
import os
import imutils
import pygame
from pygame.locals import *
import numpy as np
import pygame_gui
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import *
import os
from threading import Thread

from pygame_gui.elements import UIButton
from pygame_gui.windows import UIColourPickerDialog


def SaveToFile(wykresy, live, root):
    suma = 0
    for i in range(9):
        suma = suma + live[i].get()
    if suma != 1:
        messagebox.showerror("Error", "Tylko jeden wykres moze byc live")
        return 0
    file = open( str(os.path.abspath(os.getcwd())) + '/config.txt', 'w')
    for i in range(9):
        if (live[i].get() == 1):
            file.write("2\n")
        else:
            file.write(f"{wykresy[i].get()}\n")
        
    root.destroy()


def SetOptions():

    window = Tk()

    wykresy = []
    live = []

    for i in range(9):
        wykresy.append(IntVar())
        live.append(IntVar())


    window.columnconfigure(0, weight=1)
    window.columnconfigure(1, weight=1)

    var4 = StringVar()
    label4 = Label( window, textvariable=var4, relief=RAISED)

    var4.set("Plik")
    label4.grid(row=0,column=0)

    var5 = StringVar()
    label5 = Label( window, textvariable=var5, relief=RAISED)

    var5.set("Live")
    label5.grid(row=0,column=1)



    var = StringVar()
    label = Label( window, textvariable=var, relief=RAISED )

    var.set("Polozenia:")
    label.grid(row=1,columnspan=2)


    checkbox1 = Checkbutton(window,text='x(t)',variable=wykresy[0],onvalue=1,offvalue=0)
    checkbox1.grid(row=2,column=0)


    checkbox2 = Checkbutton(window,text='y(t)',variable=wykresy[1],onvalue=1,offvalue=0)
    checkbox2.grid(row=3,column=0)


    checkbox3 = Checkbutton(window,text='y(x)',variable=wykresy[2],onvalue=1,offvalue=0)
    checkbox3.grid(row=4,column=0)


    var2 = StringVar()
    label2 = Label( window, textvariable=var2, relief=RAISED )

    var2.set("Predkosci:")
    label2.grid(row=5,columnspan=2)


    checkbox4 = Checkbutton(window,text='v_x(t)',variable=wykresy[3],onvalue=1,offvalue=0)
    checkbox4.grid(row=6,column=0)


    checkbox5 = Checkbutton(window,text='v_y(t)',variable=wykresy[4],onvalue=1,offvalue=0)
    checkbox5.grid(row=7,column=0)


    checkbox6 = Checkbutton(window,text='v(t)',variable=wykresy[5],onvalue=1,offvalue=0)
    checkbox6.grid(row=8,column=0)


    var3 = StringVar()
    label3 = Label( window, textvariable=var3, relief=RAISED )

    var3.set("Przyspieszenia:")
    label3.grid(row=9,columnspan=2)


    checkbox7 = Checkbutton(window,text='a_x(t)',variable=wykresy[6],onvalue=1,offvalue=0)
    checkbox7.grid(row=10,column=0)


    checkbox8 = Checkbutton(window,text='a_y(t)',variable=wykresy[7],onvalue=1,offvalue=0)
    checkbox8.grid(row=11,column=0)


    checkbox9 = Checkbutton(window,text='a(t)',variable=wykresy[8],onvalue=1,offvalue=0)
    checkbox9.grid(row=12,column=0)



    var4 = StringVar()
    label = Label( window, textvariable=var, relief=RAISED )


    checkbox10 = Checkbutton(variable=live[0],onvalue=1,offvalue=0)
    checkbox10.grid(row=2,column=1)


    checkbox11 = Checkbutton(variable=live[1],onvalue=1,offvalue=0)
    checkbox11.grid(row=3,column=1)


    checkbox12 = Checkbutton(variable=live[2],onvalue=1,offvalue=0)
    checkbox12.grid(row=4,column=1)



    checkbox13 = Checkbutton(variable=live[3],onvalue=1,offvalue=0)
    checkbox13.grid(row=6,column=1)


    checkbox14 = Checkbutton(variable=live[4],onvalue=1,offvalue=0)
    checkbox14.grid(row=7,column=1)


    checkbox15 = Checkbutton(variable=live[5],onvalue=1,offvalue=0)
    checkbox15.grid(row=8,column=1)


    checkbox7 = Checkbutton(variable=live[6],onvalue=1,offvalue=0)
    checkbox7.grid(row=10,column=1)


    checkbox8 = Checkbutton(variable=live[7],onvalue=1,offvalue=0)
    checkbox8.grid(row=11,column=1)


    checkbox9 = Checkbutton(variable=live[8],onvalue=1,offvalue=0)
    checkbox9.grid(row=12,column=1)



    button = Button(window, text ="Save", command =lambda:  SaveToFile(wykresy, live, window))
    button.grid(row=13,column=1)


    window.mainloop()












global lower 
lower = True
global lower_bound, upper_bound, lower_rgb, upper_rgb
lower_rgb = pygame.Color(2, 2, 3)
upper_rgb = pygame.Color(55, 0, 255)
lower_bound = np.array([94, 80, 2])
upper_bound = np.array([126, 255, 255])
beg_time = time.perf_counter()
start_info = False
file = open( str(os.path.abspath(os.getcwd())) + '/data.txt', 'w')

ask = messagebox.askyesno("Pytanie","Czy chcesz sledzic obiekt z nagrania?")

if ask:

    application_window = tk.Tk()

    # Build a list of tuples for each file type the file dialog should display
    my_filetypes = [('pliki video', '.mp4')]


    # Ask the user to select a single file name.
    path = filedialog.askopenfilename(parent=application_window,
                                        initialdir=os.getcwd(),
                                        title="Wybierz plik:",
                                        filetypes=my_filetypes)
    
    screen_height = application_window.winfo_screenheight()
    application_window.destroy()


    cap = cv2.VideoCapture(path)

    ret, imageFrame = cap.read()
    imageFrame = imutils.resize(imageFrame, height=int(3*screen_height/4))

    dimensions = imageFrame.shape

    height = imageFrame.shape[0]
    width = imageFrame.shape[1]

    pygame.init()
    pygame.display.set_caption("Wybierz kolor sledzonego obiektu")
    screen = pygame.display.set_mode((width, height))

    ui_manager = pygame_gui.UIManager((width, height))
    lower_bound_button = UIButton(relative_rect=pygame.Rect(-180, -60, 150, 30),
                                    text='Lower Bound',
                                    manager=ui_manager,
                                    anchors={'left': 'right',
                                            'right': 'right',
                                            'top': 'bottom',
                                            'bottom': 'bottom'})

    upper_bound_button = UIButton(relative_rect=pygame.Rect(-180, -100, 150, 30),
                                    text='Upper Bound',
                                    manager=ui_manager,
                                    anchors={'left': 'right',
                                            'right': 'right',
                                            'top': 'bottom',
                                            'bottom': 'bottom'})

    start = UIButton(relative_rect=pygame.Rect(-180, -140, 150, 30),
                                    text='start',
                                    manager=ui_manager,
                                    anchors={'left': 'right',
                                            'right': 'right',
                                            'top': 'bottom',
                                            'bottom': 'bottom'})
    
    options = UIButton(relative_rect=pygame.Rect(-180, -180, 150, 30),
                                    text='options',
                                    manager=ui_manager,
                                    anchors={'left': 'right',
                                            'right': 'right',
                                            'top': 'bottom',
                                            'bottom': 'bottom'})


    clock = pygame.time.Clock()
   
    while not start_info:

        imageFrame2 = imageFrame.copy()

        hsvFrame = cv2.cvtColor(imageFrame2, cv2.COLOR_BGR2HSV)
        
        mask = cv2.inRange(hsvFrame, lower_bound, upper_bound)

        kernel = np.ones((5, 5), "uint8")
        mask = cv2.erode(mask, kernel, iterations=1)
        mask = cv2.dilate(mask, kernel)
        res = cv2.bitwise_and(imageFrame2, imageFrame2,
                                    mask = mask)
        
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        if len(contours) > 0:
            contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(contour)
            imageFrame2 = cv2.rectangle(imageFrame2, (x, y), (x + w, y + h), (0, 255, 0), 2)

        imageFrame2 = cv2.cvtColor(imageFrame2, cv2.COLOR_BGR2RGB)
        imageFrame2 = cv2.flip(imageFrame2,1)
        imageFrame2 = np.rot90(imageFrame2)
        frame = pygame.surfarray.make_surface(imageFrame2)
        screen.blit(frame, (0,0))

        time_delta = clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == lower_bound_button:
                lower = True
                colour_picker = UIColourPickerDialog(pygame.Rect(160, 50, 420, 400),
                                                    ui_manager,
                                                    window_title="Set Lower Bound",
                                                    initial_colour=lower_rgb)
                lower_bound_button.disable()

            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == upper_bound_button:
                lower = False
                colour_picker = UIColourPickerDialog(pygame.Rect(160, 50, 420, 400),
                                                    ui_manager,
                                                    window_title="Set Upper Bound",
                                                    initial_colour=upper_rgb)
                upper_bound_button.disable()

            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == options:
                SetOptions()


            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == start:
                start_info = True
                start.disable()

            if event.type == pygame_gui.UI_COLOUR_PICKER_COLOUR_PICKED:
                tmp = list(event.colour.hsva)[:3]
                tmp2 = []
                tmp2.append(int(tmp[0]/360*179))
                tmp2.append(int(tmp[1]/100*255))
                tmp2.append(int(tmp[2]/100*255))
                if lower:
                    lower_rgb = event.colour
                    lower_bound = np.array(tmp2)

                else:
                    upper_rgb = event.colour
                    upper_bound = np.array(tmp2)



            if event.type == pygame_gui.UI_WINDOW_CLOSE:
                lower_bound_button.enable()
                upper_bound_button.enable()
            
            ui_manager.process_events(event)

        ui_manager.update(time_delta)


        ui_manager.draw_ui(screen)

        pygame.display.update()

    pygame.quit()

    while (cap.isOpened()):
        ret, imageFrame = cap.read()
        if not ret:
            break
        hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsvFrame, lower_bound, upper_bound)
        kernel = np.ones((5, 5), "uint8")
        mask = cv2.erode(mask, kernel, iterations=1)
        mask = cv2.dilate(mask, kernel)
        res = cv2.bitwise_and(imageFrame, imageFrame, mask = mask)
		
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) > 0:
            contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(contour)
            file.write(f'{x}\t{y}\t{cap.get(cv2.CAP_PROP_POS_MSEC)/1000}\n')
            imageFrame = cv2.rectangle(imageFrame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        imageFrame = imutils.resize(imageFrame, height=int(3*screen_height/4))
        cv2.imshow("Controls", imageFrame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            end_time = time.perf_counter()
            cap.release()
            cv2.destroyAllWindows()
            break


    cap.release()
    file.write("dupa\n")
    file.close()
    cv2.destroyAllWindows()

else:

    cam = cv2.VideoCapture(0)

    _, imageFrame = cam.read()

    dimensions = imageFrame.shape

    height = imageFrame.shape[0]
    width = imageFrame.shape[1]


    pygame.init()
    pygame.display.set_caption("Wybierz kolor sledzonego obiektu")
    screen = pygame.display.set_mode((width, height))

    ui_manager = pygame_gui.UIManager((width, height))
    lower_bound_button = UIButton(relative_rect=pygame.Rect(-180, -60, 150, 30),
                                    text='Lower Bound',
                                    manager=ui_manager,
                                    anchors={'left': 'right',
                                            'right': 'right',
                                            'top': 'bottom',
                                            'bottom': 'bottom'})

    upper_bound_button = UIButton(relative_rect=pygame.Rect(-180, -100, 150, 30),
                                    text='Upper Bound',
                                    manager=ui_manager,
                                    anchors={'left': 'right',
                                            'right': 'right',
                                            'top': 'bottom',
                                            'bottom': 'bottom'})

    start = UIButton(relative_rect=pygame.Rect(-180, -140, 150, 30),
                                    text='start',
                                    manager=ui_manager,
                                    anchors={'left': 'right',
                                            'right': 'right',
                                            'top': 'bottom',
                                            'bottom': 'bottom'})
    
    options = UIButton(relative_rect=pygame.Rect(-180, -180, 150, 30),
                                text='options',
                                manager=ui_manager,
                                anchors={'left': 'right',
                                        'right': 'right',
                                        'top': 'bottom',
                                        'bottom': 'bottom'})




    clock = pygame.time.Clock()

    

    while not start_info:
        
        _, imageFrame = cam.read()

        hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)
        
        mask = cv2.inRange(hsvFrame, lower_bound, upper_bound)

        kernel = np.ones((5, 5), "uint8")
        mask = cv2.erode(mask, kernel, iterations=1)
        mask = cv2.dilate(mask, kernel)
        res = cv2.bitwise_and(imageFrame, imageFrame,
                                    mask = mask)
        
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        if len(contours) > 0:
            contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(contour)
            imageFrame = cv2.rectangle(imageFrame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        imageFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2RGB)
        imageFrame = cv2.flip(imageFrame,1)
        imageFrame = np.rot90(imageFrame)
        frame = pygame.surfarray.make_surface(imageFrame)
        screen.blit(frame, (0,0))

        time_delta = clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == lower_bound_button:
                lower = True
                colour_picker = UIColourPickerDialog(pygame.Rect(160, 50, 420, 400),
                                                    ui_manager,
                                                    window_title="Set Lower Bound",
                                                    initial_colour=lower_rgb)
                lower_bound_button.disable()

            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == upper_bound_button:
                lower = False
                colour_picker = UIColourPickerDialog(pygame.Rect(160, 50, 420, 400),
                                                    ui_manager,
                                                    window_title="Set Upper Bound",
                                                    initial_colour=upper_rgb)
                upper_bound_button.disable()

            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == options:
                helper = Thread(target= SetOptions)
                helper.start()

            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == start:
                beg_time = time.perf_counter()
                start_info = True
                start.disable()

            if event.type == pygame_gui.UI_COLOUR_PICKER_COLOUR_PICKED:
                tmp = list(event.colour.hsva)[:3]
                tmp2 = []
                tmp2.append(int(tmp[0]/360*179))
                tmp2.append(int(tmp[1]/100*255))
                tmp2.append(int(tmp[2]/100*255))
                if lower:
                    lower_rgb = event.colour
                    lower_bound = np.array(tmp2)
                else:
                    upper_rgb = event.colour
                    upper_bound = np.array(tmp2)


            if event.type == pygame_gui.UI_WINDOW_CLOSE:
                lower_bound_button.enable()
                upper_bound_button.enable()
            
            ui_manager.process_events(event)

        ui_manager.update(time_delta)


        ui_manager.draw_ui(screen)

        pygame.display.update()

    pygame.quit()

    while(True):
            
            _, imageFrame = cam.read()


            hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)
            
            mask = cv2.inRange(hsvFrame, lower_bound, upper_bound)

            kernel = np.ones((5, 5), "uint8")
            mask = cv2.erode(mask, kernel, iterations=1)
            mask = cv2.dilate(mask, kernel)
            res = cv2.bitwise_and(imageFrame, imageFrame,
                                        mask = mask)
            
            contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            
            if len(contours) > 0:
                contour = max(contours, key=cv2.contourArea)
                x, y, w, h = cv2.boundingRect(contour)
                file.write(f'{x}\t{y}\t{time.perf_counter() - beg_time}\n')
                imageFrame = cv2.rectangle(imageFrame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            cv2.imshow("Sledzenie (nacisnij q aby zakonczyc)", imageFrame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                end_time = time.perf_counter()
                cam.release()
                cv2.destroyAllWindows()
                break
    file.write("dupa\n")
    file.close()
    cv2.destroyAllWindows()