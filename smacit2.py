# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 10:56:45 2015

@author: ruben
"""

import sys
import os

planner_type = "geometric::BITstar"
pcs_file = "BIT_stop.pcs"
scene_number = "4"
problem_iterations = "5"
smac_iterations = 300

##############################################################

os.system("python load_scene.py " + scene_number)
name = "tmpscenario.txt"
try:
	tfile = open(name,'a') 
	tfile.write("use-instances = false\n")
	tfile.write("numberOfRunsLimit = " + str(smac_iterations) + "\n")
	tfile.write("runObj = RUNTIME\n")
	tfile.write("deterministic = 1\n")
	tfile.write("pcs-file = pcs/" + pcs_file + "\n")
	tfile.write("algo = python smac_runproblem.py " + planner_type + " " + scene_number + " " + problem_iterations + "\n")
	tfile.close()
except:
	print('Something went wrong!')
	sys.exit(0)

os.system("smac/smac --kill-run-exceeding-captime false --transform-crashed-quality false --scenario-file " + name)

os.system("rm " + name)
os.system("python clear_scene.py " + scene_number)

###############################################################