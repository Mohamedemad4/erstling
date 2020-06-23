#!/usr/bin/env python
import os
import sys
import cv2
import rospy
from geometry_msgs.msg import Twist
from state_pub import read_and_pub_vars
from cospace2ros.msg import cospace_state
from session_pool_man import session_pool

max_lin_spd = .22 #arbitrary in m/s
max_ang_spd = 2.84 #arbitrary in r/s
max_whl_spd = 5


rospy.init_node('cospace2Ros', anonymous=True,log_level=rospy.WARN)

comms_dir=rospy.get_param("comms_dir",None)
ffmpeg_path=rospy.get_param("ffmpeg_path","ffmpeg.exe") #assume it's globally installed if it ain't
rtsp_server=rospy.get_param("rtsp_server",None)

cospace_state_pub = rospy.Publisher('cospace_state', cospace_state, queue_size=1)

sess_pool=session_pool()
state_pub_rate=rospy.Rate(15)

def _send_control(whl_left=0,whl_right=0,LED=0,state=0,Teleport=0):
    try:
       f=open(comms_dir+"control_vars.txt",'w')
    except:
        rospy.logfatal("Couldn't open {0}control_vars.txt for writing check comms_dir param".format(comms_dir))
        sys.exit(1)
    f.seek(0)
    f.write("WheelLeft={0};WheelRight={1};LED_1={2};MyState={3};Teleport={4};".format(int(whl_left),int(whl_right),LED,state,Teleport)) #force whl_left and whl_right to be int not floats
    f.truncate()
    f.close()

def angz_to_spd(spd):
    return trim_spd(translate(abs(spd),0,max_ang_spd,0,max_whl_spd))

def linx_to_spd(spd):
    return trim_spd(translate(abs(spd),0,max_lin_spd,0,max_whl_spd))

def trim_spd(spd):
    if spd>max_whl_spd: # when the cmd_vel.x_lin is > max_lin_spd the spd is more than max_whl_spd
        return max_whl_spd
    return spd

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    # https://stackoverflow.com/questions/1969240/
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

def twist_callback(twist):
    angz=twist.angular.z
    linx=twist.linear.x
    #set a priority for angular cmds
    if angz!=0:

        spd=angz_to_spd(angz)
        if angz>0:
            rospy.logdebug("angz is postive,heading right")
            _send_control(whl_left=-spd,whl_right=spd)
        if angz<0:
            rospy.logdebug("angz is negative,heading left")
            _send_control(whl_left=spd,whl_right=-spd)

    if linx!=0:

        spd=linx_to_spd(linx)
        if linx>0:
            rospy.logdebug("linx if postive ,heading forward")
            _send_control(whl_left=spd,whl_right=spd)
        else:
            rospy.logdebug("linx is negative")
            _send_control(whl_left=-spd,whl_right=-spd)

    if linx==0 and angz==0:
        _send_control(whl_left=0,whl_right=0)
    return

def start_ffmpeg_stream():
    sess_pool.run_session_process(rtsp_server)
    rospy.sleep(3) # give stream-server some time to start    
    sess_pool.run_session_process('{ff_path} -f gdigrab -i title="Microsoft Visual Simulation Environment 4" -f rtsp -b:v 800k -r 24 -framerate 10 -codec:a mp2 -b:a 128k -muxdelay 0.001 rtsp://localhost:8554/stream'.format(
        ff_path=ffmpeg_path
    ))
    rospy.sleep(2) # give ffmpeg some time to spin up and spit the video file


def shutdown():
    print("Byee")
    _send_control(whl_left=0,whl_right=0)
    sess_pool.kill_session_process('{ff_path} -f gdigrab -i title="Microsoft Visual Simulation Environment 4" -f rtsp -b:v 800k -r 24 -framerate 10 -codec:a mp2 -b:a 128k -muxdelay 0.001 rtsp://localhost:8554/stream'.format(
        ff_path=ffmpeg_path
    ))
    sess_pool.kill_session_process(rtsp_server)
    exit(0)
    return

if __name__=="__main__":
    rospy.loginfo("Using {0} as comms_dir".format(comms_dir))
    rospy.loginfo("Subscribing to cmd_vel")
    rospy.Subscriber("cmd_vel", Twist, twist_callback,queue_size=1)
    rospy.on_shutdown(shutdown)
    start_ffmpeg_stream()
    vcap=cv2.VideoCapture("rtsp://localhost:8554/stream")

    open(comms_dir+"allvars.txt","wb+").write("""clock=146;Duration=0;SuperDuration=0;bGameEnd=0;CurAction=-1;CurGame=0;SuperObj_Num=0;SuperObj_X=0;SuperObj_Y=0;
Teleport=0;LoadedObjects=0;US_Front=96;US_Left=38;US_Right=131;CSLeft_R=233;CSLeft_G=246;CSLeft_B=255;CSRight_R=204;
CSRight_G=217;CSRight_B=255;PositionX=0;PositionY=0;TM_State=1;Compass=0;Time=50;WheelLeft=2;WheelRight=2;LED_1=0;MyState=0;""")
    rospy.loginfo("Started Video cap")
    rospy.loginfo("Started State Publisher")
    while True:
            read_and_pub_vars(comms_dir,vcap,cospace_state_pub)
            state_pub_rate.sleep() #cap it at 15hz
