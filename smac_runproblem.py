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

import signal

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


class brc():								

	def __init__(self):
		self.done = False

	def bm_run_cost(self, problem_config, configMap):
		""" benchmark run that sets parameters and generates a cost  """

		planner_name = "SMAC"
		planning_timeout = 4
		failfactor = 1

		planner_type = problem_config[0]
		scene_number = problem_config[1]
		problem_iterations = int(problem_config[2])

		rospy.set_param("/move_group/planner_configs/" + planner_name + "/type",
			planner_type)
				
		group = moveit_commander.MoveGroupCommander('manipulator')
		
		robot = moveit_commander.RobotCommander()
		rospy.sleep(0.2)

		planning_frame = group.get_planning_frame()

		group.set_planning_time(planning_timeout)
		group.set_planner_id(planner_name)
		
		base_string = "/move_group/planner_configs/"+ planner_name +"/"
		for name, value in configMap.items():
			rospy.set_param(base_string+name,float(value))

		with open("files/scene_" + scene_number + ".states") as f:
			lines = 0   # get lines to know amount of states
			for line in f:
				lines += 1
			f.seek(0)   #reset readline
			
			states = [[0 for x in xrange(6)] for x in xrange(lines)] # 6 by Lines list for storing the states
			
			for num in range (0, lines):
				states[num] = eval(f.readline())

		result = 0		   		            
		for x2 in xrange(len(states)):
			start = states[x2]
			for x3 in xrange(len(states)):         #loops to decide start and goal states
				if (x2==x3): break              #break if start/goal is same
				goal = states[x3]                            										
				query = {"start":start, "goal":goal}        #create query dict										
				for it in range (0, problem_iterations):

					start_state = robot.get_current_state()
					start_state.joint_state.position = start				
					group.set_start_state(start_state)
					group.set_joint_value_target(goal)     #takes a list as input
					start_time = time.time()                # *1000 to get millisecond
					planned_path = group.plan()
		
					if (len(planned_path.joint_trajectory.points) == 0): #invalid path
						tm = planning_timeout*failfactor
					else:
						tm = (time.time()-start_time)
					
					result += tm
					print tm
		self.done = True
		return(result)

def sigint_exit(signal, frame):
	moveit_commander.roscpp_shutdown()

if __name__ == "__main__":
	""" The main, init roscpp and rospy, construct class and launch benchmark """

	moveit_commander.roscpp_initialize(sys.argv)
	rospy.init_node('Benchmark_node', anonymous=True, log_level=rospy.FATAL)

	# Read in first arguments.
	planner_type = sys.argv[1]
	scene_number = sys.argv[2]
	problem_iterations = sys.argv[3]

	problem_config = [sys.argv[1],sys.argv[2],sys.argv[3]]

	instance = sys.argv[4]
	specifics = sys.argv[5]
	cutoff = int(float(sys.argv[6]) + 1)
	runlength = int(sys.argv[7])
	seed = int(sys.argv[8])

	bmclass = brc()
	 
	# Read in parameter setting and build a dictionary mapping param_name to param_value.
	params = sys.argv[9:]
	configMap = dict((name[1:], value) for name, value in zip(params[::2], params[1::2]))

	quality = 1000.0

	signal.signal(signal.SIGINT, sigint_exit)
	quality = bmclass.bm_run_cost(problem_config, configMap)

	if (bmclass.done == True):
		print("Result of this algorithm run: SUCCESS, " + str(quality) + ", 0, " + str(quality) +", 0")

	moveit_commander.roscpp_shutdown()