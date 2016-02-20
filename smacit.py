# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 10:56:45 2015

@author: ruben
"""

import sys
import os

planner_type = "geometric::RRTConnect"
pcs_file = "RRTC.pcs"
smac_iterations = 100

name = "tmpscenario.txt"
try:
	tfile = open(name,'a') 
	tfile.write("use-instances = false\n")
	tfile.write("numberOfRunsLimit = " + str(smac_iterations) + "\n")
	tfile.write("runObj = RUNTIME\n")
	tfile.write("deterministic = 1\n")
	tfile.write("pcs-file = pcs/" + pcs_file + "\n")
	tfile.write("algo = python smac_runproblem.py " + planner_type + "\n")
	tfile.close()
except:
	print('Something went wrong!')
	sys.exit(0)

os.system("smac/smac --scenario-file " + name)
os.system("rm " + name)