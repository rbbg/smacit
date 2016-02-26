# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 10:56:45 2015

@author: ruben
"""

import sys
import os

planner_type = "geometric::BITstar"
pcs_file = "BIT_stop.pcs"
scene_number = "7"
problem_iterations = "3"
smac_iterations = 10000
walltime_limit = 30*60

##############################################################

os.system("python load_scene.py " + scene_number)
name = "tmpscenario.txt"
try:
	tfile = open(name,'a') 
	tfile.write("use-instances = false\n")
	tfile.write("numberOfRunsLimit = " + str(smac_iterations) + "\n")
	tfile.write("runtimeLimit = " + str(walltime_limit) + "\n")
	tfile.write("runObj = QUALITY\n")
	tfile.write("deterministic = 1\n")
	tfile.write("pcs-file = pcs/" + pcs_file + "\n")
	tfile.write("algo = python smac_runproblem.py " + planner_type + " " + scene_number + " " + problem_iterations + "\n")
	
	tfile.write("check-sat-consistency false \n")
	tfile.write("check-sat-consistency-exception false \n")
	tfile.write("algo-cutoff-time 25\n")
	tfile.write("kill-run-exceeding-captime-factor 2\n")

	# tfile.write("kill-run-exceeding-captime false")
	# tfile.write("transform-crashed-quality false")

	tfile.close()
except:
	print('Something went wrong!')
	sys.exit(0)

# os.system("smac/smac --kill-run-exceeding-captime false --transform-crashed-quality false --scenario-file " + name)
os.system("smac/smac --scenario-file " + name)

os.system("rm " + name)
os.system("python clear_scene.py " + scene_number)

###############################################################