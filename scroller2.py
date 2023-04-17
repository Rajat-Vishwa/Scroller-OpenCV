import cv2
import mediapipe as mp
from FaceAnalyzer import FaceAnalyzer, Face
from pyautogui import scroll
from time import sleep

fa = FaceAnalyzer(1)
cap = cv2.VideoCapture(0)

threshold = 20
distThreshold = 0.05
avgh = 0
avgNum = 5
lastVals = [0 for x in range(avgNum)]
counter = 0
prevVal = 0

maxTimer = 25
timer = 0

scrollSens = 280

while True:
    success, image = cap.read()
    RGB_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    fa.process(RGB_image)

    if(fa.found_faces):
        if(counter >= avgNum):
            counter = 0

        Face.draw_bounding_box(fa.faces[0], image)

        #h = Face.get_right_eye_height(fa.faces[0])

        res = Face.get_realigned_landmarks_pos(fa.faces[0])[Face.nose_tip_index]
        Face.draw_landmark_by_index(fa.faces[0], image, Face.nose_tip_index)

        h = res[1]

        lastVals[counter] = h
        avgh = 0
        for x in lastVals:
            avgh += x
        avgh /= avgNum

        dist = abs(res[2])
        threshold = dist * distThreshold

        #print([h, avgh, h - avgh, threshold])
        
        if(h - avgh > threshold and timer == 0):
            scroll(-scrollSens)
            print("Scroll Down!")
            timer = maxTimer
        elif(h - avgh < -threshold and timer == 0):
            scroll(scrollSens)
            print("Scroll Up")
            timer = maxTimer

    cv2.imshow("Win", image)
    cv2.waitKey(1)

    if cv2.waitKey(1) == 27:
        exit()

    counter += 1
    if(timer > 0):
        timer -= 1
    sleep(0.005)