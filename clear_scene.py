# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 10:56:45 2015

@author: ruben
"""
#from __future__ import division, print_function
import pysmac
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
									

def clear_scene(x1):
	""" benchmark run that sets parameters and generates a cost  """
	print("running once")

	scene_string = "scene_" + str(x1)

	object_publisher = rospy.Publisher('/collision_object',
			moveit_msgs.msg._CollisionObject.CollisionObject,
			queue_size=100)
			
	group = moveit_commander.MoveGroupCommander('manipulator')	
			
	scene = moveit_commander.PlanningSceneInterface()

	rospy.sleep(0.2)

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
			f.readline()
			f.readline()
			f.readline()
			f.readline()

			print name
			
			env_names.append(name)   #adding name to list in order to clear later	

	
	rospy.sleep(0.2)
	for x in xrange(len(env_names)):			
		scene.remove_world_object(env_names[x])
	env_names = []


if __name__ == "__main__":
	""" The main, init roscpp and rospy, construct class and launch benchmark """

	moveit_commander.roscpp_initialize(sys.argv)
	rospy.init_node('Benchmark_node', anonymous=True)

	clear_scene(sys.argv[1])

	moveit_commander.roscpp_shutdown()