import cv2
import imutils
import numpy as np
import pytesseract
from PIL import Image
from picamera.array import PiRGBArray
from picamera import PiCamera
import RPi.GPIO as GPIO
import time
from time import sleep
from Adafruit_CharLCD import Adafruit_CharLCD
import sqlite3
import datetime

def updateSqliteTable(plate_number):
    try:
        sqliteConnection = sqlite3.connect('db.sqlite3')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        exit = datetime.datetime.now()
        sql_update_query = """Update Vehicle_Parkings set exit_time = ? where plate_number = ?"""
        data = (exit, plate_number)
        cursor.execute(sql_update_query, data)
        sqliteConnection.commit()
        print("Record Updated successfully ")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to update sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(640, 480))
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array
        cv2.imshow("Frame", image)
        key = cv2.waitKey(1) & 0xFF
        rawCapture.truncate(0)
        if key == ord("s"):
             gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #convert to grey scale
             gray = cv2.bilateralFilter(gray, 11, 17, 17) #Blur to reduce noise
             edged = cv2.Canny(gray, 30, 200) #Perform Edge detection
             cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE,              cv2.CHAIN_APPROX_SIMPLE)
             cnts = imutils.grab_contours(cnts)
             cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]
             screenCnt = None
             for c in cnts:
                peri = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.018 * peri, True)
                if len(approx) == 4:
                  screenCnt = approx
                  break
             if screenCnt is None:
               detected = 0
               print ("No contour detected")
             else:
               detected = 1
             if detected == 1:
               cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 3)
             mask = np.zeros(gray.shape,np.uint8)
             new_image = cv2.drawContours(mask,[screenCnt],0,255,-1,)
             new_image = cv2.bitwise_and(image,image,mask=mask)
             (x, y) = np.where(mask == 255)
             (topx, topy) = (np.min(x), np.min(y))
             (bottomx, bottomy) = (np.max(x), np.max(y))
             Cropped = gray[topx:bottomx+1, topy:bottomy+1]
             text = pytesseract.image_to_string(Cropped, config='--psm 11')

             rand_str = ""
             for x in text:
                 if(x.isdigit() or x.isalpha()):
                     rand_str = rand_str + x
             final_str = rand_str[0:10]

             print("Detected Number is:",final_str)

             updateSqliteTable(final_str)

            #  cv2.imshow("Frame", image)
            #  cv2.imshow('Cropped',Cropped)
             
             #LCD OPERATION
             lcd = Adafruit_CharLCD(rs=26, en=19,
                                    d4=13, d5=6, d6=5, d7=11,
                                    cols=16, lines=2)
             lcd.clear()
             lcd_1 = v.parking_spot + '  ' + "Vacated"
             lcd.message(lcd_1)
             # lcd.message("Vacated")
             
             #SERVO MOTOR OPERATION
             # Set GPIO numbering mode
             GPIO.setmode(GPIO.BCM)
             # Set pin 11 as an output, and set servo1 as pin 11 as PWM
             GPIO.setup(17,GPIO.OUT)
             servo1 = GPIO.PWM(17,50) # Note 11 is pin, 50 = 50Hz pulse
             #start PWM running, but with value of 0 (pulse off)
             servo1.start(0)
             print ("Waiting for 2 seconds")
             time.sleep(2)           #Plate recognition
             #90 degrees
             print ("Rotating 90 degrees")
             servo1.ChangeDutyCycle(7)
             time.sleep(5)
             #servo1.ChangeDutyCycle(0)
             #back to 0
             print ("Rotating back to 0")
             servo1.ChangeDutyCycle(2)
             time.sleep(0.5)
             servo1.ChangeDutyCycle(0)
             servo1.stop()
             GPIO.cleanup()
             print ("Goodbye")
             
             cv2.waitKey(0)
             break
cv2.destroyAllWindows()

