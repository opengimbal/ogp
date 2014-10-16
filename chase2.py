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
s = serial.Serial('/dev/ttyUSB0', 9600)


class chase2(object):
    def __init__(self, js, wsh, wsh2, c2, sqx, sqy):
        self.js = js
        self.wsh = wsh
        self.wsh2 = wsh2
        self.c2=c2
        self.sqx=sqx
        self.sqy=sqy
        
    def run(self):
        cam_mode=1
        s.write('s')
        wsh = self.wsh
        js = self.js
        wsh2 = self.wsh2
        ms = 50
        d = "n"
        acu = int(1)
        acd = int(1)
        acl = int(1)
        acr = int(1)
        c2=self.c2
        sqx=self.sqx
        sqy=self.sqy
        x=0
        y=0
        stat="cam1"
        img1 = c2.getImage()

        blobs = img1.findBlobs()
        if blobs :
            img1.drawCircle((blobs[-1].x,blobs[-1].y),30,color=(255,255,255))
            img1.drawCircle((blobs[-1].centroid()),10,color=(255,100,100))
            blobx1 = blobs[-1].x
            bloby1 = blobs[-1].y
            print blobx1
            print bloby1
            img1.drawText("ogp: centering", 10, 10, fontsize=50)
            img1.drawText(str(blobx1), 10, 200, color=(255,255,255), fontsize=50)
            ##img1.drawText(str(bloby1), 50, 200, color=(255,255,255), fontsize=50)
            img1.drawText(str(bloby1), 10, 250, color=(255,255,255), fontsize=50)
            img1.save(js.framebuffer)
            sqx2=sqx+20
            sqy2=sqy+20
            
            if blobx1 > sqx2:
                d = 'r'
                s.write('4')
                mov = acx(s, d, ms, acu, acd, acl, acr)
                mov.run()
                wsh.write_message(wsh2, "m_"+ str(d))

            if blobx1 < sqx:
                d = 'l'
                s.write('2')
                mov = acx(s, d, ms, acu, acd, acl, acr)
                mov.run()
                wsh.write_message(wsh2, "m_"+ str(d))

            if bloby1 > sqy2:
                d = 'd'
                s.write('9')
                mov = acx(s, d, ms, acu, acd, acl, acr)
                mov.run()
                wsh.write_message(wsh2, "m_"+ str(d))

            if bloby1 < sqy:
                d = 'u'
                s.write('6')
                mov = acx(s, d, ms, acu, acd, acl, acr)
                mov.run()
                wsh.write_message(wsh2, "m_"+ str(d))

            else:
                print "else"            
            wsh.write_message(wsh2, "c")

        else:
            wsh.write_message(wsh2, "c_" + "null" )



class chase3(object):
    def __init__(self, js, wsh, wsh2, c2, sqx, sqy, cam_mode):
        self.cam_mode=cam_mode
        self.js = js
        self.wsh = wsh
        self.wsh2 = wsh2
        self.c2=c2
        self.sqx=sqx
        self.sqy=sqy
        
    def run(self):
        cam_mode=self.cam_mode
        s.write('s')
        wsh = self.wsh
        js = self.js
        wsh2 = self.wsh2
        ms = 50
        d = "n"
        acu = int(1)
        acd = int(1)
        acl = int(1)
        acr = int(1)
        c2=self.c2
        sqx=self.sqx
        sqy=self.sqy
        x=0
        y=0
        stat="centering"
        if cam_mode == 3:
            img1 = c2.getImage()
        if cam_mode==1:
            with picamera.PiCamera() as camera:
                camera.resolution = (544, 288)
                camera.capture('imagesmall.jpg')
            img1 = Image('imagesmall.jpg')
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
            img1.drawText("ogp: centering", 10, 10, fontsize=50)
            img1.drawText(str(blobx1), 10, 200, color=(255,255,255), fontsize=50)
            ##img1.drawText(str(bloby1), 50, 200, color=(255,255,255), fontsize=50)
            img1.drawText(str(bloby1), 10, 250, color=(255,255,255), fontsize=50)
            img1.save(js.framebuffer)
            sqx2=sqx+20
            sqy2=sqy+20

            if blobx1 > sqx2:
                d = '_r'
                s.write('4')
                mov = acx(s, d, ms, acu, acd, acl, acr)
                mov.run()
                wsh.write_message(wsh2, "g_"+ str(d))

            if blobx1 < sqx:
                d = 'l'
                s.write('2')
                mov = acx(s, d, ms, acu, acd, acl, acr)
                mov.run()
                wsh.write_message(wsh2, "g_"+ str(d))

            if bloby1 > sqy2:
                d = 'd'
                s.write('9')
                mov = acx(s, d, ms, acu, acd, acl, acr)
                mov.run()
                wsh.write_message(wsh2, "g_"+ str(d))

            if bloby1 < sqy:
                d = 'u'
                s.write('6')
                mov = acx(s, d, ms, acu, acd, acl, acr)
                mov.run()
                wsh.write_message(wsh2, "g_"+ str(d))
         
            wsh.write_message(wsh2, "c")
        
        else:
            wsh.write_message(wsh2, "c_" + "null" )
