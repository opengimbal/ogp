## OGP Class Library 1
## contains MAP(so), CHASE, ACX, & HUD

#!/usr/bin/env python2
# ogp4.py

## LIBRARIES IN USE

import time
import serial
import os
import ircam    ## our library
import picamera

from SimpleCV import Camera, Image

## ENVIRONMENT VARIABLES are likely not in use since this isn't main module.

## for Mapping
mySet = set()
brightpixels = 0   ## these are couter-intuitive and might need to be switched
darkpixels = 0
l = int(4)
s = serial.Serial('/dev/ttyUSB0', 9600)



class so(object):    ## aka Mapper    (btw this is broken, it gets to frame 4 and stops dropping thumbnails)

    def __init__(self, side, m, js, wsh, wsh2):  ## this definition gets your variables to become available
        self.ms = m     ## milliseconds of movement
        self.js = js    ## name of the javascript framebuffer for image out
        self.wsh = wsh  ## a redundant variable i accidentally created. wsh always equals "tornado.websocket.WebSocketHandler"
        self.wsh2 = wsh2 ## wsh2 is the name of the current instance of the main loop
        self.m = m   ## is depricated, probably isnt used anymore
      ##  self.c = c
        self.l = side   ## size of the map in units squared
        self.brightpixels = 11   ## this becomes the size of the dark side of the histogram readout
        self.darkpixels = 11   ## this variable becomes size of the bright side of the histogram readout
        self.x = 0  ## x axis location on grid
        self.y = 0    ## y axis location on grid
        self.w = 0  ## is histogram info for display on the viewfinder
        self.p = 1   ## is the picture number
        

        l = self.l   ## size of side packed away
        x = -1      ## reset of the map happens here
        y = -1      

        self.countdownA = int(self.l)   ## these three counters control the back and forth sweeping motion
        self.countdownB = int(self.l)     ## first they are loaded with the size of the intended map
        self.countdownC = -1          
        


    def histo(self):    ## performs a histogram on the image and saves image and thumb in the image and thumb folders
    
    ## so... declare your variable states
        i = 0      ## will become the counter of histogram cross sections
        js = self.js   ## is the image output socket
        ms = self.ms   ## stepsize
        w = self.w   ## z axis info for future use
       ## c = self.c
        cent = 0   ##  for use with blob detector section
        rgb1 = 0   ## for use with blob detector section

        brightpixels = 0    ## zero out the function
        darkpixels = 0
        wsh = self.wsh 
        wsh2 = self.wsh2
        s.write('s')
        stat = "ogp - mapping"
        
    ##begin the machine...
    ## first a picture is taken
        
        with picamera.PiCamera() as camera:
            camera.resolution = (544, 288)
            camera.capture('imagesmall.jpg')
        img1 = Image('imagesmall.jpg')

        time.sleep(1) ## BUFFERING POSSIBLY UNNECESSARY
        ##img1.save(d)
        hist = img1.histogram(20)    ## histogram will have 20 cross sections

        while i < 20:    ## this iterates through the cross sections
            if (i < 10):  ## histogram produces a line graph of light to dark ratios, 10 is halfway through the graph
                darkpixels = darkpixels + hist[i] ## seems backwards i know. this part needs refinement but
                self.darkpixels = darkpixels  ## it has seemed to work
            else:
                brightpixels = brightpixels + hist[i]   ## the opposite for testing purposes
                self.brightpixels = brightpixels    ## saves away this data
            i = i + 1   ## moves you forward one cross section at a time 

        if (darkpixels > 0):  ## if you have a "bright" image then all this happens...
            print "bright"
            x = self.x
            y = self.y
            w = darkpixels
            p = self.p
            p = p + 1
            self.w = darkpixels
            z = w
         
            thumbnail = img1.crop(100,0,300,300)     ## make a thumbnail
