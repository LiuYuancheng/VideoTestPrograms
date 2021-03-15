#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        cameraEchoServer.py
#
# Purpose:     This module will create a camera/video viewer which used to test 
#              the image/data tranfer latency between 2 nodes in a network. It 
#              will display the camera view/video in one window the send the data
#              to the other side of the network. The other side <camEchoClient.py>
#              will echo send the data back, then the sent back data will show 
#              on another window.
#              
# Author:       Yuancheng Liu
#
# Created:     2021/03/11
# Copyright:   Singtel Cyber Security Research & Development Laboratory
# License:     N.A
#-----------------------------------------------------------------------------

import sys
import math
import time
import socket
import pickle

import cv2
import numpy as np
import udpCom
# image transfer : https://gist.github.com/kittinan/e7ecefddda5616eab2765fdb2affed1b
TEST_MD = True  # Test mode: True - use pre-saved video, False - capture from camera.
UDP_PORT = 5005
BUFFER_SZ = udpCom.BUFFER_SZ
CONFIG_FILE = 'camServerConfig.txt'

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class camServer(object):
    def __init__(self, parent, videoSrc=0):
        """ Init the image fetch UDP client and motion detection handler.
            Init example : cam = camServer(None)
        """
        self.paramDict = self.loadConfig()
        self.client = udpCom.udpClient((self.paramDict['IPADD'], UDP_PORT))
        self.termiate = False   # program terminate flag
        # self.staticBack = None # parameter used for 
        # Video capture section:
        self.videoSrc = videoSrc
        print("Capture video from src: %s" % str(self.videoSrc))
        self.cam = cv2.VideoCapture(self.videoSrc)
        self.encodeParam = [int(cv2.IMWRITE_JPEG_QUALITY), 90] # image encode parameter
        # Image resolution setup:
        self.imageW = self.cam.get(3) if TEST_MD else 1600
        self.imageH = self.cam.get(4) if TEST_MD else 900
        print("Video resolution is: %s" %str((self.imageW, self.imageH)))
        if not TEST_MD: self.setResolution(self.imageW, self.imageH)
        # Data parameters:
        self.data = None        # image data (Byte data).
        self.now = time.time()  # time tag used to calculate the latency.

#-----------------------------------------------------------------------------
    def loadConfig(self):
        """ load the config parameter from the config file."""
        paramDict = {   'IPADD': '127.0.0.1', # IPaddress
                        'FRATE': 10,    # display frame rate
                        'DISMD': 0,     # 0:normal mode, 1:different gray-scale mode.
                        'SENLV': 30,    # Motion changed level which will be detected.(smaller->sensitive)
                        'TGMIN': 400,   # Min detected target range, target smaller than TGMIN will be ignore
                        'TGMAX': 10000, # Max detected target range, target bigger than TGMIN will be ignore
        }
        with open(CONFIG_FILE, "r") as fh:
            lines = fh.readlines()
            for line in lines:
                line = line.rstrip()
                if line == '' or line[0] == '#': continue
                key, val = line.split(':')
                paramDict[key] = int(val) if key != 'IPADD' else val
        return paramDict

#-----------------------------------------------------------------------------
    def run(self):
        """ main loop to fetch image bytes from the camera client."""
        print("Start to fetch the image.")
        while not self.termiate:
            self.now = time.time()
            # get a new image from the camera/video
            _, image = self.cam.read()
            if image is None:
                print("Reload the image source.")
                # reload the image source if can not read
                self.cam.release()
                self.cam = None
                self.cam = cv2.VideoCapture(self.videoSrc)
                _, image = self.cam.read()
            _, frame = cv2.imencode('.jpg', image, self.encodeParam)
            self.data = pickle.dumps(frame, 0)
            # Show the captured image in the Orignal window.
            frame = cv2.imdecode(pickle.loads(self.data, fix_imports=True, encoding="bytes"), cv2.IMREAD_COLOR)
            cv2.imshow('Orignal capture',frame) # Show the orignal image.
            # Send the image data to the echo client.
            imgSz = len(self.data)
            rcvIterN = math.ceil(imgSz/float(BUFFER_SZ)) #iteration time to receive one img.
            print('Next image size: %s' %str(imgSz))
            imgData = b'' # received image data.
            for _ in range(int(rcvIterN)):
                msg = None
                if len(self.data) > BUFFER_SZ:
                    msg = self.data[:BUFFER_SZ]
                    self.data = self.data[BUFFER_SZ:]
                else:
                    msg = self.data
                imgData += self.client.sendMsg(msg, resp=True)

            # Check whether the image size is same as the sent one.
            if imgSz != len(imgData):
                print("Error: some image byte lose!")
                continue
            # Show the echo sent back image on Window2.
            frame = cv2.imdecode(pickle.loads(
                imgData, fix_imports=True, encoding="bytes"), cv2.IMREAD_COLOR)
            self.showEchoImage(frame, imgSz, rcvIterN)
            # Tempory disabled the detection.
            #self.detectTgt(frame)

            # if q entered whole process will stop 
            if cv2.waitKey(1) == ord('q'):
                self.termiate = True 
            time.sleep(1/self.paramDict['FRATE'])
        # Destroying all the windows when user quit.        
        cv2.destroyAllWindows() 

