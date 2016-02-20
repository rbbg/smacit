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
									
def bm_run_cost(planner_type,configMap):
	""" benchmark run that sets parameters and generates a cost  """

	planner_name = "SMAC"

	rospy.set_param("/move_group/planner_configs/" + planner_name + "/type",
		planner_type)
			
	group = moveit_commander.MoveGroupCommander('manipulator')
	
	robot = moveit_commander.RobotCommander()
	rospy.sleep(0.2)

	planning_frame = group.get_planning_frame() 

	group.set_planning_time(3)
	group.set_planner_id(planner_name)
	
	base_string = "/move_group/planner_configs/"+ planner_name +"/"
	for name, value in configMap.items():
		rospy.set_param(base_string+name,float(value))				
	
	states = [[1.2119047900726956, -1.0789121808903783, 1.7089048559038458,
	 		-1.2580455469851477, -0.5853913290905349, 2.1585251655353033], 
	 		[-1.0809913028897857, -1.2672336893382499, -0.8308119476540057,
	 		 -1.8211554831620005, 2.6605030443567, -2.244767596407182],
	 		[-0.3213221270871598, -0.7064710071721609, 1.16905227652397,
	 		 -0.8275752604135796, -1.9994209399472982, 1.4569111290179193], 
	 		[-1.6430097177151217, -1.7009085861670843, -1.9497761699343577, 
	 		 2.7055998875277325, 0.11668101664456862, 2.2915025755006893], 
	 		[-2.828711205610591, -2.884992362653886, -0.5500342441045457,
	 		 -0.6611208594724118, 2.404477588566261, -0.8306490600328073]]

	result = 0		   		            
	for x2 in xrange(5):
		start = states[x2]
		for x3 in range (x2+1, 5):         #loops to decide start and goal states
			goal = states[x3]                            										
			query = {"start":start, "goal":goal}        #create query dict										
			for it in range (0, 1):						
				start_state = robot.get_current_state()
				start_state.joint_state.position = start				
				group.set_start_state(start_state)
				group.set_joint_value_target(goal)     #takes a list as input
				start_time = time.time()                # *1000 to get millisecond
				planned_path = group.plan()
				result += (time.time()-start_time)					
	return(result)

if __name__ == "__main__":
	""" The main, init roscpp and rospy, construct class and launch benchmark """

	moveit_commander.roscpp_initialize(sys.argv)
	rospy.init_node('Benchmark_node', anonymous=True)

	# Read in first arguments.
	planner_type = sys.argv[1]

	instance = sys.argv[2]
	specifics = sys.argv[3]
	cutoff = int(float(sys.argv[4]) + 1)
	runlength = int(sys.argv[5])
	seed = int(sys.argv[6])
	 
	# Read in parameter setting and build a dictionary mapping param_name to param_value.
	params = sys.argv[7:]
	configMap = dict((name[1:], value) for name, value in zip(params[::2], params[1::2]))

	quality = bm_run_cost(planner_type, configMap)

	print("Result for SMAC: SUCCESS, " + str(quality) + ", 0, 0, 0")

	moveit_commander.roscpp_shutdown()