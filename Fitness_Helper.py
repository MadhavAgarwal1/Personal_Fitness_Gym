
import cv2
# import mediapipe as mp 
import time
import pose_Detector as pD
import math
import numpy as np

cap = cv2.VideoCapture(0)
detector = pD.poseDetector()       #creating object
pTime = 0
flag1 = 0      
flag2 = 0     
count1 = 0 
count2 = 0 


while True:  
    success, img = cap.read()
    # img = cv2.resize(img, (640, 480))
    # img = cv2.resize(img, (1280, 720))
    img = detector.findPerson(img, False)        #calling method 
    lmList = detector.findPosition(img, False)
    # print("32 LandMarks list: ",lmList)
    if lmList != None and len(lmList) !=0 :
        rightHand = detector.findAngle(img, 12,14,16)     
        leftHand = detector.findAngle(img, 11,13,15)

        # leftLeg = detector.findAngle(img, 23,25,27)
        # rightLeg = detector.findAngle(img, 24,26,28)
    
        perCent1 = np.interp(rightHand, (25,165),(100,0))       # (changable value, changeable val btw this, convert_in_this_range)
        perCent2 = np.interp(leftHand, (25,165),(100,0))     
        
#left
        colorCode1 = (77, 255, 147)      # this is in BGR since openCV uses BGR format
        if perCent1 == 100:
            colorCode1 = (0, 255, 0)
            if flag1 == 0:
                count1 += 0.5
                flag1 = 1
        if perCent1 == 0:
            if flag1 == 1:
                count1 += 0.5
                flag1 = 0
        # print(count)

#right
        colorCode2 = (77, 255, 147)      # this is in BGR since openCV uses BGR format
        if perCent2 == 100:
            colorCode2 = (0, 255, 0)
            if flag2 == 0:
                count2 += 0.5
                flag2 = 1
        if perCent2 == 0:
            if flag2 == 1:
                count2 += 0.5
                flag2 = 0
        # print(count)
        
    #bar
    bar1 = np.interp(rightHand, (25,165),(110, img.shape[1]-240)) 
    bar2 = np.interp(leftHand, (25,165),(110, img.shape[1]-240)) 
    # print(bar)
    #right side 
    cv2.rectangle(img, (img.shape[0]+140, 110), (img.shape[0]+110, img.shape[1]-240), colorCode2, 3)
    cv2.rectangle(img, (img.shape[0]+140, int(bar2)), (img.shape[0]+110, img.shape[1]-240), colorCode2, cv2.FILLED)
    cv2.putText(img, f"{str(int(perCent2))}%", (img.shape[0]+100,90), cv2.FONT_HERSHEY_PLAIN, 2, colorCode2, 2) 
    cv2.putText(img, f"Count:{str(int(count2))}", (img.shape[1]-140,50), cv2.FONT_ITALIC, 1, (0,255,0), 2)  
    #left side 
    cv2.rectangle(img, (15, 110), (45, img.shape[1]-240), colorCode1, 3)
    cv2.rectangle(img, (15, int(bar1)), (45, img.shape[1]-240), colorCode1, cv2.FILLED)
    cv2.putText(img, f"{str(int(perCent1))}%", (15,90), cv2.FONT_HERSHEY_PLAIN, 2, colorCode1, 2)
    cv2.putText(img, f"Count:{str(int(count1))}", (10,50), cv2.FONT_ITALIC, 1, (0,255,0), 2)  

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    # to show FPS(frame per second) 
    cv2.putText(img, f"FPS:{str(int(fps))}", (int((img.shape[1])/2 - 20),90), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,0), 3)  
    cv2.imshow("Image Name", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break   
cv2.destroyAllWindows()