#-----------------------------------------------------------------------------
    def showEchoImage(self, frame, imgSz, rcvIterN):
        """ Show the echo sent back image in another window.
        Args:
            frame ([type]): cv image fram
            imgSz ([type]): image size
            rcvIterN ([type]): how many section the image was splitted for sending.
        """
        timeInterval = time.time() - self.now
        dataRate = (imgSz/timeInterval)//1000
        Imglatency = timeInterval*1000/2
        datalatency = Imglatency/rcvIterN
        yPos = 30 
        cv2.rectangle(frame, (20, yPos), (550, yPos+120), (0, 0, 0), -1)
        cv2.putText(frame,"ImgLatency[ms]: %s" %str(Imglatency) , (30,yPos+20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), thickness = 2)
        cv2.putText(frame,"DataLatency[ms]: %s" % str(datalatency) , (30 ,yPos+60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), thickness = 2)
        cv2.putText(frame,"DataRate[kbps]: %s" % str(dataRate) , (30 ,yPos+100), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), thickness = 2)
        cv2.imshow('Echo Back Image',frame)

#-----------------------------------------------------------------------------
    def setResolution(self, w, h):
        """ Set the feed back image resulotion. """
        self.cam.set(3, w)
        self.cam.set(4, h)

#-----------------------------------------------------------------------------
    def detectTgt(self, frame):
        """ [Currently not used in this program]
            Motion detection and target tracking function. Result will show in 
            opencv default window.
            reference: https://www.geeksforgeeks.org/webcam-motion-detector-python/
        """
        # Converting colour image to gray_scale image.
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
        # Converting gray scale image to GaussianBlur.
        gray = cv2.GaussianBlur(gray, (21, 21), 0) 
        # In first iteration we assign the value of staticBack to our first frame.
        if self.staticBack is None: 
            self.staticBack = gray # use the first image as a reference.
            return
        # Difference between static background and current frame (which is GaussianBlur) 
        diffFrame = cv2.absdiff(self.staticBack, gray) 
        # If change in between static background and current frame is greater than 30 
        # it will show white color(255).
        threshFrame = cv2.threshold(diffFrame, self.paramDict['FRATE'], 255, cv2.THRESH_BINARY)[1] 
        threshFrame = cv2.dilate(threshFrame, None, iterations = 2) 
        # Finding contour of moving object.
        cnts, _ = cv2.findContours(threshFrame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
        # old opencv version use the below line:
        # _, cnts, _ = cv2.findContours(threshFrame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
        for contour in cnts: 
            if self.paramDict['TGMIN']< cv2.contourArea(contour) < self.paramDict['TGMAX']:
                (x, y, w, h) = cv2.boundingRect(contour) 
                # Making green rectangles around the moving object.
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3) 
        # Show the difference compare frame or the detection tracking frame.
        if self.paramDict['DISMD']:
            cv2.imshow('Different Gray-Scale Image',diffFrame)
        else:
            cv2.imshow('Echo Back Image',frame)

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
def main():
    videoSrc = 'test.mp4' if TEST_MD else 0 
    cam = camServer(None, videoSrc=videoSrc)
    cam.run()

#-----------------------------------------------------------------------------
if __name__ == '__main__':
    main()


