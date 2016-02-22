smacit tool

In order to run:
- start move_group/rviz: roslaunch "ur5_moveit_config demo.launch"
- configure smac in smacit.py
- run smac by doing "python smacit.py"

files that SMAC needs:
- pcs file: parameter defninition (predefined for each planner)
- scenario file: configuration (created by the smacit.py)
- algo command: executable that runs the problem (created by smacit.py)

Getting states:

do move->execute with rviz, wait until robot arrives and run python ur5_getstate.py
