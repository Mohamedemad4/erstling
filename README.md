# Erstling: Solving Cospace Rescue with ROS and computer vision 

## Why is it called Erstling?
Based on the [FuG 25a Erstling](https://en.wikipedia.org/wiki/FuG_25a_Erstling) [Friend or Foe Detection Radar System](https://en.wikipedia.org/wiki/Identification_friend_or_foe) 
the system was brilliant but over engineerd. and this is sort of the theme of this project 
Solving a trivial Game meant to teach kids programming with cutting edge robotics techniques and tools

## Reading Material 
- [Rulebook](https://junior.robocup.org/wp-content/uploads/2019Rules/2019_RescueSimulation_Final.pdf)
- [all vars explained](http://cospacerobot.org/documents/CSR-Rescue%202016%20Help%20(Secondary)/index.html#!advancedConditions)

## Tasks!

- Odom_publisher
    - sub to /cospace_state and integerate over WheelSpeedLeft and WheelSpeedRight to figure out our position and orientation 
    - hint: use eular angles and compass then convert to quats. and pixels per second

- object_markers (take video from the arena and convert it to useful markers)
    - write the actual ROS Code
        - write the frame reading from cospace_state code
        - write the Marker Publisher code
        - Write the frame_viz Publisher code
    - check object_markers/notebooks/playground.ipynb for details about tasks and the actual Computer Vision Code

    - ## V2 (better score)
        - detect super objects
        - detect swaps
        - detect speical zones

- Nav Package 
    - Must be able to teleport 
        - when to teleport? idk read the rules
    - use the CS to pick points
        - and do the dance in 
    - use US to avoid obsticals 

## Installation
- install WSL 1 on your windows machine
- install MS robotics dev studio 4
- install cospace rescue
- download ffmpeg and unzip it in a directory
- set that dir to ```ffmpeg_path in cospace2ros/launch/cospace_ctrl.launch```
- create a dir in your perfrred location and put it's location in ```comms_dir in cospace2ros/launch/cospace_ctrl.launch``
- change the locations of the files read and written to in ```cospace2ros/cospace_project_files/ai.c``` (lines:163 and 176) to ones that point to ```comms_dir```
- Upload the ai.c file to the Cospace Rescue Robot
- create a catkin_ws with the project files inside src dir. (not src/erstling/cospace2ros, but src/cospace2ros)
- copy the .git dir from erstling repo into the src dir in the catkin_ws (makes working and tracking changes easier)
- run ```catkin_make .``` then ```catkin_make install```
- ```roslaunch catkin_ws/src/erstling/launch/nuke.launch``` (Todo)

## Troubleshooting / Notes
- if the Entire **cospace program quits** after starting the game that means that ai.c can't read/write the control files 
- thanks to https://github.com/aler9/rtsp-simple-server for stream-server