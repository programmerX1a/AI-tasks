import cv2
import matplotlib.pyplot as plt
import numpy as np
import os
img=cv2.imread(os.path.abspath("balls\\balls\\ball_14.jpg"))
b,g,r=cv2.split(img)
brightness=0.299*r+0.587*g+0.114*b
for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        if brightness[i][j] <50:
            img[i][j]=np.clip(img[i][j]*1.1+[1,1,1],0,255)
        elif brightness[i][j]>190:
           img[i][j]=np.clip(img[i][j]*0.8+[-1,-1,-1],0,255)
hsv_img=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
lower_blue = np.array([95, 70, 40])
upper_blue = np.array([140, 255, 255])

lower_red_1 = np.array([0, 70, 40])
upper_red_1 = np.array([10, 255, 255])

lower_red_2 = np.array([170, 70, 40])
upper_red_2 = np.array([180, 255, 255])

red_mask=cv2.inRange(hsv_img,lower_red_1,upper_red_1) | cv2.inRange(hsv_img,lower_red_2,upper_red_2)
blue_mask=cv2.inRange(hsv_img,lower_blue,upper_blue)
img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
filtered_img_gray=cv2.GaussianBlur(img_gray,(13,13),0)
circles=cv2.HoughCircles(filtered_img_gray,cv2.HOUGH_GRADIENT,1,70,param1=100,param2=30,minRadius=30,maxRadius=500)
red=0
blue=0
img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

if circles is not None:
    circles=np.uint16(np.around(circles))
    for i in circles[0]:
        try:         
            red_count=0
            blue_count=0
            for j in range(i[1]-i[2],i[1]+i[2]):
                for k in range(i[0]-i[2],i[0]+i[2]):
                    if red_mask[j][k]>0:
                        red_count+=1
                    if blue_mask[j][k]>0:
                        blue_count+=1
            if red_count>=(3.14*i[2]**2)/2:
                red+=1
                cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),5)
            elif blue_count>=(3.14*i[2]**2)/2:
                blue+=1
                cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),5)

                
         
        except IndexError:
            continue

print(blue)
print(red)
plt.imshow(img)
