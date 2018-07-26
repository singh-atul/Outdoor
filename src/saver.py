#!/usr/bin/env python
import roslib
import rospy
from sensor_msgs.msg import NavSatFix

def callback(data):
	#rospy.log_info("hum: ", data.data)
	print('@@@@')


def saver():
	rospy.init_node('saver',anonymous = True)
	rospy.Subscriber("/navsat/fix",NavSatFix,callback)
	rospy.spin()



if __name__ == '__main__':
	saver()
