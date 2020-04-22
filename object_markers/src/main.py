#!/usr/bin/env python

'''
- publish frame_viz
- make cospace2ros publish video in the msg
- make marker publisher
- Write the image_coordinates_to_ros function
- Write Docs in the colors.yaml file
- maybe put a score in yaml file?
'''

import yaml
import rospy
from cv_utils import *
from cospace2ros.msg import cospace_state
from pub_markers import 
rospy.init_node('object_markers', anonymous=True,log_level=rospy.WARN)


def get_viz_frame_and_cords(frame,frame_viz,config,c=(255,0,0)):
    mask=get_color(frame,config["up"],config["low"])
    obj_cords=get_box_cords(mask,config["box_tolrance"],config["box_min_area"])
    frame_viz=viz_box(frame_viz,cyan_obj_cordsc,c)
    return obj_cords,frame_viz

def video_callback(state):
    frame=cam_norm(state.frame,colors_config["norm_cam"])

    '''Detect Cyan Objects''' 
    cyan_obj_cords,frame_viz = get_viz_frame_and_cords(frame,frame,colors_config["cyan"])

    '''Detect Red Objects''' 
    red_obj_cords,frame_viz = get_viz_frame_and_cords(frame,frame_viz,colors_config["red"],c=(0,0,255))

    '''Detect Deposit''' 
    deposit_cords,frame_viz = get_viz_frame_and_cords(frame,frame_viz,colors_config["deposit"]))

    '''Detect Traps!'''
    trap_cords,frame_viz = get_viz_frame_and_cords(frame,frame_viz,colors_config["traps"]))

    
    return

def shutdown():
    print("Byee")
    exit(0)
    return

if __name__=="__main__":

    colors_config_file = rospy.get_param("config","/home/daruis1/repos/erstling/src/object_markers/config/colors.yaml")
    try:
        colors_config = yaml.load(open(colors_config_file,"r"))
    except:
        rospy.logfatal("Couldn't Parse/Read config from {0}".format(colors_config_file))
        rospy.logfatal("Check your YAML syntax.")

    rospy.loginfo("Subscribing to cospace_state")
    rospy.Subscriber("cospace_state", video_callback, twist_callback,queue_size=1)

    rospy.on_shutdown(shutdown)
    rospy.loginfo("Started Markers Publisher")
    rospy.spin()