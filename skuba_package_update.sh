#!/bin/bash
repos[0]="athome_msgs"
repos[1]="athome_navigation"
repos[2]="camera_pose"
repos[3]="door_detection"
repos[4]="dynamixel_motor"
repos[5]="faces"
repos[6]="gesture_detection"
repos[7]="hardware_bridge"
repos[8]="main_state"
repos[10]="manipulator"
repos[11]="object_perception"
repos[12]="people_detection"
repos[13]="speech_processing"

prefix="robocupssl.cpe.ku.ac.th/hg/skuba_athome/"
for repo in ${repos[@]}
do
	echo "pulling from http://"$prefix$repo
	auth_user=earth:htrae
	link="http://"$auth_user"@"$prefix$repo
	dir=$(rospack find $repo)
	echo $dir
	hg pull -u -R $dir $link
	hg update

done