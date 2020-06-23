#!/usr/bin/env python
import sys
import cv2
import time
import rospy
from cospace2ros.msg import cospace_state

'''
# check it -> https://github.com/eric-wieser/ros_numpy
- the numpy thingy it needs it to be uint8 maybe try just an int8?
- Test it with a moving video 
- Write a tool that views frames from this msg type
- delete winCrescue.webm on shutdown
- Also why the FUCK is the shutdown Routine Garbage?
'''
#all the vars explained:http://cospacerobot.org/documents/CSR-Rescue%202016%20Help%20(Secondary)/index.html#!advancedConditions
"""
all vars should look like this:

clock=146;Duration=0;SuperDuration=0;bGameEnd=0;CurAction=-1;CurGame=0;SuperObj_Num=0;SuperObj_X=0;SuperObj_Y=0;
Teleport=0;LoadedObjects=0;US_Front=96;US_Left=38;US_Right=131;CSLeft_R=233;CSLeft_G=246;CSLeft_B=255;CSRight_R=204;
CSRight_G=217;CSRight_B=255;PositionX=0;PositionY=0;TM_State=1;Compass=0;Time=50;WheelLeft=2;WheelRight=2;LED_1=0;MyState=0;"""

def read_and_pub_vars(comms_dir,vcap,cospace_state_pub):
    try:
        f=open(comms_dir+"allvars.txt","r")
    except:
        rospy.logfatal("Couldn't open {0}allvars.txt for reading check comms_dir param".format(comms_dir))
        sys.exit(1)
    allvars=f.read()
    f.close()
    try:
        state_dict={i.split("=")[0].replace("\n",""):int(i.split("=")[1]) for i in allvars.split(";") if len(i.split("="))==2}
    except:
        rospy.logfatal("Couldn't parse {0}allvars.txt check it's in the format in cospace2ros/state_pub.py")
    
    ret,frame=vcap.read()
    if ret:
        state_dict["frame"]=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    else:
        rospy.logerr("Couldn't Capture frame at timestamp {0}".format(rospy.Time.now()))
    try:
        publish_current_state(state_dict,cospace_state_pub) #pass the publisher object as an argument

    except KeyError:
        rospy.logerr("Passed Publishing cospace_state at timestamp {0} ".format(rospy.Time().now()))


def publish_current_state(state_dict,cospace_state_pub):
    state=cospace_state()
    
    state.clock=state_dict["clock"]
    state.Duration=state_dict["Duration"]
    state.SuperDuration=state_dict["SuperDuration"]
    state.bGameEnd=state_dict["bGameEnd"]
    state.CurAction=state_dict["CurAction"]
    state.CurGame=state_dict["CurGame"]
    
    state.SuperObj_Num=state_dict["SuperObj_Num"]
    state.SuperObj_X=state_dict["SuperObj_X"]
    state.SuperObj_Y=state_dict["SuperObj_Y"]
    
    state.Teleport=state_dict["Teleport"]
    state.LoadedObjects=state_dict["LoadedObjects"]
    
    state.US_Front=state_dict["US_Front"]
    state.US_Left=state_dict["US_Left"]
    state.US_Right=state_dict["US_Right"]
    
    state.CSLeft_R=state_dict["CSLeft_R"]
    state.CSLeft_G=state_dict["CSLeft_G"]
    state.CSLeft_B=state_dict["CSLeft_B"]
    
    state.CSRight_R=state_dict["CSRight_R"]
    state.CSRight_G=state_dict["CSRight_G"]
    state.CSRight_B=state_dict["CSRight_B"]
    
    state.PositionX=state_dict["PositionX"]
    state.PositionY=state_dict["PositionY"]
    state.TM_State=state_dict["TM_State"]
    state.Compass=state_dict["Compass"]
    
    state.Time=state_dict["Time"]

    state.WheelLeft=state_dict["WheelLeft"]
    state.WheelRight=state_dict["WheelRight"]
    state.LED_1=state_dict["LED_1"]
    state.MyState=state_dict["MyState"]
    try:
        state.frame=state_dict["frame"]#).astype(np.uint8)
        #print(state_dict["frame"])
    except KeyError:
        pass
    cospace_state_pub.publish(state)
