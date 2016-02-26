# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 10:56:45 2015

@author: ruben
"""
#from __future__ import division, print_function
import sys
import os
import time
import logging

import numpy
#import cPickle as pickle

import rospy
import moveit_commander
import moveit_msgs.msg
import moveit_msgs.srv
import geometry_msgs
import shape_msgs
import std_msgs
from datetime import datetime as dt

logging.basicConfig(level=logging.INFO)
									
def ld_scene(x1):
	""" benchmark run that sets parameters and generates a cost  """

	scene_string = "scene_" + str(x1)
	
	#Object Publishers, can alsu use PlanningSceneInterface, but this doesn throw any warnings
	
	object_publisher = rospy.Publisher('/collision_object',
			moveit_msgs.msg._CollisionObject.CollisionObject,
			queue_size=100)
			
	group = moveit_commander.MoveGroupCommander('manipulator')

	rospy.sleep(0.2)

	planning_frame = group.get_planning_frame()

	env_names = []

	with open("files/"+scene_string+".scene") as f:

		lines = 0   # get lines to know amount of blocks
		for line in f:
			lines += 1                
		f.seek(0)   # reset readfile location
		   
		title = f.readline()
		logging.info("loading scene:%s" % title)
		
		cnt = int((lines-2)/7)             # object data is 7 lines long, count amount of objects
		
		for objs in range (0, cnt):
			name = f.readline()[2:]   # object name
			number = f.readline()     # object number?
			shape = f.readline()      # object shape
			
			env_names.append(name)   #adding name to list in order to clear later
			
			#****** Parsing dimension ******#
			text = f.readline()
			dim = []
			for x in range (0, 3):          #3D dimension
				loc = text.find(" ")
				dim.append(float(text[:loc]))
				text = text[loc+1:]         #Remove used text
			
			#****** Parsing Location ******#
			text = f.readline()
			pos = []
			for x in range (0, 3):          #3D loc
				loc = text.find(" ")        
				pos.append(float(text[:loc]))
				text = text[loc+1:]
				
			#****** Parsing Rotation ******#
			text = f.readline()
			rot = []
			for x in range (0, 4):          #4D rotation
				loc = text.find(" ")
				rot.append(float(text[:loc]))
				text = text[loc+1:]
				
			#****** Parsing Colour ******#
			text = f.readline()
			col = []
			for x in range (0, 4):
				loc = text.find(" ")
				col.append(float(text[:loc]))
				text = text[loc+1:]
			# Currently unused, also not needed for adding objects
				
			
			#******* adding the object ********#
			object_shape = shape_msgs.msg._SolidPrimitive.SolidPrimitive()

			if (shape.rstrip() == "cylinder"):
				object_shape.type = object_shape.CYLINDER
				object_shape.dimensions.append(dim[1])
				object_shape.dimensions.append(dim[0])
			else:
				object_shape.type = object_shape.BOX #extend support for other primitives?
				object_shape.dimensions = dim
			
			object_pose = geometry_msgs.msg._Pose.Pose()
			object_pose.position.x = pos[0]
			object_pose.position.y = pos[1]
			object_pose.position.z = pos[2]
			
			object_pose.orientation.x = rot[0]
			object_pose.orientation.y = rot[1]
			object_pose.orientation.z = rot[2]
			object_pose.orientation.w = rot[3]
			
			Cobject = moveit_msgs.msg.CollisionObject()
			Cobject.id = name
			Cobject.header.frame_id = planning_frame
			Cobject.primitives.append(object_shape)
			Cobject.primitive_poses.append(object_pose)
			
			#assert type(Cobject) == moveit_msgs.msg.CollisionObject
			
			Cobject.header.stamp = rospy.Time.now()
			Cobject.operation = Cobject.ADD
			object_publisher.publish(Cobject)
			time.sleep(0.02)
			

if __name__ == "__main__":
	""" The main, init roscpp and rospy, construct class and launch benchmark """

	moveit_commander.roscpp_initialize(sys.argv)
	rospy.init_node('scene_loader', anonymous=True)

	ld_scene(sys.argv[1])

	moveit_commander.roscpp_shutdown()
