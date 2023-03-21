import cv2
import mediapipe as mp 
import time
import math

# we are creating class so that we can create object and able to have/use methods
class poseDetector():

    def __init__(self):
    # def __init__(self, mode=False, complexity=1, smoothLm=True, enableSeg=False, smoothSeg=True, detectionCon=0.5, trackCon=0.5):
    #     self.mode=mode
    #     self.complexity=complexity
    #     self.smoothLm=smoothLm
    #     self.enableSeg=enableSeg
    #     self.smoothSeg=smoothSeg
    #     self.detectionCon=detectionCon
    #     self.trackCon=trackCon

        self.mp_drawing_styles = mp.solutions.drawing_styles     
        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose()        #creating pose
        # self.pose = self.mpPose.Pose(self.mode, self.complexity, self.smoothLm, self.enableSeg, self.smoothSeg, self.detectionCon, self.trackCon)        #creating pose

    def findPerson(self, img, draw=False):

        # this img is in BGR and mediapipe uses RGB therefore...we convert it into RGB
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        # print(results.pose_landmarks)

        if self.results.pose_landmarks:      # landmarks are there AND
            if draw:         # if landmarks to be drawn 
                
                # Draw pose landmarks on the image. (0 to 32 points are there)

                # self.mpDraw.draw_landmarks(img, self.results.pose_landmarks)  # it make all the points
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks,self.mpPose.POSE_CONNECTIONS)  # it connect all the points
                # self.mpDraw.draw_landmarks(img, self.results.pose_landmarks,self.mpPose.POSE_CONNECTIONS, landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())  # it make all the points color different
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
                self.lmList.append([id,cx,cy])      # we can also append z value | visiblity value...but for now we do not need it.

                if draw:
                    #drawing circle at landmark points( just for checking)
                    cv2.circle(img, (cx, cy), 3, (255,0,0), cv2.FILLED)
                    # cv2.putText(img, str(id), (cx,cy), cv2.FONT_ITALIC, 1, (255,0,255), 2)        # printing landmark count on body  

            return self.lmList

    def findAngle(self, img, p1, p2, p3, draw= True, showAngle= False):

        # getting targeted landmarks x,y values
        p1_x, p1_y = self.lmList[p1][1:]        # OR lmList[p1][1], lmList[p1][2])
        p2_x, p2_y = self.lmList[p2][1:]
        p3_x, p3_y = self.lmList[p3][1:]
        
        #finding angle
        angle = math.degrees(math.atan2(p3_y - p2_y, p3_x - p2_x) - math.atan2(p1_y - p2_y, p1_x - p2_x))   # math.degrees() will convert given radian value to degree | atan( returns value in range -PI/2 to PI/2 radians. atan2() returns in range -PI to PI)
        # if angle < 0:
        #     angle += 360
        angle = (angle + 180) % 360 - 180
        angle = abs(angle)
        # if angle < 0:
        #     angle = abs(angle)
        # if angle > 180:
        #     angle -= 180
        # print(angle)

        
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
            #put angle value
            # I think both work fine...for showing angle
            cv2.putText(img, str(int(angle)), (p2_x+5, p2_y+5), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,0), 2)  
            # cv2.putText(img, str(int(abs(angle))), (p2_x+5, p2_y+5), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,0), 2)   #adding 360 if -ve value 

        return angle
    
    
# to make it a module we write like below...
def main():
    cap = cv2.VideoCapture(0)
    pTime = 0
    detector = poseDetector()       #creating object

    while True:     
        success, img = cap.read()

        img = detector.findPerson(img,True)        #calling method 
        lmList = detector.findPosition(img,True)     # since if we did not call findPerson method prior to this, then we can not access result attribute(variable)(...i think for this we can check in findPositio method if result is present then OK else call findPerson inside findPosition method)
        # print("32 LandMarks list: ",lmList)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        # put text in the frame 
        cv2.putText(img, str(int(fps)), (40,50), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)  

        cv2.imshow("Image Name", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cv2.destroyAllWindows()


#TO RUN THIS FILE UNCOMMENT BELOW LINE
# if __name__ == "__main__":
#     main()      # if we run this file then it will run this main function...else if we are calling another function...then it will not run the if part