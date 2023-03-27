# as module

import cv2
import mediapipe as mp 
import time
import math

# we are creating class so that we can create object and able to have/use methods
class poseDetector():

    def __init__(self):

        self.mp_drawing_styles = mp.solutions.drawing_styles     
        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose()        #creating pose
       
    def findPerson(self, img, draw=False):

        # this img is in BGR therefore...we convert it into RGB
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        # print(self.results.pose_landmarks)

        if self.results.pose_landmarks:      # landmarks are there AND
            if draw:        
                # Draw pose landmarks on the image. (0 to 32 points are there)
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks,self.mpPose.POSE_CONNECTIONS, landmark_drawing_spec= self.mp_drawing_styles.get_default_pose_landmarks_style())  # (img, make all the points, connect all the points, make all the points color different)            
        # else:
        #     print('no body is shown...')

        return img

    def findPosition(self, img, draw=False):
        self.lmList = []        #landmark list
        if self.results.pose_landmarks:        #not none
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape     #height, width, no. of channels(here is 3(which are Red, Blue, Green))
                # print("img.shape",img.shape)
                # print(id, lm)          #lm-> landmark values are the ratio of images

                # to get actual pixel values of lm
                cx, cy = int(lm.x*w) , int(lm.y*h)
                self.lmList.append([id,cx,cy])      

                if draw:
                    #drawing circle at landmark points( just for checking)
                    cv2.circle(img, (cx, cy), 3, (255,0,0), cv2.FILLED)
                    # cv2.putText(img, str(id), (cx,cy), cv2.FONT_ITALIC, 1, (255,0,255), 2)        # printing landmark count on body  

            return self.lmList

    def findAngle(self, img, p1, p2, p3, draw= True, showAngle= False):

        # getting targeted landmarks x,y coordinates values
        p1_x, p1_y = self.lmList[p1][1:]        # OR lmList[p1][1], lmList[p1][2])
        p2_x, p2_y = self.lmList[p2][1:]
        p3_x, p3_y = self.lmList[p3][1:]
        
        #finding angle
        angle = math.degrees(math.atan2(p3_y - p2_y, p3_x - p2_x) - math.atan2(p1_y - p2_y, p1_x - p2_x))   # math.degrees() will convert radian value to degree
        
        angle = (angle + 180) % 360 - 180
        angle = abs(angle)
        
        # drawing and joining targeted points
        if draw:
            # drawing joining line btw 3 points
            cv2.line(img, (p1_x, p1_y), (p2_x, p2_y), (255,255,255), 3)
            cv2.line(img, (p2_x, p2_y), (p3_x, p3_y), (255,255,255), 3)
            #highlighting 3 points
            cv2.circle(img, (p1_x,p1_y), 8, (0,0,255), cv2.FILLED)
            cv2.circle(img, (p1_x,p1_y), 12, (0,0,255), 2)
            cv2.circle(img, (p2_x,p2_y), 8, (0,0,255), cv2.FILLED)
            cv2.circle(img, (p2_x,p2_y), 12, (255,0,0), 2)
            cv2.circle(img, (p3_x,p3_y), 8, (0,0,255), cv2.FILLED)
            cv2.circle(img, (p3_x,p3_y), 12, (0,0,255), 2)

        if showAngle:
            cv2.putText(img, str(int(angle)), (p2_x+5, p2_y+5), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,0), 2)  

        return angle
    