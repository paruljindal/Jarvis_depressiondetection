from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils
from threading import Thread
import numpy as np
import playsound
import argparse
import imutils
import time
import dlib
import cv2
import imageio
#import visvis as vv

from gi.repository import Gdk
#from SimpleCV import Camera
import sys

def sound_alarm(path):
	playsound.playsound(path)

def eye_aspect_ratio(eye):
	# compute the euclidean distances between the two sets of
	# vertical eye landmarks (x, y)-coordinates
	A = dist.euclidean(eye[1], eye[5])
	B = dist.euclidean(eye[2], eye[4])

	# compute the euclidean distance between the horizontal
	# eye landmark (x, y)-coordinates
	C = dist.euclidean(eye[0], eye[3])

	# compute the eye aspect ratio
	ear = (A + B) / (2.0 * C)
	return ear


def main(path):
	args = {}
	args["shape_predictor"] = "/home/rock19/Desktop/drowsiness-detection/shape_predictor_68_face_landmarks.dat"
	args["alarm"] = "/home/rock19/Desktop/drowsiness-detection/alarm.wav"
	 
	EYE_AR_THRESH = 0.26
	EYE_AR_CONSEC_FRAMES = 20
	
	earpre = 0
	ear = 0 
	count = 0 
	val = 0
	c = 0
	clock = 0 

	print("[INFO] loading facial landmark predictor...")
	detector = dlib.get_frontal_face_detector()
	predictor = dlib.shape_predictor(args["shape_predictor"])

	# grab the indexes of the facial landmarks for the left and
	# right eye, respectively
	(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
	(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

	# start the video stream thread
	print("[INFO] starting video stream thread...")
	  
	reader = imageio.get_reader(path)
	#t = vv.imshow(reader.get_next_data(), clim=(0, 255))

	#time.sleep(1.0)  # If you don't wait, the image will be dark

	i=1
	for frame in reader:

		frame = imutils.resize(frame, width=450)
		gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
			
		# detect faces in the grayscale frame
		rects = detector(gray, 0)

		for rect in rects:

			# determine the facial landmarks for the face region, then
			# convert the facial landmark (x, y)-coordinates to a NumPy
			# array
			shape = predictor(gray, rect)
			shape = face_utils.shape_to_np(shape)

			# extract the left and right eye coordinates, then use the
			# coordinates to compute the eye aspect ratio for both eyes
			leftEye = shape[lStart:lEnd]
			rightEye = shape[rStart:rEnd]
			leftEAR = eye_aspect_ratio(leftEye)
			rightEAR = eye_aspect_ratio(rightEye)

			# average the eye aspect ratio together for both eyes
			ear = (leftEAR + rightEAR) / 2.0

			# compute the convex hull for the left and right eye, then
			# visualize each of the eyes
			
			leftEyeHull = cv2.convexHull(leftEye)
			rightEyeHull = cv2.convexHull(rightEye)
			#cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
			#cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
			

			# check to see if the eye aspect ratio is below the blink
			# threshold, and if so, increment the blink frame counter

			if earpre - ear > 0.05 and c < i-1:
				print 'blink'
				val = max(val, i-clock )
				print val
				clock = i
				count += 1
				c = i

			earpre=ear

			# draw the computed eye aspect ratio on the frame to help
			# with debugging and setting the correct eye aspect ratio
			# thresholds and frame counters
			#cv2.putText(frame, "EAR: {:.2f}".format(ear), (10, 30),
			#	cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

		# show the frame
		#cv2.imshow("Frame", frame)
		#key = cv2.waitKey(1) & 0xFF
		i += 1

	#cv2.destroyAllWindows()
	if val == 0:
		val = i
	
	val = val/38

	if val <= 5:
		return 'Blink time: '+str(val)+'\nThis time indicates there is a strong likelihood that you may have dry eyes.\
				Dry eyes can be relieved though appropriate eye care drops and sprays.You should \
				consult your healthcare professional for diagnosis and to review possible relief options.'

	elif val <= 9:
		return 'Blink time: '+str(val)+'\nThis time indicates that you may have dry eyes linked to moisture evaporation.'

	elif val <= 15:
		return 'Blink time: '+str(val)+'\nBased on this time you may not have dry eyes,\
		 		particularly if you do not have any other eye symptoms.'

	else:
		return 'Blink time: '+str(val)+'\nYou have healthy eyes!!!!'
