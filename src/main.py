# -*- coding: utf-8 -*-
"""
Created on Sat Aug 27 15:51:51 2022

@author: Alyssa
"""

# Standard library imports.
import time

# Related third party imports.
import cv2
import numpy as np
import serial

# Local application/library specific imports.
from circle_killer import CircleKiller



if __name__ == "__main__":
    # initialize the CircleKiller object
    ck = CircleKiller(arduino_port='COM7', 
                      baud_rate=115200, 
                      camera_id=0,
                      screen_center_width=640,
                      screen_center_height=360)
    keep_running = True
    
    # continue to find new circles and shoot until the user types 'q'
    while keep_running:
        keep_running = ck.update()
        
    # user has ended the program, release all the variables cleanly
    ck.kill()