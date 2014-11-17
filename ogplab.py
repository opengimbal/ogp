#!/usr/bin/env python2
# ogp5.py

import time
import serial
import os
import ircam
import picamera

from SimpleCV import Camera, Image

mySet = set()
brightpixels = 0
darkpixels = 0

l = int(4)
s = serial.Serial('/dev/ttyUSB0', 9600)

class so(object):

    def __init__(self, side, m, js, wsh, wsh2, c2, cam_mode):
        self.cam_mode=cam_mode
        self.c2=c2
        self.ms = m
        self.js = js
        self.wsh = wsh
        self.wsh2 = wsh2
        self.m = m
        self.l = side
        self.x = 0
        self.y = 0
        self.w = 0
        self.p = 1        
        c2=self.c2
        l = self.l
        x = -1
        y = -1
        self.countdownA = int(self.l)
        self.countdownB = int(self.l)
        self.countdownC = -1

    def histo(self):
        cam_mode = self.cam_mode
        js = self.js
        ms = self.ms
        w = self.w
        cent = 0
        rgb1 = 0
        c2 = self.c2
        wsh = self.wsh 
        wsh2 = self.wsh2
        s.write('s')
        
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
        
        if blobs:
            print "blob"
            x = self.x
            y = self.y
            p = self.p
            p = p + 1
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
            
            thumbnail = img1.crop(150,25,250,250)
            thumbnail = thumbnail.scale(20,20)
            thumb1 = "/var/www/images/thumbs/thumb"
            thumb3 = ".png"
            thumbpath = thumb1 + str(p) + thumb3
            print thumbpath
            thumbnail.save(thumbpath)
            
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
            wshx = str(self.x)
            wshy = str(self.y)
            wsh.write_message(wsh2, wshx + " " + wshy + "dark")
 
            print "dark"


    def run(self):
        wsh = self.wsh 
        wsh2 = self.wsh2
        acu = int(1)
        acd = int(1)
        acl = int(1)
        acr = int(1)
        countdownA = self.countdownA
        countdownB = self.countdownB
        countdownC = self.countdownC
        ms = self.ms
        x = self.x
        y = self.y
        if countdownA > 0:
                

            if countdownC == 1:
                countdownB = int(self.l)
                countdownC = -1
                print "down"
                d = 'd'
                s.write('9')
                mov = acx(s, d, ms, acu, acd, acl, acr)
                mov.run()
                y = y - 1
                self.y = y
                elf = self.histo()
##                time.sleep(1)
                countdownA -=1
                wsh.write_message(wsh2, "m" )
                self.countdownA = countdownA
                self.countdownB = countdownB
                self.countdownC = countdownC
            if countdownC > 1:
                print "left"
                countdownC -= 1
                d = 'l'
                s.write('2')
                mov = acx(s, d, ms, acu, acd, acl, acr)
                mov.run()
                x = x - 1
                self.x = x
              ##  time.sleep(1)
                elf = self.histo()
                s.write('s')
         ##       time.sleep(1)
                wsh.write_message(wsh2, "m" )
                        
                self.countdownA = countdownA
                self.countdownB = countdownB
                self.countdownC = countdownC
            
            if countdownB == 1:
                countdownC = int(self.l)
                countdownB = -1
                print "down"
                d = 'd'
                s.write('9')
                mov = acx(s, d, ms, acu, acd, acl, acr)
                mov.run()
                y = y - 1
                self.y = y
                time.sleep(1)
                elf = self.histo()
        ##        time.sleep(1)
                countdownA -=1
                wsh.write_message(wsh2, "m" )
                self.countdownA = countdownA
                self.countdownB = countdownB
                self.countdownC = countdownC
                
                print self.l
                print countdownC
                print self.countdownC
            if countdownB > 1:
                print "right"
                countdownB-=1
                d = 'r'
                s.write('4')
                mov = acx(s, d, ms, acu, acd, acl, acr)
                mov.run()
                s.write('s')
                s.write('j')
                x = x + 1
                self.x = x
          ##      time.sleep(1)
                elf = self.histo()
            ##    time.sleep(1)
                wsh.write_message(wsh2, "m" )
                
                self.countdownA = countdownA
                self.countdownB = countdownB
                self.countdownC = countdownC



        else:
            wsh = self.wsh
            wsh2 = self.wsh2

         ##   wsh.write_message(wsh2, str(mySet) )
            wsh.write_message(wsh2, "map complete" )

            print "done"



