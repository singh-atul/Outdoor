#!/usr/bin/env python

from __future__ import print_function

import roslib; 
import rospy
from sensor_msgs.msg import NavSatFix
from geometry_msgs.msg import Twist

import sys, select, termios, tty, os
import rospkg
import geonav_transform.geonav_conversions as gc

from move_base_msgs.msg import MoveBaseAction , MoveBaseGoal
import actionlib

file_path = "/waypoint_file/points_sim.txt"
rospack=rospkg.RosPack()
abs_path = rospack.get_path("mower")+file_path

def movebase_client(x,y):

	client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
	client.wait_for_server()

	goal = MoveBaseGoal()
	goal.target_pose.header.frame_id ="map"
	goal.target_pose.header.stamp = rospy.Time.now()
	goal.target_pose.pose.position.x = x
	goal.target_pose.pose.orientation.w = y

	client.send_goal(goal)
	wait= client.wait_for_result()
	if not wait:
		rospy.logerr("Action server not available!")
		rospy.signal_shutdown("Action server not available !")
	else:
		return client.get_result()


if __name__=="__main__":
	rospy.init_node('autonomous_twist')	
	points=[]
	# Read the files	
	if os.path.isfile(abs_path):
		with open(abs_path,'r') as f:
			points = f.readlines()

	print("Available number of manual points : ", len(points))

	#Convert point to UTM
	for point in points:
		if len(point) <10 :
			continue
		coo = point.split('    ')
		lat = float(coo[0].strip())
		lon = float(coo[1].strip())
		utmy , utmx , utmzone = gc.LLtoUTM(lat,lon)
		
	
		#Convert UTM to odom frame
		olat = 49.9
		olon = 8.90
		xg2 , yg2 = gc.ll2xy(lat,lon,olat,olon)

		#send as goal
		result = movebase_client(xg2,yg2)
		print ("Result " , result)
