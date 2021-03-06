#!/usr/bin/env python

# local pymodules
from threading import local
from planning import *
from vision import *

from copy import deepcopy

if __name__ == '__main__':
    rospy.init_node('vision_planner_node', anonymous=True)
    camera = RSCamera()
    arm = URPlanner(speed=0.25)
    arm.go_to_known_location('zone2')
    
    try:
        locations = deepcopy(camera.find_contour_centers(camera.find_contours(), camera.observable))
        for location in locations:
            dx, dy = camera.distance_to_camera(location)
            arm.move_ik_xyz(dx, dy, 0.0)
            arm.move_ik_xyz(0, 0, -0.29 / 2)
            camera.observable = 'narrow'
            localized_center = camera.find_contour_centers(camera.find_contours(), camera.observable)[0]
            dxl, dyl = camera.distance_to_camera(localized_center)
            arm.move_ik_xyz(dxl, dyl, 0.0)
            arm.nozzle_to_camera()
            arm.move_ik_xyz(0, 0, -0.29 / 2)
            arm.move_ik_xyz(0, 0, -0.0025)
            arm.vacuum_on()
            rospy.sleep(2)
            arm.move_ik_xyz(0, 0, 0.05)
            rospy.sleep(1)
            arm.go_to_known_location('zone1')
            arm.nozzle_to_camera()
            rospy.sleep(1)
            arm.move_ik_xyz(0, 0, -0.29 / 4 * 3)
            arm.vacuum_off()
            rospy.sleep(3)
            camera.observable = 'full'
            arm.go_to_known_location('zone2')
    except:
        exit(0)
        
    rospy.spin()