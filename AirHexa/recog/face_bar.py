import cv2
import numpy as np 
import sqlite3
import os
from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
import imutils
import time

#FACE_START
name=""
text=""
conf=100
conn = sqlite3.connect('database.db')
c = conn.cursor()
fname = "recognizer/trainingData.yml"
if not os.path.isfile(fname):
  print("Please train the data first")
  exit(0)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(2)
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read(fname)
while True:
	ret, img = cap.read()
	cv2.putText(img, 'AIRHEXA(JATAYU)', (0,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),2)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	for (x,y,w,h) in faces:
		cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)
		ids,conf = recognizer.predict(gray[y:y+h,x:x+w])
		c.execute("select name from users where id = (?);", (ids,))
		result = c.fetchall()
		name = result[0][0]
		if conf < 50:
			cv2.putText(img, name, (x+2,y+h-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (150,255,0),2)
			print(name)
			print(ids)
			cap.release()
			cv2.destroyAllWindows()
			#break

            #QR_CODE STARTS
        #    ap = argparse.ArgumentParser()
        #    ap.add_argument("-o", "--output", type=str, default="barcodes.csv",help="path to output CSV file containing barcodes")
        #    args = vars(ap.parse_args())
			vs=cv2.VideoCapture(2)
			print("Please show the QR Code")
			time.sleep(2.0)
        #    csv = open(args["output"], "w")
        #    found = set()
			while True:
				ret,frame =vs.read()
				
				frame=cv2.resize(frame,(800,600))
				cv2.putText(img, 'AIRHEXA(JATAYU)', (0,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),2)
				barcodes=pyzbar.decode(frame)
				for barcode in barcodes:
			
					(x, y, w, h) = barcode.rect
					cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
					barcodeData = barcode.data.decode("utf-8")
					barcodeType = barcode.type
					text = "{}".format(barcodeData)
					#cv2.putText(frame, text, (x, y - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
					if(text!=""):
						print(text)
						cv2.destroyAllWindows()
						vs.release()
						break
				
				cv2.imshow("Barcode Scanner", frame)
				if(text!=""):
					break
				#print(text)	
				key = cv2.waitKey(1) & 0xFF
				if key == ord("q"):
					break
			cv2.destroyAllWindows()
			vs.release()
			break
		
		else:
			cv2.putText(img, 'AIRHEXA(JATAYU)', (0,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),2)
	cv2.imshow('Face and QR Code Recognizer(AIRHEXA)',img)
	if conf<50:
		cap.release()
		cv2.destroyAllWindows()
		break
	k = cv2.waitKey(30) & 0xff
	if k == 27:
		break
a=str(ids)
b=str(text)
if(a==b):
	print("release the product")
else:
	print("Authentication failed!!")