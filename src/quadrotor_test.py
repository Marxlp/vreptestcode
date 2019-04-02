# Copyright 2006-2017 Coppelia Robotics GmbH. All rights reserved. 
# marc@coppeliarobotics.com
# www.coppeliarobotics.com
# 
# -------------------------------------------------------------------
# THIS FILE IS DISTRIBUTED "AS IS", WITHOUT ANY EXPRESS OR IMPLIED
# WARRANTY. THE USER WILL USE IT AT HIS/HER OWN RISK. THE ORIGINAL
# AUTHORS AND COPPELIA ROBOTICS GMBH WILL NOT BE LIABLE FOR DATA LOSS,
# DAMAGES, LOSS OF PROFITS OR ANY OTHER KIND OF LOSS WHILE USING OR
# MISUSING THIS SOFTWARE.
# 
# You are free to use/modify/distribute this file for whatever purpose!
# -------------------------------------------------------------------
#
# This file was automatically created for V-REP release V3.4.0 rev. 1 on April 5th 2017

# Make sure to have the server side running in V-REP: 
# in a child script of a V-REP scene, add following command
# to be executed just once, at simulation start:
#
# simExtRemoteApiStart(19999)
#
# then start simulation, and run this program.
#
# IMPORTANT: for each successful call to simxStart, there
# should be a corresponding call to simxFinish at the end!

import os
from math import sin,cos
import numpy as np

from vrepConst import simx_opmode_oneshot

try:
    import vrep
except:
    print ('--------------------------------------------------------------')
    print ('"vrep.py" could not be imported. This means very probably that')
    print ('either "vrep.py" or the remoteApi library could not be found.')
    print ('Make sure both are in the same folder as this file,')
    print ('or appropriately adjust the file "vrep.py"')
    print ('--------------------------------------------------------------')
    print ('')

import time

print ('Program started')
vrep.simxFinish(-1) # just in case, close all opened connections
clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5) # Connect to V-REP
if clientID!=-1:
    print('Connected to remote API server')
    
    # Now try to retrieve data in a blocking fashion (i.e. a service call):
    res,objs=vrep.simxGetObjects(clientID,vrep.sim_handle_all,vrep.simx_opmode_blocking)
    if res==vrep.simx_return_ok:
        print ('connect success')
        current_filename = os.path.realpath(__file__)
        vrep.simxAddStatusbarMessage(clientID,'connected from '+ current_filename,
                                     vrep.simx_opmode_oneshot)
    else:
        print ('Remote API function call returned with error code: ',res)
    
    res,quadrotor_base = vrep.simxGetObjectHandle(clientID,"Quadricopter_base", vrep.simx_opmode_oneshot_wait)
    _,quadrotor_target = vrep.simxGetObjectHandle(clientID, "Quadricopter_target", vrep.simx_opmode_oneshot_wait)
    if _ == vrep.simx_return_ok:
        print('get the object')
        print(quadrotor_target)
    
    # the target position
    target_position = [[-0.14999999105930328+x, 0.19999998807907104,1+0.4*sin(x)] for x in np.linspace(0,2*np.pi,100)]
    _,quadrotor_target_position= vrep.simxGetObjectPosition(clientID, quadrotor_target, -1, vrep.simx_opmode_streaming)
    for  i in range(100):
        vrep.simxSetObjectPosition(clientID, quadrotor_target, -1,target_position[i], vrep.simx_opmode_oneshot)
        time.sleep(0.05)
        res,quadrotor_target_position = vrep.simxGetObjectPosition(clientID, quadrotor_target, -1, vrep.simx_opmode_buffer)
        if res == vrep.simx_return_ok:
            print(target_position)
        else:
            print('no data')
    
    vrep.simxAddStatusbarMessage(clientID,'connected closed ',
                                     vrep.simx_opmode_oneshot)
    # Before closing the connection to V-REP, make sure that the last command sent out had time to arrive. 
    # You can guarantee this with (for example):
    vrep.simxGetPingTime(clientID)
    
    # Now close the connection to V-REP:
    vrep.simxAddStatusbarMessage(clientID,'connected closed ',
                                     vrep.simx_opmode_oneshot)
    vrep.simxFinish(clientID)
else:
    print ('Failed connecting to remote API server')
print ('Program ended')
