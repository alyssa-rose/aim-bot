# -*- coding: utf-8 -*-
"""
Created on Sat Aug 27 15:40:58 2022

@author: Alyssa
"""
import serial
import time

import numpy as np
import cv2


class CircleKiller():
    """ Class to locate, track, and shoot circles
    as seen in AimLabs. Original concept by the lovely 
    Daniel Bekai"""
    
    def __init__(self, arduino_port: str = 'COM7', baud_rate: int = 115200, camera_id: int = 0) -> None:
        '''
        Parameters
        ----------
        arduino_port : str, optional
            DESCRIPTION. The default is 'COM7'.
        baud_rate : int, optional
            DESCRIPTION. The default is 115200.
        camera_id : int, optional
            DESCRIPTION. The default is 0.

        Returns
        -------
        None.

        '''
        # initialize the connection to the arduino
        self.serialcomm = serial.Serial(arduino_port, baud_rate)
        self.serialcomm.timeout = 1

        # Start capturing video
        self.cap = cv2.VideoCapture(camera_id)

        # global variable for previous circle
        self.prevcircle = None
        
        
    def control_law(self, dx: int, dy: int, dist_from_center: int) -> str:
        '''
        Parameters
        ----------
        dx : int
            DESCRIPTION.
        dy : int
            DESCRIPTION.
        dist_from_center : int
            DESCRIPTION.

        Returns
        -------
        str
            DESCRIPTION.

        '''
        kpx = 5
        kdx = 1
        kix = 0

        kpy = 10
        kdy = 1
        kiy = 0

        ex = (kpx*dx)
        ey = -1*kpy*dy

        return "{}x{}z".format(ex, ey)
    
    def dist(self, x1: float, y1: float, x2: float, y2: float) -> float: 
        '''
        Parameters
        ----------
        x1 : float
            DESCRIPTION.
        y1 : float
            DESCRIPTION.
        x2 : float
            DESCRIPTION.
        y2 : float
            DESCRIPTION.

        Returns
        -------
        float
            DESCRIPTION.

        '''
        return np.sqrt((x1-x2)**2+(y1-y2)**2)
    
    def update(self) -> bool:
        '''
        

        Returns
        -------
        bool
            DESCRIPTION.

        '''
        ret, frame = self.cap.read()
        width = int(self.cap.get(3))
        height = int(self.cap.get(4))

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_blue = np.array([90, 50, 50])
        upper_blue = np.array([130, 255, 255])

        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        result = cv2.bitwise_and(frame, frame, mask=mask)

        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        result = result[:, :, 2]

        circles = cv2.HoughCircles(result, cv2.HOUGH_GRADIENT, 1.2,
                                   100, param1=100, param2=30, minRadius=30, maxRadius=100)

        cv2.circle(frame, (640, 360), 5, (0, 0, 255), 2)
        if circles is not None:
            circles = np.uint16(np.around(circles))
            chosen = None
            closecircle_dist = 1000000

            # iterate over all the current circles on the screen and find the closest one
            for i in circles[0, :]:
                cv2.circle(frame, (i[0], i[1]), 1, (0, 100, 100), 3)
                cv2.circle(frame, (i[0], i[1]), i[2], (255, 0, 255), 3)
                dist_from_center = self.dist(i[0], i[1], 640, 360)
                if dist_from_center < closecircle_dist:
                    closecircle_dist = dist_from_center
                    chosen = i
            cv2.line(frame, (640, 360), (chosen[0], chosen[1]), (0, 255, 0), 3)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, str(closecircle_dist),
                        (640, 360), font, 4, (0, 0, 0), 3)
            dx = chosen[0] - 640
            dy = 360-chosen[1]
            dist_from_center = self.dist(chosen[0], chosen[1], 640, 360)
            velocities = self.control_law(dx, dy, dist_from_center)
            print(velocities)

            self.serialcomm.write(velocities.encode())
            time.sleep(0.03)  # sleep to avoid overwhelming the arduino

        cv2.imshow('frame', frame) # display the current frame with all the circles
        
        # if q is pressed, then break out of the loop and end communication
        if cv2.waitKey(1) == ord('q'):
            velocities = "0x0z"
            self.serialcomm.write(velocities.encode())
            self.serialcomm.close()
            return False
        return True
        
        
    def kill(self) -> None:
        '''
        

        Returns
        -------
        None
            DESCRIPTION.

        '''
        self.cap.release()
        cv2.destroyAllWindows()
            
    
    
    
    
    
    
    
    