class autocal(object):
    def __init__(self, js, wsh, wsh2):
        self.js = js
        self.wsh = wsh
        self.wsh2 = wsh2
      ##  self.c = c
    
    def run(self):

        wsh = self.wsh
      ##  c = self.c
        js = self.js
        wsh2 = self.wsh2
        acu = int(1)
        acd = int(1)
        acl = int(1)
        acr = int(1)
        irpic = pinoir2(js)

        img1 = Image('imagesmall.jpg')   
        blobs = img1.findBlobs()
        img1.drawCircle((blobs[-1].x,blobs[-1].y),30,color=(255,255,255))
        img1.drawCircle((blobs[-1].centroid()),10,color=(255,100,100))
        acx1 = blobs[-1].x
        acy1 = blobs[-1].y


        img1.drawText("ogp: autocalibrating", 10, 10, fontsize=50)
        img1.drawText(str(acx1), 10, 50, color=(255,255,255), fontsize=20)
        img1.drawText(str(acy1), 10, 75, color=(255,255,255), fontsize=20)
        img1.save(js.framebuffer)
        
        d = 'r'
        ms = 50
        s.write('4')
        mov = acx(s, d, ms, acu, acd, acl, acr)
        mov.run()
            
        time.sleep(1)

        img1 = c.getImage()   
        blobs = img1.findBlobs()
        img1.drawCircle((blobs[-1].x,blobs[-1].y),30,color=(255,255,255))
        img1.drawCircle((blobs[-1].centroid()),10,color=(255,100,100))
        acx2 = blobs[-1].x
        acy2 = blobs[-1].y

        
        img1.drawText("ogp: autocalibrating", 10, 10, fontsize=50)
        img1.drawText(str(acx1), 10, 50, color=(255,255,255), fontsize=20)
        img1.drawText(str(acy1), 10, 75, color=(255,255,255), fontsize=20)        
        img1.drawText(str(acx2), 40, 50, color=(255,255,255), fontsize=20)
        img1.drawText(str(acy2), 40, 75, color=(255,255,255), fontsize=20)
        img1.save(js.framebuffer)
        
        d = 'd'
        ms = 50
        s.write('9')
        mov = acx(s, d, ms, acu, acd, acl, acr)
        mov.run()
        time.sleep(1)


        img1 = c.getImage()   
        blobs = img1.findBlobs()
        img1.drawCircle((blobs[-1].x,blobs[-1].y),30,color=(255,255,255))
        img1.drawCircle((blobs[-1].centroid()),10,color=(255,100,100))
        acx3 = blobs[-1].x
        acy3 = blobs[-1].y

        img1.drawText("ogp: autocalibrating", 10, 10, fontsize=50)
        img1.drawText(str(acx1), 10, 50, color=(255,255,255), fontsize=20)
        img1.drawText(str(acy1), 10, 75, color=(255,255,255), fontsize=20)        
        img1.drawText(str(acx2), 40, 50, color=(255,255,255), fontsize=20)
        img1.drawText(str(acy2), 40, 75, color=(255,255,255), fontsize=20)
        img1.drawText(str(acx3), 70, 50, color=(255,255,255), fontsize=20)
        img1.drawText(str(acy3), 70, 75, color=(255,255,255), fontsize=20)
        img1.save(js.framebuffer)
        d = 'l'
        ms = 50
        s.write('2')
        mov = acx(s, d, ms, acu, acd, acl, acr)
        mov.run()
        time.sleep(1)


        img1 = c.getImage()   
        blobs = img1.findBlobs()
        img1.drawCircle((blobs[-1].x,blobs[-1].y),30,color=(255,255,255))
        img1.drawCircle((blobs[-1].centroid()),10,color=(255,100,100))
        acx4 = blobs[-1].x
        acy4 = blobs[-1].y

        img1.drawText("ogp: autocalibrating", 10, 10, fontsize=50)
        img1.drawText(str(acx1), 10, 50, color=(255,255,255), fontsize=20)
        img1.drawText(str(acy1), 10, 75, color=(255,255,255), fontsize=20)        
        img1.drawText(str(acx2), 40, 50, color=(255,255,255), fontsize=20)
        img1.drawText(str(acy2), 40, 75, color=(255,255,255), fontsize=20)
        img1.drawText(str(acx3), 70, 50, color=(255,255,255), fontsize=20)
        img1.drawText(str(acy3), 70, 75, color=(255,255,255), fontsize=20)
        img1.drawText(str(acx4), 100, 50, color=(255,255,255), fontsize=20)
        img1.drawText(str(acy4), 100, 75, color=(255,255,255), fontsize=20)
        img1.save(js.framebuffer)
        d = 'u'
        ms = 50
        s.write('6')
        mov = acx(s, d, ms, acu, acd, acl, acr)
        mov.run()
        time.sleep(1)
        
        img1 = c.getImage()   
        blobs = img1.findBlobs()
        img1.drawCircle((blobs[-1].x,blobs[-1].y),30,color=(255,255,255))
        img1.drawCircle((blobs[-1].centroid()),10,color=(255,100,100))
        acx5 = blobs[-1].x
        acy5 = blobs[-1].y
        img1.drawText("ogp: autocalibrating", 10, 10, fontsize=50)
        img1.drawText(str(acx1), 10, 50, color=(255,255,255), fontsize=20)
        img1.drawText(str(acy1), 10, 75, color=(255,255,255), fontsize=20)        
        img1.drawText(str(acx2), 40, 50, color=(255,255,255), fontsize=20)
        img1.drawText(str(acy2), 40, 75, color=(255,255,255), fontsize=20)
        img1.drawText(str(acx3), 70, 50, color=(255,255,255), fontsize=20)
        img1.drawText(str(acy3), 70, 75, color=(255,255,255), fontsize=20)
        img1.drawText(str(acx4), 100, 50, color=(255,255,255), fontsize=20)
        img1.drawText(str(acy4), 100, 75, color=(255,255,255), fontsize=20)
        img1.drawText(str(acx5), 130, 50, color=(255,255,255), fontsize=20)
        img1.drawText(str(acy5), 130, 75, color=(255,255,255), fontsize=20)
        img1.save(js.framebuffer)
        cal1 = acx1 - acx2
        cal2 = acy2 - acy3
        cal3 = acx3 - acx4
        cal4 = acy4 = acy5
        time.sleep(2)
        wsh.write_message(wsh2, "x_" + str(cal1) + "_" + str(cal2) + "_" + str(cal3)+ "_" + str(cal4) )


