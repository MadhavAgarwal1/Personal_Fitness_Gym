
import cv2
# import mediapipe as mp 
import time
import pose_Detector as pD
import math
import numpy as np

cap = cv2.VideoCapture(0)
detector = pD.poseDetector()       #creating object
pTime = 0
dir = 0     #direction 
count = 0 

while True:     
    # cap = cv2.VideoCapture('Pose_Estimation_Work/human_face.jpg')
    success, img = cap.read()
    # img = cv2.resize(img, (640, 480))
    # img = cv2.resize(img, (1280, 720))
    img = detector.findPerson(img, False)        #calling method 
    lmList = detector.findPosition(img, False)
    # print("32 LandMarks list: ",lmList)
    if lmList != None and len(lmList) !=0 :
        rightHand = detector.findAngle(img, 12,14,16)     
        leftHand = detector.findAngle(img, 11,13,15)
        #this 25,165 are by observing(for now considering dumble exercice and by sample running fetch its max and min)
        # perCent = np.interp(rightHand, (22,165),(0,100))       # (changable value, changeable val btw this, convert_in_this_range)
        perCent = np.interp(rightHand, (25,165),(100,0))       # (changable value, changeable val btw this, convert_in_this_range)
        # print(rightHand,perCent)

        colorCode = (77, 255, 147)      # this is in RGB since (OpenCV reads in images in BGR format (instead of RGB) because when OpenCV was first being developed, BGR color format was popular among camera manufacturers and image software providers.)
        if perCent == 100:
            colorCode = (0, 255, 0)
            if dir == 0:
                count += 0.5
                dir = 1
        if perCent == 0:
            if dir == 1:
                count += 0.5
                dir = 0
        # print(count)
        
    #bar
    bar = np.interp(rightHand, (25,165),(60, img.shape[1]-240))       # (changable value, changeable val btw this, convert_in_this_range)
    # print(bar)
    cv2.rectangle(img, (img.shape[0]+130, 60), (img.shape[0]+90, img.shape[1]-240), colorCode, 3)
    cv2.rectangle(img, (img.shape[0]+130, int(bar)), (img.shape[0]+90, img.shape[1]-240), colorCode, cv2.FILLED)
    cv2.putText(img, f"{str(int(perCent))}%", (img.shape[0]+75,40), cv2.FONT_HERSHEY_PLAIN, 2, colorCode, 3)  

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    # to show FPS(frame per second) 
    cv2.putText(img, f"FPS:{str(int(fps))}", (40,90), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,0), 3)  
    # to show counts completed 
    cv2.putText(img, f"Count:{str(int(count))}", (40,50), cv2.FONT_ITALIC, 1, (0,255,0), 3)  
    cv2.imshow("Image Name", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break   
cv2.destroyAllWindows()