##            thumbnail = thumbnail.dilate(10)   ##this wouild kind of amplify the light 
            thumbnail = thumbnail.scale(20,20)

            thumb1 = "/var/www/images/thumbs/thumb"  ## name the thumbs location
            thumb3 = ".png"
            thumbpath = thumb1 + str(p) + thumb3
            thumbnail.save(thumbpath)    ## and save it

            hud1 = hud(img1, js, stat, x, y, z)   ## send image away for processing (then sending to client)
            hud1.run()   

            blobs = img1.findBlobs()                            ## get blob info of image
            time.sleep(1)
            if blobs :    ## draw the indicators
                img1.drawCircle((blobs[-1].x,blobs[-1].y),30,color=(255,255,255))
                img1.drawCircle((blobs[-1].centroid()),10,color=(255,100,100))
                print blobs[-1].meanColor()                    ## get info from the blob centroid
                rgb1 = blobs[-1].meanColor()
                cent = blobs[-1].centroid()

            
            pth1 = "/var/www/images/image"                    ## save image
            pth3 = ".png"
            pth = pth1 + str(p) + pth3
            print pth
            img1.save(pth)
            
            apath = os.path.abspath(pth)                ## some debugging
            ##wsh.write_message(wsh2, str(apath) )

            self.p = p ## p is the pic number
            
            mySet.add((p,x,y,w,cent,rgb1))   ## these two lines collect up your current info 
            self.mySet = mySet                 ## and add it into a large set of info 
            
            wshx = str(self.x)             #this is the data that is about to get socketed to the client
            wshy = str(self.y)
            ## d commands the client to draw a thumb into its html5 canvas
            ## x and y are the location of the thumb on the map, and p is the image reference number
            wsh.write_message(wsh2, "d_" + wshx + "_" + wshy + "_" + str(p) )   
            wsh.write_message(wsh2, "rgb_" + str(rgb1))    ## rgb data
            wsh.write_message(wsh2, "x_" + str(cent) )    ## centroid data

        else:    ## if the frame is dark then pretty much nothing happens
            wshx = str(self.x)  
            wshy = str(self.y)
            wsh.write_message(wsh2, wshx + " " + wshy + "dark")
            print "dark"


    def run(self):     ## when a map is begun, this definition more or less...
        wsh = self.wsh   ## draws the line that goes back and forth to complete the
        wsh2 = self.wsh2  ## square of any given size.
        acu = int(1)  ## this is the auto-calibrate function
        acd = int(1)
        acl = int(1)
        acr = int(1)
        countdownA = self.countdownA   ## load the current mapsize
        countdownB = self.countdownB    
        countdownC = self.countdownC
        ms = self.ms   ## movement in milliseconds
        x = self.x   ## x and y coordinates
        y = self.y
        
        if countdownA > 0:                      ## heres where the madness begins
            if countdownC == 1:               ## describing a cascading series of countdowns
                countdownB = int(self.l)     ## that make a grid. 
                countdownC = -1
                print "down"
                d = 'd'                                         ## so that acx knows we're going direction down
                s.write('9')                                    ## triggers the down motor to run open 
                mov = acx(s, d, ms, acu, acd, acl, acr)   ## acx is a timer, it pauses and then stops the motor
                mov.run()
                y = y - 1                 ## bring the position up to date
                self.y = y              
                time.sleep(1)            ## buffering possibly uneccessary
                elf = self.histo()         ##   elves bring you the histogram info
                time.sleep(1)                 ## more buffering
                countdownA -=1                   ## iterate though the countdown
                wsh.write_message(wsh2, "m" )    ## sending an "m" to the client causes the mapping to continue another step
                
                self.countdownA = countdownA   ## update our counters
                self.countdownB = countdownB
                self.countdownC = countdownC
                
            if countdownC > 1:       ## same as before but left now
                print "left"
                countdownC -= 1
                d = 'l'
                s.write('2')
                mov = acx(s, d, ms, acu, acd, acl, acr)
                mov.run()
                x = x - 1
                self.x = x
                time.sleep(1)
                elf = self.histo()
                s.write('s')
                time.sleep(1)
                wsh.write_message(wsh2, "m" )
                        
                self.countdownA = countdownA
                self.countdownB = countdownB
                self.countdownC = countdownC
            
            if countdownB == 1:   ## same as before but "right" now
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
                time.sleep(1)
                countdownA -=1
                wsh.write_message(wsh2, "m" )
                self.countdownA = countdownA
                self.countdownB = countdownB
                self.countdownC = countdownC
                print self.l                        ##debugging
                print countdownC
                print self.countdownC
                
            if countdownB > 1:       ## same as before but right...
                print "right"     ## you'll notice that these four parts actually happen in reverse order.
                countdownB-=1     ## the mapper moves right first... until counter B runs down. 
                d = 'r'
                s.write('4')
                mov = acx(s, d, ms, acu, acd, acl, acr)
                mov.run()
                s.write('s')
                s.write('j')
                x = x + 1
                self.x = x
                time.sleep(1)
                elf = self.histo()
                time.sleep(1)
                wsh.write_message(wsh2, "m" )
                
                self.countdownA = countdownA       ## updates all counters
                self.countdownB = countdownB
                self.countdownC = countdownC

        else:                            ## if its done mapping then this should happen
            wsh = self.wsh
            wsh2 = self.wsh2
            wsh.write_message(wsh2, str(mySet) )  ## outputs the entire set of data all at once
            print "done"