class hud2(object):
    def __init__(self, img1, js, stat, x, y, z):
        self.img1 = img1
        self.js = js
        self.stat = stat
        self.x = x
        self.y = y
        self.z = z
        
    
    def run(self):        
        img1 = self.img1
        js = self.js
        stat = self.stat
        x = self.x
        y = self.y
        z = self.z
        cent = 0
        rgb1 = 0
        

        
        blobs = img1.findBlobs()
        if blobs:
            crop1 = blobs[-1].x
            crop2 = blobs[-1].y
            crop3 = crop1 - 294
            crop4 = crop2 - 144
            img1 = img1.crop(crop3,crop4,544,288)
            img1.drawCircle((blobs[-1].x,blobs[-1].y),30,color=(255,255,255))
            img1.drawCircle((blobs[-1].centroid()),10,color=(255,100,100))
            rgb1 = blobs[-1].meanColor()
            cent = blobs[-1].centroid()
            

        img1.drawText(str(stat), 10, 10, fontsize=50)
        img1.drawText(str(x), 10, 70, color=(255,255,255), fontsize=25)
        img1.drawText(str(y), 10, 100, color=(255,255,255), fontsize=25)
        
        img1.drawText(str(z), 10, 230, color=(255,255,255), fontsize=15)
        img1.drawText(str(cent), 10, 250, color=(255,255,255), fontsize=15)
        img1.drawText(str(rgb1), 10, 270, color=(255,255,255), fontsize=15)
        img1.save(js.framebuffer)

class acx(object):
    def __init__(self, s, d, ms, acu, acd, acl, acr):

        self.s = s
        self.d = d
        self.ms = ms
        self.acu = acu
        self.acd = acd
        self.acl = acl
        self.acr = acr   
    
    def run(self):
        s = self.s
        d = self.d
        ms = self.ms
        acu = self.acu
        acd = self.acd
        acl = self.acl
        acr = self.acr
        stat = "ogp"
        x = 'x'
        y = 'y'
        z = 'z'

        acu1 = ms * acu
        acd1 = ms * acd
        acl1 = ms * 1.25
        acr1 = ms * acr
        i = int(0)

        if d =='u':
            self.countdown = acu1
        if d =='d':
            self.countdown = acd1
        if d =='l':
            self.countdown = acl1
        if d =='r':
            self.countdown = acr1

        acms = self.countdown
        
        while i < acms:
            i = i + 1
            time.sleep(.001)

        if d == 'u':
            s.write('8')
        if d == 'd':
            s.write('8')
            
        if d == 'l':
            s.write('3')
        if d == 'r':
            s.write('3')




if __name__ == '__main__'  :
    foo = so(2)
    foo.histo()
    foo.run()
else:
   pass



