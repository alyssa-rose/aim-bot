# -*- coding: utf-8 -*-
"""
Created on Sat Aug 27 15:51:51 2022

@author: Alyssa
"""
import serial
import time

import numpy as np
import cv2

from circle_killer import CircleKiller



if __name__ == "__main__":
    # initialize the CircleKiller object
    ck = CircleKiller(arduino_port='COM7', baud_rate=115200, camera_id=0)
    keep_running = True
    
    # continue to find new circles and shoot until the user types 'q'
    while keep_running:
        keep_running = ck.update()
        
    # user has ended the program, release all the variables cleanly
    ck.kill()