class chase(object):      ## CHASE the Blob !!
    def __init__(self, js, wsh, wsh2):     ## these variables allow for websocket communications on both channels
        self.js = js
        self.wsh = wsh
        self.wsh2 = wsh2
        ##self.c = c
    
    def run(self):
        s.write('s')
        wsh = self.wsh
      ##  c = self.c
        js = self.js
        wsh2 = self.wsh2
        ms = 50         ## nudge size
        d = "n"
        acu = int(1)    ## autocalibration settings
        acd = int(1)
        acl = int(1)
        acr = int(1)
        irpic = pinoir2(js)   ## needs more arguments now -- should get a pic and drop it

        img1 = Image('imagesmall.jpg')  ##pic your image back up
        
        blobs = img1.findBlobs()   ##  get blob info on image
        if blobs :                  ##  if blobs then draw the centroid indicators
            img1.drawCircle((blobs[-1].x,blobs[-1].y),30,color=(255,255,255))
            img1.drawCircle((blobs[-1].centroid()),10,color=(255,100,100))
        

            blobx1 = blobs[-1].x    ## save centroid data as variables
            bloby1 = blobs[-1].y

            print blobx1    ## debug
            print bloby1
        
            img1.drawText("ogp: tracking", 10, 10, fontsize=50)     ##  draw onto the image
            img1.drawText(str(blobx1), 10, 200, color=(255,255,255), fontsize=50)
            ##img1.drawText(str(bloby1), 50, 200, color=(255,255,255), fontsize=50)
            img1.drawText(str(bloby1), 10, 250, color=(255,255,255), fontsize=50)
            img1.save(js.framebuffer)      ##  send the image to the client
           ## time.sleep(1)

            if blobx1 > 300:     ## if the blob is to the right of pixel 300
                d = 'r'      ## then the motor nudges right
                s.write('4')  ## sets the motor to run open and to the right
                mov = acx(s, d, ms, acu, acd, acl, acr)  ## acx is a timer that waits and then stops the motor
                mov.run()
            if blobx1 < 260:   ## to the left
                d = 'l'
                s.write('2')
                mov = acx(s, d, ms, acu, acd, acl, acr)
                mov.run()
            if bloby1 > 180:   ## down
                d = 'd'
                s.write('9')
                mov = acx(s, d, ms, acu, acd, acl, acr)
                mov.run()
            if bloby1 < 140:   ## up
                d = 'u'
                s.write('6')
                mov = acx(s, d, ms, acu, acd, acl, acr)
                mov.run()
            
            wsh.write_message(wsh2, "c_" + str(d) + "_" + str(bloby1) )   ## relays chasing info and triggers the next round of chasing

        else:
            wsh.write_message(wsh2, "c_" + "null" )  ## if theres no blob then relay that info and trigger next round of chasing



class autocal(object):                                ## when you press the AC button this class is supposed to 
    def __init__(self, js, wsh, wsh2):            ##  gather autocalibrate data from a single 
        self.js = js                            ## blob centroid. preferably a star.
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
        irpic = pinoir2(js)                                  ## it takes a pic...

        img1 = Image('imagesmall.jpg')   
        blobs = img1.findBlobs()
        img1.drawCircle((blobs[-1].x,blobs[-1].y),30,color=(255,255,255))
        img1.drawCircle((blobs[-1].centroid()),10,color=(255,100,100))
        acx1 = blobs[-1].x                                    ## grabs the centroid data...
        acy1 = blobs[-1].y


        img1.drawText("ogp: autocalibrating", 10, 10, fontsize=50)
        img1.drawText(str(acx1), 10, 50, color=(255,255,255), fontsize=20)
        img1.drawText(str(acy1), 10, 75, color=(255,255,255), fontsize=20)
        img1.save(js.framebuffer)                             ## sends marked up image to client...
        
        d = 'r'                                               ## it moves..
        ms = 50
        s.write('4')
        mov = acx(s, d, ms, acu, acd, acl, acr)
        mov.run()
            
        time.sleep(1)

        img1 = c.getImage()                                   ## gets another image...
        blobs = img1.findBlobs()
        img1.drawCircle((blobs[-1].x,blobs[-1].y),30,color=(255,255,255))
        img1.drawCircle((blobs[-1].centroid()),10,color=(255,100,100))
        acx2 = blobs[-1].x                                  ## gets the new centroid data...
        acy2 = blobs[-1].y

        
        img1.drawText("ogp: autocalibrating", 10, 10, fontsize=50)
        img1.drawText(str(acx1), 10, 50, color=(255,255,255), fontsize=20)
        img1.drawText(str(acy1), 10, 75, color=(255,255,255), fontsize=20)        
        img1.drawText(str(acx2), 40, 50, color=(255,255,255), fontsize=20)
        img1.drawText(str(acy2), 40, 75, color=(255,255,255), fontsize=20)
        img1.save(js.framebuffer)                           ## and sends the new image to the client...
        
        d = 'd'                               ## it moves again and so on... in the 4 directions
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
           ##outputs info to the socketed client field
        wsh.write_message(wsh2, "x_" + str(cal1) + "_" + str(cal2) + "_" + str(cal3)+ "_" + str(cal4) )


class hud2(object):       ## this has been replaced by pinoir2
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

class hud(object):    ## this is image post production for the histogram
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


class acx(object):        ## acx is supposed to adjust the stepsize according to the 4 ac variables
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
        acl1 = ms * acl
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




if __name__ == '__main__'  :       ## this isn't the main module so this part won't happen
    foo = so(2)
    foo.histo()
    foo.run()
else:
   pass

