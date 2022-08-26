import cv2
import mediapipe as mp
import math
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))


cap = cv2.VideoCapture(0)
mpHands=mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils


while True:
    success,img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    #print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks :
        for handlms in results.multi_hand_landmarks:
            lmlist = []
            for id , lm in enumerate(handlms.landmark):
                #print(id,lm)
                h,w,c = img.shape
                cx , cy =int(lm.x*w) , int(lm.y*h)
                #print(id,cx,cy)
                lmlist.append([id,cx,cy])
            mpDraw.draw_landmarks(img,handlms, mpHands.HAND_CONNECTIONS)
            #print(lmlist)
        if lmlist :
            #print(lmlist[4])
            x1,y1=lmlist[4][1],lmlist[4][2]
            x2,y2=lmlist[8][1],lmlist[8][2]

            cv2.circle(img,(x1,y1),10,(230,250,9),cv2.FILLED)
            cv2.circle(img,(x2,y2),10,(230,250,9),cv2.FILLED)
            cv2.line(img,(x1,y1),(x2,y2),(230,30,30),2)
            length = math.hypot(x2-x1,y2-y1)
            #print(length)

            if length<10:   
                z1=(x1+x2)//2
                z2=(y1+y2)//2
                cv2.circle(img,(z1,z2),10,(230,30,9),cv2.FILLED)
            
        volumerange=volume.GetVolumeRange()
        minVol= volumerange[0]
        maxVol= volumerange[1]
        vol=np.interp(length,[10,120],[minVol,maxVol])
        volumebar = np.interp(length,[10,120],[400,140])
        volumepercent = np.interp(length,[10,120],[0,100])

        #print(int(vol))
        volume.SetMasterVolumeLevel(vol, None)
        cv2.rectangle(img,(50,140),(85,400),(0,223,23),3)
        cv2.rectangle(img,(50,int(volumebar)),(85,400),(255,253,253),cv2.FILLED)
        cv2.putText(img,str(int(volumepercent)),(30,480),cv2.FONT_HERSHEY_COMPLEX_SMALL,3,(255,253,253),3)



    cv2.imshow("Image", img) 
    cv2.waitKey(1)