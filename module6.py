import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
from picamera import PiCamera
import picamera.array
from time import sleep
import cv2
import math
import numpy as np

#setup duty cycle
PWM_pin = 12
freq = 50
dutyCycle = 25
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PWM_pin,GPIO.OUT)
pwm = GPIO.PWM(PWM_pin, freq)
#setup camera
camera = PiCamera()
camera.rotation = 180
stream = picamera.array.PiRGBArray(camera)

#function camera
def camera2angle():
	#take picture
	camera.capture(stream,format='bgr',use_video_port=True)
	img = stream.array
	stream.truncate(0)
	#find ball
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv, (100, 150, 0),(135,255,255))
	#get center of mass
	M = cv2.moments(mask)
	cX = int(M["m10"] / M["m00"])
	cY = int(M["m01"] / M["m00"])
	#calc angle from camera
	angle = (360/math.pi)
	angle2 = 90-(angle*(math.atan(float(cY)/float(cX))))
#	if angle2 > 0:
#		print("Angle: %s" %angle2) #if the angle is positive
#	elif angle2 < 0:
#		angle2 = abs(angle2)+90 #positive and 90-180 range
#		print("Angle: %s" %angle2)
	return angle2

#function duty cycle
def angle2dutycycle(angle2):
	servo_pwm = angle2/15.0 #camera properly angled
	pwm.start(servo_pwm)
	time.sleep(1)
	pwm.stop()

#METHOD

#camera2angle() #take picture, find CM of ball, get angle
#if angle2>10: #if angle is more than 10deg, stop
#	angle2dutycycle(angle2)
#else
#	print("Camera is pointed at ball") 


angle2 = camera2angle()
while angle2>10:
	angle2dutycycle(angle2)
	angle2 = camera2angle()
print("Camera pointed at ball")
