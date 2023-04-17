import cv2
import mediapipe as mp
from FaceAnalyzer import FaceAnalyzer, Face
import pyautogui as pyg
from time import sleep

fa = FaceAnalyzer(1)
cap = cv2.VideoCapture(0)
threshold = 0.6
avgh = 0
avgNum = 3
lastVals = [0 for x in range(avgNum)]
counter = 0

scrollSens = 200

while True:
    success, image = cap.read()
    RGB_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    fa.process(RGB_image)

    if(fa.found_faces):
        if(counter >= avgNum):
            counter = 0

        Face.draw_eyes_landmarks(fa.faces[0], image)

        h = Face.get_right_eye_height(fa.faces[0])

        lastVals[counter] = h
        avgh = 0
        for x in lastVals:
            avgh += x
        avgh /= avgNum

        #print([avgh, h, avgh-h])

        if(avgh - h > threshold):
            pyg.scroll(-scrollSens)
            print("BLINK")

    cv2.imshow("Win", image)
    cv2.waitKey(1)

    if cv2.waitKey(1) == 27:
        exit()

    counter += 1