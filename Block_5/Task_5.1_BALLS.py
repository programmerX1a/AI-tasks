import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

for ball in range(1,21):
    plt.figure()
    keys=["class_id","x_center","y_center","width","height"]
    df=pd.DataFrame(columns=keys)
    img=cv2.imread(os.path.abspath(f"balls\\balls\\ball_{ball}.jpg"))
    img=cv2.convertScaleAbs(img,alpha=1.3,beta=30)
    hsv_img=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    plt.imshow(cv2.cvtColor(hsv_img,cv2.COLOR_HSV2RGB))
    lower_blue = np.array([90, 70, 90])
    upper_blue = np.array([135, 255, 255])

    lower_red_1 = np.array([0, 50, 150])
    upper_red_1 = np.array([10, 255, 255])

    lower_red_2 = np.array([170, 50, 150])
    upper_red_2 = np.array([180, 255, 255])


    blue_mask_c=cv2.inRange(hsv_img,lower_blue,upper_blue)
    blue_mask = cv2.bitwise_and(img, img, mask=blue_mask_c)
    blue_mask_gr=cv2.cvtColor(blue_mask,cv2.COLOR_BGR2GRAY)
    blue_mask_gr=cv2.medianBlur(blue_mask_gr,17)
    blue_mask_gr=cv2.GaussianBlur(blue_mask_gr,(17,17),0)
    blue_mask = cv2.morphologyEx(blue_mask,cv2.MORPH_OPEN,np.ones((17,17),np.uint8))



    red_mask_c=cv2.inRange(hsv_img,lower_red_1,upper_red_1) | cv2.inRange(hsv_img,lower_red_2,upper_red_2)
    red_mask=cv2.bitwise_and(img,img,mask=red_mask_c)
    red_mask_gr=cv2.cvtColor(red_mask,cv2.COLOR_BGR2GRAY)
    red_mask_gr=cv2.medianBlur(red_mask_gr,17)
    red_mask_gr=cv2.GaussianBlur(red_mask_gr,(17,17),0)

    red_mask = cv2.morphologyEx(red_mask,cv2.MORPH_OPEN,np.ones((15,15),np.uint8))
    red_mask = cv2.morphologyEx(red_mask,cv2.MORPH_CLOSE,np.ones((7,7),np.uint8))

    img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    circles=cv2.HoughCircles(red_mask_gr,cv2.HOUGH_GRADIENT,1,1200,param1=90,param2=10,minRadius=10,maxRadius=700)
    if circles is not None:
        circles=np.uint16(np.around(circles))
        for i in circles[0]:
            circle_detector=np.zeros((img.shape[0],img.shape[1]),dtype=np.uint16)
            cv2.circle(circle_detector,(i[0],i[1]),i[2],255,-1)
            pixels=cv2.countNonZero(circle_detector & red_mask_c)
            area=cv2.countNonZero(circle_detector)
            if pixels>(area)*0.3:
                cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),8)
                new_row=pd.DataFrame([[1,i[0],i[1],i[2]*2,i[2]*2]],columns=keys)
                df=pd.concat([df,new_row])
            

    circles2=cv2.HoughCircles(blue_mask_gr,cv2.HOUGH_GRADIENT,1,1200,param1=80,param2=20,minRadius=10,maxRadius=700)
    if circles2 is not None:
        circles2=np.uint16(np.around(circles2))
        for i in circles2[0]:
            circle_detector=np.zeros((img.shape[0],img.shape[1]),dtype=np.uint8)
            cv2.circle(circle_detector,(i[0],i[1]),i[2],255,-1)
            pixels=cv2.countNonZero(circle_detector & blue_mask_c)
            area=cv2.countNonZero(circle_detector)
            if pixels>area*0.4:
                cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),8)
                new_row=pd.DataFrame([[0,i[0],i[1],i[2]*2,i[2]*2]],columns=keys)
                df=pd.concat([df,new_row])

    df.to_string(f"balls_{ball}.txt",header=False,index=False)        
    plt.imshow(img)
    plt.title("Image")
    plt.figure()
    plt.imshow(red_mask_c)
    plt.title("Red mask")
    plt.figure()
    
    plt.imshow(blue_mask_c)
    plt.title("Blue mask")


#First step is to add contrast to the original image
#to better identify the balls in shadowy areas
#then the image is converted to hsv to filter the image with
#red/blue colors since we want blue/red balls then some filtering
#is applied to reduce noise then we use hough circles to determine all circles
#the parameters are loose because the balls formed in the grayscale image arent entirely circular
#then for each circle formed by hough circles we check if the pixels inside the hough circle 
#actually contains any of the pixels we filtered (30% of the area) 30% was chosen because in some cases
#the circles arent complete in the color mask