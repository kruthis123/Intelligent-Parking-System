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
from numpy import asarray
from numpy import savetxt
from numpy import loadtxt
import sys

class MinHeap:
    def __init__(self, data):
        self.maxsize = 110
        self.size = len(data)
        self.Heap = data
        self.FRONT = 1
 
    # Function to return the position of parent for the node currently at pos
    def parent(self, pos):
        return pos//2
 
    # Function to return the position of the left child for the node currently at pos
    def leftChild(self, pos):
        return 2 * pos
 
    # Function to return the position of the right child for the node currently at pos
    def rightChild(self, pos):
        return (2 * pos) + 1
 
    # Function that returns true if the passed node is a leaf node
    def isLeaf(self, pos):
        if pos >= (self.size//2) and pos <= self.size:
            return True
        return False
 
    # Function to swap two nodes of the heap
    def swap(self, fpos, spos):
        self.Heap[fpos], self.Heap[spos] = self.Heap[spos], self.Heap[fpos]
 
    # Function to heapify the node at pos
    def minHeapify(self, pos):
 
        # If the node is a non-leaf node and greater than any of its child
        if not self.isLeaf(pos):
            if (self.Heap[pos] > self.Heap[self.leftChild(pos)] or
               self.Heap[pos] > self.Heap[self.rightChild(pos)]):
 
                # Swap with the left child and heapify the left child
                if self.Heap[self.leftChild(pos)] < self.Heap[self.rightChild(pos)]:
                    self.swap(pos, self.leftChild(pos))
                    self.minHeapify(self.leftChild(pos))
 
                # Swap with the right child and heapify the right child
                else:
                    self.swap(pos, self.rightChild(pos))
                    self.minHeapify(self.rightChild(pos))
 
    # Function to insert a node into the heap
    def insert(self, element):
        if self.size >= self.maxsize :
            return
        self.size+= 1
        self.Heap[self.size] = element
 
        current = self.size
 
        while self.Heap[current] < self.Heap[self.parent(current)]:
            self.swap(current, self.parent(current))
            current = self.parent(current)
 
    # Function to build the min heap using the minHeapify function
    def minHeap(self):
 
        for pos in range(self.size//2, 0, -1):
            self.minHeapify(pos)
 
    # Function to remove and return the minimum element from the heap
    def remove(self):
 
        popped = self.Heap[self.FRONT]
        self.Heap[self.FRONT] = self.Heap[self.size - 1]
        self.size-= 1
        self.minHeapify(self.FRONT)
        return popped

class Vehicle:
    def __init__(self, vehicle_number, vehicle_type, pl):
        self.vehicle_number = vehicle_number
        self.vehicle_type = vehicle_type
        self.parking_spot = pl.remove()
        print(f"Inserted at {self.parking_spot}")

def insertVaribleIntoTable(v):
    try:
        sqliteConnection = sqlite3.connect('db.sqlite3')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_insert_with_param = """INSERT INTO Vehicle_Parkings
                          (plate_number, vehicle_type, parking_spot, entry_time) 
                          VALUES (?, ?, ?, ?);"""

        data_tuple = (v.vehicle_number, v.vehicle_type, v.parking_spot, datetime.datetime.now())
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqliteConnection.commit()
        print("Python Variables inserted successfully into Vehicle_Parkings table")

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

data = loadtxt('data.csv', delimiter=',')
data_list = list(data)
data_list = [int(x) for x in data_list]

pl = MinHeap(data_list)

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
                     
             print("Detected Number is:", final_str)
             v = Vehicle(final_str, 2, pl)
             insertVaribleIntoTable(v)
             cv2.imshow("Frame", image)
             cv2.imshow('Cropped',Cropped)
             
             #LCD OPERATION
             lcd = Adafruit_CharLCD(rs=26, en=19,
                                    d4=13, d5=6, d6=5, d7=11,
                                    cols=16, lines=2)
             lcd.clear()
             lcd_1 = final_str + '\n' + str(v.parking_spot)
             lcd.message(lcd_1)
             #sleep(10)
             
             #SERVO MOTOR OPERATION
             GPIO.setmode(GPIO.BCM)
             # Set pin 11 as an output, and set servo1 as pin 11 as PWM
             GPIO.setup(17,GPIO.OUT)
             servo1 = GPIO.PWM(17,50) 
             servo1.start(0)
             print ("Waiting for 2 seconds")
             time.sleep(2)           #Plate recognition
             #90 degrees
             print ("Rotating 90 degrees")
             servo1.ChangeDutyCycle(7)
             time.sleep(5)
             
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
data = asarray(pl.Heap)
savetxt('data.csv', data, delimiter=',')
