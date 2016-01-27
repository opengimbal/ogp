#!/usr/bin/env python2
# ogplab2.py
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import time
import serial
import os
import ircam
import picamera
from fractions import Fraction

from SimpleCV import Camera, Image

mySet = set()
brightpixels = 0
darkpixels = 0

l = int(4)
s = serial.Serial('/dev/ttyUSB0', 9600)

class so(object):
    def __init__(self, side, js, wsh, wsh2, c2, cam_mode, c):
        self.cam_mode=cam_mode
        self.c2=c2
        self.js = js
        self.wsh = wsh
        self.wsh2 = wsh2
        self.l = side
        self.x = 12
        self.y = -12
        self.w = 0
        self.p = 1
        c2=self.c2
        l = self.l
        x = -1
        y = -1
        self.countdownA = int(self.l)
        self.countdownB = 1
        self.countdownC = 0
        self.left = 0
        self.right = 1
        self.up = 0
        self.down=0
        i = 0
        brightpixels=0
        darkpixels =0
        blobs = 0

    def histo(self): ## this def is the "light meter" part---
        cam_mode = self.cam_mode ## the pic gets cataloged if true ---
        js = self.js
        w = self.w
        cent = 0
        rgb1 = 0
        c2 = self.c2
        wsh = self.wsh
        wsh2 = self.wsh2
        i=0
        brightpixels=0
        darkpixels=0
        blobs = 0

        if cam_mode == 3: ## sort out the confusing cam modes
            img1 = c2.getImage()
            time.sleep(.25)

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

        blobs = img1.findBlobs()
        if blobs:
            crop1 = blobs[-1].x       ## find the blob centroid and cut it out  20x20
            crop2 = blobs[-1].y
            crop3 = crop1 - 10
            crop4 = crop2 - 10
            thumbnail = img1.crop(crop3,crop4,20,20)
            img2 = thumbnail
            hist = img2.histogram(20)   ## split the thumb into 20 levels of darkness
            brightpixels = hist[10]   ## 10 is where the darkest of the light pixels accumulate
            print brightpixels

##            while i < 20:        ## old code for if you want to split the histogram in two
##                if (i < 10):
##                    darkpixels = darkpixels + hist[i]
##                    self.darkpixels = darkpixels
##                    print hist[i]
##                else:
##                    brightpixels = brightpixels + hist[i]
##                    self.brightpixels = brightpixels
##                    print hist[i]
##                i = i + 1

            if (brightpixels<150):   ## heres where it decides to catalog the pic or not...
                print darkpixels,'_', brightpixels
                wsh.write_message(wsh2, "histo_" + str(darkpixels) + "_" + str(brightpixels))
                print "blob"
                x = self.x
                y = self.y
                p = self.p
                p = p + 1
                thumb1 = "/var/www/images/thumbs/thumb"
                thumb3 = ".png"
                thumbpath = thumb1 + str(p) + thumb3
                print thumbpath
                thumbnail.save(thumbpath)
                img1.drawCircle((blobs[-1].x,blobs[-1].y),30,color=(255,255,255))
                img1.drawCircle((blobs[0].centroid()),10,color=(255,100,100))
                print blobs[-1].meanColor()
                rgb1 = blobs[-1].meanColor()
                cent = blobs[-1].centroid()

                pth1 = "/var/www/images/image"
                pth3 = ".png"
                pth = pth1 + str(p) + pth3
                print pth
                img1.save(pth)

                self.p = p

                mySet.add((p,x,y,w,cent,rgb1))
                self.mySet = mySet

                wshx = str(self.x)
                wshy = str(self.y)

                centroidx = int(cent[0])
                centroidy=int(cent[1])
                rcolor=rgb1[0]
                gcolor=rgb1[1]
                bcolor=rgb1[2]
                rcolor=int(rcolor)
                gcolor=int(gcolor)
                bcolor=int(bcolor)
                wsh.write_message(wsh2, "rgb_" + str(rcolor)+"_"+str(gcolor)+"_"+str(bcolor))
                wsh.write_message(wsh2, "x_" + str(centroidx)+"_"+str(centroidy))
                img1.save(js.framebuffer)
                wsh.write_message(wsh2, "d_" + wshx + "_" + wshy + "_" + str(p) )

            else:
                print "dark"
                print darkpixels,'_', brightpixels
                blobs = 0
                wsh.write_message(wsh2, "histo_" + str(darkpixels) + "_" + str(brightpixels))

        else:
            wshx = str(self.x)
            wshy = str(self.y)
            wsh.write_message(wsh2, wshx + " " + wshy + "dark")
            img1.save(js.framebuffer)

            print "dark"


    def run(self):    ## this def is the movement iterator
        wsh = self.wsh
        wsh2 = self.wsh2

        countdownA = self.countdownA
        countdownB = self.countdownB
        countdownC = self.countdownC
        left = self.left
        right = self.right
        up = self.up
        down = self.down

        x = self.x
        y = self.y
        wsh2 = self.wsh2

        if (countdownB < countdownA):
            print "ctb",countdownB
            print right
            if (right > 0):
                print "right- 0"
                print right
                s.write('p')
                x = x + 1
                self.x = x
                time.sleep(1)
                elf = self.histo()
                wsh.write_message(wsh2, "m" )
                right = right - 1
                self.right = right
                if (right == 0):
                    down = countdownB
                    self.down = down
            if (down>0):
                print "ctb",countdownB
                print "down"
                print down
                s.write('l')
                time.sleep(1)
                y = y - 1
                self.y = y
                elf = self.histo()
                wsh.write_message(wsh2, "m" )
                down = down - 1
                self.down = down
                if (down == 0):
                    countdownB += 1
                    self.countdownB = countdownB
                    left = countdownB
                    self.left = left
                    print "ctb", countdownB

            if (left>0):
                print "left"
                print left
                print "ctb",countdownB

                s.write('k')
                time.sleep(1)
                x = x - 1
                self.x = x
                elf = self.histo()
                wsh.write_message(wsh2, "m" )
                left = left - 1
                self.left = left
                if (left == 0):
                    print "ctb",countdownB

                    up = countdownB
                    self.up = up


            if (up>0):
                print "up"
                print "ctb",countdownB

                print up
                s.write('o')
                y = y + 1
                self.y = y
                time.sleep(1)
                elf = self.histo()
                wsh.write_message(wsh2, "m" )
                up = up - 1
                self.up = up
                if (up == 0):
                    countdownB += 1
                    self.countdownB = countdownB
                    right = countdownB
                    self.right = right
                    print "ctb",countdownB

        else:
            wsh = self.wsh
            wsh2 = self.wsh2

            wsh.write_message(wsh2, "map complete" )

            print "done"
