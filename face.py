import cv2
import mediapipe as mp
from FaceAnalyzer import FaceAnalyzer, Face
from pyautogui import scroll
from time import sleep

fa = FaceAnalyzer(1)
cap = cv2.VideoCapture(0)

while True:
    success, image = cap.read()
    RGB_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    fa.process(RGB_image)

    if(fa.found_faces):
        pass

    cv2.imshow("Win", image)

    cv2.waitKey(1)
    if cv2.waitKey(1) == 27:
        exit()