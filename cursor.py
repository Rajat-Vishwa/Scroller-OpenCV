import cv2
import mediapipe as mp
from FaceAnalyzer import FaceAnalyzer, Face
import pyautogui as pyg
from time import sleep
from numpy import interp
import os

screenWidth = 640
screenHeight = 480

fa = FaceAnalyzer(1)
cap = cv2.VideoCapture(0)

displayWidth = 1920
displayHeight = 1080

boundX = 2.6
boundY = 2.6

mouthOpeningThreshold = 18

avgNum = 10
lastVals = [100 for x in range(avgNum)]
counter = 0

while True:
    success, image = cap.read()
    RGB_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    fa.process(RGB_image)

    if(fa.found_faces):
        Face.draw_bounding_box(fa.faces[0], image)
        if(counter >= avgNum):
            counter = 0

        res = Face.get_realigned_landmarks_pos(fa.faces[0])
        Face.draw_landmark_by_index(fa.faces[0], image, Face.nose_tip_index)
        yawn = False

        nose = res[Face.nose_tip_index]
        x = nose[0]
        y = nose[1]

        xpos = interp(x, [screenWidth/boundX,screenWidth*(boundX-1)/boundX], [displayWidth, 0])
        ypos = interp(y, [screenHeight/boundY,screenHeight*(boundY-1)/boundY], [0, displayHeight])

        dist = res[Face.mouth_outer_indices[19]][2]
        upperLip = res[Face.mouth_outer_indices[19]][1]
        lowerLip = res[Face.mouth_outer_indices[5]][1]

        dist = abs(30+dist)
        diff = abs(lowerLip - upperLip)

        lastVals[counter] = diff
        avgh = 0
        for x in lastVals:
            avgh += x
        avgh /= avgNum

        #print([diff, mouthOpeningThreshold*dist])
        print([diff, avgh])


        if(diff > avgh * 1.3):
            yawn = True
        else:
            yawn = False

        #print(yawn)
        pyg.moveTo(xpos, ypos)

        if yawn:
            pyg.click()
        

    cv2.imshow("Win", image)
    cv2.waitKey(1)

    if cv2.waitKey(1) == 27:
        exit()
    counter += 1