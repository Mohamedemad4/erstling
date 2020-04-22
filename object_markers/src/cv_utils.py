import cv2
import numpy as np

def viz_box(src,cords,c):
    frame=src.copy()
    for i in cords:
        cv2.circle(frame,(i[0],i[1]), 5, c, -1)
    return frame    
    
def get_color(frame,up,low):
    """
    Return Image mask of selected color range
    params:
        frame: opencv color src image
        up: [R,G,B] upper bound
        low: [R,G,B] Lower bound
    """
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #even though it says BGR treat it like RBG [r,g,b]
    upp_blue_Hsv=cv2.cvtColor(np.uint8([[up]]),cv2.COLOR_BGR2HSV).reshape(3,)
    low_blue_Hsv=cv2.cvtColor(np.uint8([[low]]),cv2.COLOR_BGR2HSV).reshape(3,)
    low_blue_Hsv[1]=60 # sets saturation

    mask = cv2.inRange(hsv, low_blue_Hsv, upp_blue_Hsv)

    return mask

def image_coordinates_to_ros(x,y):
    '''convert opencv/numpy image cooridnate frame to ROS cord frame (0,0) is bottom left'''
    return

def isWithinRange(x,y,r):
    if (x-y)>r or (y-x) >r:
        return False
    return True

def get_box_cords(frame,boxines_tolrance=7,box_min_area=50):
    ''' Get cordinates of objects 
    
        params:
         frame: numpy mask image of the desired object (returned by get_color()[1])
         boxines_tolrance: how much of a diff between w and h before we discard it as a triangle 
         box_min_area: min area of box
    '''
    r_ar=[]
    im2, contours, hierarchy = cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    i=0

    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)
        if not isWithinRange(w,h,boxines_tolrance) or cv2.contourArea(cnt)<box_min_area:
                continue
 
        M = cv2.moments(cnt)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        r_ar.append([cX,cY])
            
        i+=1
    return r_ar

def cam_norm(frame,config):
    
    w=config["w"]
    h=config["h"]

    pts1 = np.float32([
        config["pt_tl"],
        config["pt_tr"],
        config["pt_bl"],
        config["pt_br"] 
    ])
    pts2 = np.float32([[0,0],[w,0],[0,h],[w,h]])
    
    M = cv2.getPerspectiveTransform(pts1,pts2)
    
    return cv2.warpPerspective(frame,M,(w,h))