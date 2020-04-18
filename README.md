# Erstling: Solving Cospace Rescue with ROS and computer vision 

## Why is it called Erstling?
Based on the [FuG 25a Erstling](https://en.wikipedia.org/wiki/FuG_25a_Erstling) [Friend or Foe Detection Radar System](https://en.wikipedia.org/wiki/Identification_friend_or_foe) 
the system was brilliant but over engineerd. and this is sort of the theme of this project 
Solving a trivial Game meant to teach kids programming with cutting edge robotics techniques and tools

## Reading Material 
- [Rulebook](https://junior.robocup.org/wp-content/uploads/2019Rules/2019_RescueSimulation_Final.pdf)
- [all vars explained](http://cospacerobot.org/documents/CSR-Rescue%202016%20Help%20(Secondary)/index.html#!advancedConditions)

## Tasks!

- Make cospace2ros Publish video from the vm

- Create a pkg that Published nav_msgs/odometery 
    - sub to /cospace_state and integerate over WheelSpeedLeft and WheelSpeedRight to figure out our position and orientation 
    - hint: use eular angles and compass then convert to quats. and pixels per second

- Create a pkg that captures Video from the Virtual Machine then outputs visualization_msgs/Marker postions of Objects,SuperObjs and Deposit Locations
    - check object_markers/notebooks/playground.ipynb for details about tasks
- Create a Nav Package that takes odom and visualization_msgs/Marker of objs and Navigates the map
    - Must be able to teleport 
        - when to teleport? idk read the rules
    - use the CS to pick points
        - and do the dance in 
    - use US to avoid obsticals 

## Installation
you are going to need both Linux and Windows running on the same machine for this to work
after setting up a win image in your preferred VM of choice.

- install MS robotics dev studio 4
- install cospace rescue
- create a shared directory between the VM and the host OS
- create 2 files in that shared directory allvars.txt and control_vars.txt. these files are used for communication between ROS and Cospace Rescue
    - they Should look like this:
    allvars.txt
    
    ``` 
    clock=257;Duration=0;SuperDuration=0;bGameEnd=0;CurAction=-1;CurGame=0;SuperObj_Num=0;SuperObj_X=0;SuperObj_Y=0;Teleport=0;LoadedObjects=0;US_Front=9;US_Left=19;US_Right=86;CSLeft_R=231;CSLeft_G=40;CSLeft_B=42;CSRight_R=204;CSRight_G=217;CSRight_B=255;PositionX=0;PositionY=0;TM_State=1;Compass=280;Time=132;WheelLeft=0;WheelRight=0;LED_1=0;MyState=0;
    ```

    control_vars.txt
    ```
    WheelLeft=0;WheelRight=0;LED_1=0;MyState=0;Teleport=0;
    ```

- change the locations of the files read and written to in ```cospace2ros/cospace_project_files/ai.c``` (lines:163 and 176)
- change ```comms_dir in cospace2ros/launch/cospace_ctrl.launch``` to the shared directory **Make sure to Remove the trailing Slash and make it a full path** 
- Upload the ai.c file to the Cospace Rescue Robot
- create a catkin_ws with the project files inside src dir. (not src/erstling/cospace2ros, but src/cospace2ros)
- copy the .git dir from erstling repo into the src dir in the catkin_ws (makes working and tracking changes easier)
- run ```catkin_make .``` then ```catkin_make install```
- ```roslaunch catkin_ws/src/erstling/launch/nuke.launch``` (Todo)

## Troubleshooting
- if the Entire **cospace program quits** after starting the game that means that ai.c can't read/write the control files 
