import numpy as np
import cv2
import time
import os
import imutils

global lower_bound, upper_bound
lower_bound = np.array([94, 80, 2])
upper_bound = np.array([126, 255, 255])
beg_time = time.perf_counter()
start = False


def set_red(*args):
	global lower_bound, upper_bound
	lower_bound = np.array([161, 155, 84])
	upper_bound = np.array([179, 255, 255])
	cv2.setTrackbarPos("Lower Hue", "Controls", 161)
	cv2.setTrackbarPos("Lower Saturation", "Controls", 155)
	cv2.setTrackbarPos("Lower Value", "Controls", 84)
	cv2.setTrackbarPos("Upper Hue", "Controls", 179)
	cv2.setTrackbarPos("Upper Saturation", "Controls", 255)
	cv2.setTrackbarPos("Upper Value", "Controls", 255)


def set_blue(*args):
	global lower_bound, upper_bound
	lower_bound = np.array([94, 80, 2])
	upper_bound = np.array([126, 255, 255])
	cv2.setTrackbarPos("Lower Hue", "Controls", 94)
	cv2.setTrackbarPos("Lower Saturation", "Controls", 80)
	cv2.setTrackbarPos("Lower Value", "Controls", 2)
	cv2.setTrackbarPos("Upper Hue", "Controls", 126)
	cv2.setTrackbarPos("Upper Saturation", "Controls", 255)
	cv2.setTrackbarPos("Upper Value", "Controls", 255)


def set_green(*args):
	global lower_bound, upper_bound
	lower_bound = np.array([25, 52, 72])
	upper_bound = np.array([102, 255, 255])
	cv2.setTrackbarPos("Lower Hue", "Controls", 25)
	cv2.setTrackbarPos("Lower Saturation", "Controls", 52)
	cv2.setTrackbarPos("Lower Value", "Controls", 72)
	cv2.setTrackbarPos("Upper Hue", "Controls", 102)
	cv2.setTrackbarPos("Upper Saturation", "Controls", 255)
	cv2.setTrackbarPos("Upper Value", "Controls", 255)



def on_lower_hue_changed(value):
    global lower_bound
    lower_bound[0] = value
    
def on_lower_saturation_changed(value):
    global lower_bound
    lower_bound[1] = value
    
def on_lower_value_changed(value):
    global lower_bound
    lower_bound[2] = value

def on_upper_hue_changed(value):
    global upper_bound
    upper_bound[0] = value
    
def on_upper_saturation_changed(value):
    global upper_bound
    upper_bound[1] = value
    
def on_upper_value_changed(value):
    global upper_bound
    upper_bound[2] = value
    
def reset_time(*args):
	global beg_time
	beg_time = time.perf_counter()

cv2.namedWindow("Controls")

cv2.createTrackbar("Lower Hue", "Controls", lower_bound[0], 179, on_lower_hue_changed)
cv2.createTrackbar("Lower Saturation", "Controls", lower_bound[1], 255, on_lower_saturation_changed)
cv2.createTrackbar("Lower Value", "Controls", lower_bound[2], 255, on_lower_value_changed)

cv2.createTrackbar("Upper Hue", "Controls", upper_bound[0], 179, on_upper_hue_changed)
cv2.createTrackbar("Upper Saturation", "Controls", upper_bound[1], 25, on_upper_saturation_changed)
cv2.createTrackbar("Upper Value", "Controls", upper_bound[2], 255, on_lower_value_changed)

cv2.createButton("Reset time", reset_time, None,cv2.QT_PUSH_BUTTON,1)
cv2.createButton("Set red", set_red, None,cv2.QT_PUSH_BUTTON ,0)
cv2.createButton("Set blue", set_blue, None,cv2.QT_PUSH_BUTTON ,0)
cv2.createButton("Set green", set_green, None,cv2.QT_PUSH_BUTTON,0)


select = int(input("Select source:"))

file = open( str(os.path.abspath(os.getcwd())) + '/data.txt', 'w')

if select == 1:

	cam = cv2.VideoCapture(0)
	
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
			if start:
				file.write(f'{x}\t{y}\t{time.perf_counter() - beg_time}\n')
			imageFrame = cv2.rectangle(imageFrame, (x, y), (x + w, y + h), (0, 255, 0), 2)

		cv2.imshow("Controls", imageFrame)

		if cv2.waitKey(1) & 0xFF == ord('s'):
			start = True
			beg_time = time.perf_counter()
			print("Recording started")

		if cv2.waitKey(1) & 0xFF == ord('q'):
			end_time = time.perf_counter()
			cam.release()
			cv2.destroyAllWindows()
			break
		
if select == 2:
	src = input("Enter video path:")
	cap = cv2.VideoCapture(src)
	col = input("Select color: red | gren | blue\n")

	if col == "red":
		set_green()
	if col == "blue":
		set_blue()
	if col == "green":
		set_green()

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
		
		imageFrame = imutils.resize(imageFrame, height=400)
		cv2.imshow("Controls", imageFrame)

		if cv2.waitKey(1) & 0xFF == ord('q'):
			end_time = time.perf_counter()
			cap.release()
			cv2.destroyAllWindows()
			break


	cap.release()

file.close()
cv2.destroyAllWindows()