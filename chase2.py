#!/usr/bin/env python2
# chase2.py

import time
import serial
import os
import ircam
import picamera
from SimpleCV import Camera, Image
from ogplab import *

l = int(4)
##s = serial.Serial('/dev/ttyUSB0', 9600)

class chase3(object):    ##livecam
    def __init__(self, js, wsh, wsh2, c2, sqx, sqy, cam_mode, c):
        self.cam_mode = cam_mode
        self.js = js
        self.wsh = wsh
        self.wsh2 = wsh2
        self.c2 = c2
        self.c = c
        self.sqx = sqx
        self.sqy = sqy
        
    def run(self):
        cam_mode=self.cam_mode
        wsh = self.wsh
        js = self.js
        wsh2 = self.wsh2
        d = "n"
        c2 = self.c2
        c = self.c
        sqx = self.sqx
        sqy = self.sqy
        x = 0
        y = 0
        stat="live cam"
        if cam_mode == 3:
            img1 = c2.getImage()
        if cam_mode==1:
            img1 = c.getImage()
            time.sleep(1)
	    with picamera.PiCamera() as camera:
                camera.resolution = (544, 288)
                camera.capture('imagesmall.jpg')
            img2 = Image('imagesmall.jpg')
            time.sleep(.5)
            img1 = img1.sideBySide(img2)
            img1 = img1.scale(544,288)
            time.sleep(.5)
        if cam_mode==2:
            with picamera.PiCamera() as camera:
                camera.resolution = (544, 288)
                camera.capture('imagesmall.jpg')
            img1 = Image('imagesmall.jpg')
        self.img1 = img1

        blobs = img1.findBlobs()
        if blobs :
            ##blobs.draw()
            img1.drawCircle((blobs[-1].x,blobs[-1].y),30,color=(255,255,255))
            img1.drawCircle((blobs[-1].centroid()),10,color=(255,100,100))
            blobx1 = blobs[-1].x
            bloby1 = blobs[-1].y
            print blobx1
            print bloby1
            img1.drawText("ogp: live cam", 10, 10, fontsize=50)
            img1.drawText(str(blobx1), blobx1, 250, color=(255,255,255), fontsize=20)
            img1.drawText(str(bloby1), 10, bloby1, color=(255,255,255), fontsize=20)
            img1.save(js.framebuffer)
            sqx2=sqx+20
            sqy2=sqy+20
            time.sleep(.5) 
            wsh.write_message(wsh2, "live")
        
        else:
            wsh.write_message(wsh2, "live")

class chase4(object):
    def __init__(self, js, wsh, wsh2, c2, sqx, sqy, cam_mode, c):
        self.cam_mode=cam_mode
        self.js = js
        self.wsh = wsh
        self.wsh2 = wsh2
        self.c2=c2
        self.c=c
        self.sqx=sqx
        self.sqy=sqy
        
    def run(self):
        cam_mode=self.cam_mode
        wsh = self.wsh
        js = self.js
        wsh2 = self.wsh2
        d = "n"
        acu = int(1)
        acd = int(1)
        acl = int(1)
        acr = int(1)
        c2=self.c2
        c=self.c
        sqx=self.sqx
        sqy=self.sqy
        x=0
        y=0
        stat="centering"
        if cam_mode == 3:
            img1 = c2.getImage()
        if cam_mode==1:
            img1 = c.getImage()
##            with picamera.PiCamera() as camera:
##                camera.resolution = (544, 288)
##                camera.capture('imagesmall.jpg')
##            img1 = Image('imagesmall.jpg')
        if cam_mode==2:
            with picamera.PiCamera() as camera:
                camera.resolution = (544, 288)
                camera.capture('imagesmall.jpg')
            img1 = Image('imagesmall.jpg')
        self.img1 = img1

        blobs = img1.findBlobs()
        if blobs :
            ##blobs.draw()
            img1.drawCircle((blobs[-1].x,blobs[-1].y),30,color=(255,255,255))
            img1.drawCircle((blobs[-1].centroid()),10,color=(255,100,100))
            blobx1 = blobs[-1].x
            bloby1 = blobs[-1].y
            print blobx1
            print bloby1

            print "sensor"
            s.write('n')
            time.sleep(1)
            position = "altaz_ " + str(s.readline())
            wsh.write_message(wsh2, str(position))
            
            img1.drawText("ogp: chasing", 10, 5, fontsize=40)
            img1.drawText(str(blobx1), blobx1, 250, color=(255,255,255), fontsize=20)
            img1.drawText(str(bloby1), 10, bloby1, color=(255,255,255), fontsize=20)
            img1.drawText(str(position), 10, 50, color=(255,255,255), fontsize=25)
            sqx2=sqx+20
            sqy2=sqy+20
            img1.drawRectangle(sqx,sqy,20,20,color=(100,100,255))
            
            img1.save(js.framebuffer)
            
            if blobx1 > sqx2:
                d = 'r'
                s.write('s')
                time.sleep(.5)
                wsh.write_message(wsh2, "g_"+ str(d))

            if blobx1 < sqx:
                d = 'l'
                s.write('q')
                time.sleep(.5)
                wsh.write_message(wsh2, "g_"+ str(d))

            if bloby1 > sqy2:
                d = 'd'
                s.write('a')
                time.sleep(.5)
                wsh.write_message(wsh2, "g_"+ str(d))

            if bloby1 < sqy:
                d = 'u'
                s.write('w')
                time.sleep(.5)
                wsh.write_message(wsh2, "g_"+ str(d))
            time.sleep(.5) 
            wsh.write_message(wsh2, "c")
        
        else:
            wsh.write_message(wsh2, "c" )
            wsh.write_message(wsh2, "CAPTURE" )
