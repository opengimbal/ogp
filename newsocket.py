#!/usr/bin/env python2         
# newsocket.py

## uncomment above for autorun at boot------

## OGP Telescope  --  Main Module  -- newsocket.py
## this file is just a switchboard attached to a tornado web socket
## the socket is in communication with the client 
## or many clients at once, i havent tested more than 3

## LIBRARIES 

import tornado.httpserver  ## you will have previously installed these libraries
import tornado.websocket  
import tornado.ioloop
import tornado.web
import time  ## comes with python so doesnt need installing
import serial
import picamera
from SimpleCV import *
import os   ## comes with python so doesnt need installing
## our libraries
from ogp4 import *
import ircam

## some important variables

s = serial.Serial('/dev/ttyUSB0', 9600)                     ## serial to arduino

c2 = SimpleCV.Camera(0,{ "width": 544, "height": 288 })          ## opens a camera
##c = SimpleCV.Camera(1,{ "width": 544, "height": 288 })           ## or two
js = SimpleCV.JpegStreamer('0.0.0.0:8080')                        ## opens socket for jpeg out
time.sleep(4)                                               ## strategic buffering, possibly unnecessary
c2.getImage().save(js.framebuffer)                 ## push a jpeg to the jpeg socket

cam_mode = int(1)   ## set default cam mode there are currently 3. named 1, 2, and 3

##autocalibration
acu = int(1)   ## up and down integers team up to form a fraction 
acd = int(1)  ## if it takes 3 downs to make 1 up then thats their relation
acl = int(1)  ## same with left and right
acr = int(1)

showimage = int(1)  ## this is for the "next" and "previous" buttons on the client
mapsize = int(8)  ## buttons control this
stepsize = int(100)  ## same here

stat = "ogp"   ##status is info relayed through the system to the main display, it can be anything
s.write('3')  ## send a serial command through to the motor control, 3 means stop x axis movement
s.write('8')  ##  8 is stop Y axis movement




class WSHandler(tornado.websocket.WebSocketHandler):  ## this is the switchboard / serial text socket

    def open(self):    ## socket open event
        print 'New connection was opened'  ## this prints into the python command prompt 
        self.write_message("telescope listening")   ## sends message through serial text socket
        x = int(0)  ## x y and z will get passed along to all classes. always with the un-packing...
        y = int(0)
        z = int(0)
        self.x = 0 ## and then the packing again... this makes all info up to date and accessible 
        self.y = 0
        self.z = 0
        self.mapsize = mapsize  ## these variables also get passed along when necessary, as arguments etc...
        self.showimage = showimage
        self.stepsize = stepsize
        self.cam_mode = cam_mode  ## there are currently 3. named 1, 2, and 3
        

    def on_message(self, message):   ## heres where the switchboard begins

        print 'Incoming message:', message      ## output message to python command prompt 
        showimage = self.showimage      ## unpacking variables
        mapsize = self.mapsize
        stepsize = self.stepsize
        x = self.x
        y = self.y
        z = self.z
        stat = "ogp"
        cam_mode = self.cam_mode

        
        if message =='j':                ##  switches for incoming socket events look like this, this one nudges the telescope to the right
            print "j"                       ## debug talkback
            x = x + 1                     ## since we're nudging right 
            self.x = x                    ## packing the changed variable away
            self.write_message("echo: " + message + " right " )          ## debug talkback to client
            d = 'r'                               ## d direction is r right
            ms = 50                               ## milliseconds to move
            s.write('4')                      ## python debug talkback
            mov = acx(s, d, ms, acu, acd, acl, acr)      ## instantiate an instance of the move command, acx.
            mov.run()                                       ## run that instance
            irpic = ircam.pinoir2(js, cam_mode, c2, x, y, z, stat)    ## instantiate instance of camera command
            irpic.run()                                        ## run the instance

        if message =='c3':               ## c3, this is the switch to camera mode 3
            cam_mode = 3                              ## set that mode
            self.cam_mode = cam_mode                     ## pack it away
            img1 = c2.getImage()                 ## get an image from c2 which is the secondary camera (webcam)
            blobs = img1.findBlobs()                   ## get blob info off the new pic using simpleCV process 
            if blobs:                                ## this draws your "blob centroid" indicators
                img1.drawCircle((blobs[-1].x,blobs[-1].y),30,color=(255,255,255))
                img1.drawCircle((blobs[-1].centroid()),10,color=(255,100,100))
                rgb1 = blobs[-1].meanColor()              ## this stores your centroid rgb data
                cent = blobs[-1].centroid()               ## this stores your centroid x and y data

            img1.drawText(str(stat), 10, 10, fontsize=50)     ## this is how we draw text data onto the image
            img1.drawText(str(x), 10, 70, color=(255,255,255), fontsize=25)
            img1.drawText(str(y), 10, 100, color=(255,255,255), fontsize=25)
            img1.drawText(str(z), 10, 230, color=(255,255,255), fontsize=15)
            img1.drawText(str(cent), 10, 250, color=(255,255,255), fontsize=15)
            img1.drawText(str(rgb1), 10, 270, color=(255,255,255), fontsize=15)
            
            img1.save(js.framebuffer)       ## saves the finished image to the clients socketed iframe display 
            self.write_message("echo: " + message + " " + str(cam_mode) )   ## debug talkback to client    

        if message =='c2':     ##   cam mode 2 works similarly
            cam_mode = 2
            self.cam_mode = cam_mode
            irpic = ircam.pinoir2(js, cam_mode, c2, x, y, z, stat)     ## this mode is the super high res
            irpic.run()
            self.write_message("echo: " + message + " " + str(cam_mode) )    ## client debug talkback

        if message =='c1':       ## same as last switch except it produces a low res picam output
            cam_mode = 1
            self.cam_mode = cam_mode
            irpic = ircam.pinoir2(js, cam_mode, c2, x, y, z, stat)
            irpic.run()
            self.write_message("echo: " + message + " " + str(cam_mode) )    

        if message =='h':    ## this switch is for nudging left. works same as previous nudge switch (above)
            print "h"
            s.write('h')
            x = x - 1
            self.x = x
            self.write_message("echo: " + message + " left" )
            d = 'l'
            ms = 50
            s.write('2')
            mov = acx(s, d, ms, acu, acd, acl, acr)
            mov.run()
            irpic = ircam.pinoir2(js, cam_mode, c2, x, y, z, stat)
            irpic.run()

            
        if message =='+':                              ## increases stepsize by 25
            print "+"
            stepsize = self.stepsize
            stepsize = stepsize + 25
            self.write_message("echo: " + str(stepsize) + " stepsize plus" )
            self.stepsize = stepsize
            
        if message =='-':                              ## decreases stepsize
            print "-"
            stepsize = self.stepsize
            stepsize = stepsize - 25
            self.write_message("echo: " + str(stepsize) + " stepsize minus" )
            self.stepsize = stepsize

        if message =='p':                           ## increases mapsize by 1
            stat = "mapsizing"
            print "p"
            mapsize = mapsize + 1
            self.mapsize= mapsize
            self.write_message("echo: " + message + " mapsize " + str(mapsize))

        if message =='l':         ## decreases mapsize by 1
            stat = "mapsizing"
            print "l"
            mapsize = mapsize - 1
            self.mapsize = mapsize
            self.write_message("echo: " + message + " mapsize " + str(mapsize))
            
            
        if message =='y':   ## nudge up
            print "y"
            y = y + 1
            self.y = y
            self.write_message("echo: " + message + " up   ")
            d = 'u'
            ms = 50
            s.write('6')
            mov = acx(s, d, ms, acu, acd, acl, acr)
            mov.run()
            irpic = ircam.pinoir2(js, cam_mode, c2, x, y, z, stat)
            irpic.run()

        if message =='g':   ## nudge down
            print "g"
            y = y - 1
            self.y = y
            self.write_message("echo: " + message + " down   ")
            d = 'd'
            ms = 50
            s.write('9')
            mov = acx(s, d, ms, acu, acd, acl, acr)
            mov.run()
            irpic = ircam.pinoir2(js, cam_mode, c2, x, y, z, stat)
            irpic.run()

        if message =='z':                                          ## map step --- down
            stat = "mapping down"                       ## the next 4 switches work the same way
            print "z - map down"
            y = y - 1                                                 ## adjust your current position
            self.y = y                                                        ## and pack it away
            self.write_message("echo: " + message + " map down   ")           ##  relay info to client talkback debug
            d = 'd'                                                      ## the d direction is d down
            ms = stepsize                                                 ## whatever stepsize is currently
            s.write('9')                                        ## turns the motor on 
            mov = acx(s, d, ms, acu, acd, acl, acr)      ## acx, waits a short time period (stepsize) in milliseconds
            mov.run()                                       ## and then stops the motor automatically 
            irpic = ircam.pinoir2(js, cam_mode, c2, x, y, z, stat)    ## then this command takes the pic 
            irpic.run()            ## run the instance, fool

        if message =='a':                                   ##   same as above but to the left
            stat = "mapping left"
            print "a- map left"
            x = x-1
            self.x = x
            self.write_message("echo: " + message + " map left   ")
            d = 'l'
            ms = stepsize
            s.write('2')
            mov = acx(s, d, ms, acu, acd, acl, acr)
            mov.run()
            irpic = ircam.pinoir2(js, cam_mode, c2, x, y, z, stat)
            irpic.run()

        if message =='w':        ## up
            stat = "mapping up"
            print "w- map up"
            y = y + 1
            self.y = y
            self.write_message("echo: " + message + " map up   ")
            d = 'u'
            ms = stepsize
            s.write('6')
            mov = acx(s, d, ms, acu, acd, acl, acr)
            mov.run()
            irpic = ircam.pinoir2(js, cam_mode, c2, x, y, z, stat)
            irpic.run()

        if message =='s':    ## right
            stat = "mapping right"
            print "s- map right"
            x = x + 1
            self.x = x
            self.write_message("echo: " + message + " map right   ")
            d = 'r'
            ms = stepsize
            s.write('4')
            mov = acx(s, d, ms, acu, acd, acl, acr)
            mov.run()
            irpic = ircam.pinoir2(js, cam_mode, c2, x, y, z, stat)
            irpic.run()

        if message =='b':           ## MAPPER -- start making a map!
            print "b"
            self.write_message("echo: " + message + " map" )        
            m = stepsize                                      ## get the current stepsize
            wsh = tornado.websocket.WebSocketHandler        ## wsh holds some socket info for no reason whatsoever
            wsh2 = self                     ## wsh2 holds the name of the instance of the current websocket server. 
            map = self.map     
            map.run()                                       ##  histogram is necessary before run!

        if message =='n':                         ## MAPPER -- make a new instance of a map before running one
            print "n"
            self.write_message("echo: " + message + " map" )
            print stepsize
            m = stepsize
            wsh = tornado.websocket.WebSocketHandler        ## wsh holds some socket info
            wsh2 = self                                    ## wsh2 holds the name of the instance  
            map = so(mapsize, m, js, wsh, wsh2)               ##  make an istance of the mapper --SO stands for seek out 
            self.map = map
            map.histo()                                   ##  histogram is necessary before starting a new map
           ## print map.mySet                      ## print map log data array

        if message == 'c':       ## CHASE a blob !
            wsh = tornado.websocket.WebSocketHandler        ## wsh holds some socket info
            wsh2 = self                                    ## wsh2 holds the name of the instance ... the instance we exist in now
            cchase = chase(js, wsh, wsh2)   ## just needs those args and js which names the jsframebuffer( aka image socket)
            cchase.run()

        if message == 'k':    ## AutoCalibrate motors based on camera feedback   -- is disabled
            wsh = tornado.websocket.WebSocketHandler        ## wsh holds some socket info
            wsh2 = self                                    ## wsh2 holds the name of the instance  
       ##     ac = autocal(c, js, wsh, wsh2)
      ##      ac.run()
      
        if message == 'x':       ##  previous image button -- gets image from the folder and diplays it
            showimage = showimage - 1                ## 0 minus 1 equals a bug probably
            self.showimage = showimage               ## pack away the current image number
            pth1 = "/var/www/images/image"              ## path to image --string part 1
            pth3 = ".png"                                ## string part 3
            pth = pth1 + str(showimage) + pth3               ## concatonate image string (address) 
            apath = os.path.abspath(pth)              ##i was using this handy line to debug my path
            self.write_message(pth)          ## debug to client 
            print showimage       ## debug to python shell
            img1 = Image(pth)      ## get the image according to our new path
            img1.save(js.framebuffer)     ## output that image to the clients main viewer

            
        if message == 'v':        ## next image button -- works the same as the previous
            showimage = showimage + 1
            self.showimage = showimage
            pth1 = "/var/www/images/image"
            pth3 = ".png"
            pth = pth1 + str(showimage) + pth3
            apath = os.path.abspath(pth)
            self.write_message(pth)
            print showimage
            img1 = Image(pth)
            img1.save(js.framebuffer)
##

        if message =='t':     ## FOCUS buttons
            print "t"       
            s.write('t')      ## this serial command to arduino starts the focus motor running.
            time.sleep(.25)   ## the system waits .25 milliseconds
            s.write('c')     ## and then stops the motor.
            self.write_message("echo: " + message + " focus out")   
            
        if message =='f':      ## here we have just the same but in the opposite direction
            print "f"
            s.write('f')
            time.sleep(.25)
            s.write('c')

            self.write_message("echo: " + message + " focus in")            


        if message =='2':  ## OPEN GEAR - Directional Buttons
            print "2"
            s.write('2')  ## this serial command to the arduino turns the motor on left, at which point you need to stop it manually
            self.write_message("echo: " + message + " 2")

        if message =='3':   ##STOP X axis motor 
            print "3"
            s.write('3')    ## this serial command to the arduino stops the x axis motor
            self.write_message("echo: " + message + "3")   
            irpic = ircam.pinoir2(js, cam_mode, c2, x, y, z, stat)   ## and then it relays a picture to the viewer
            irpic.run()


        if message =='4':     ## same as   "3" but in the opposite direction - right
            print "4"         
            s.write('4')     ## sets the x axis motor to running right, at which point you will need to stop it manually
            self.write_message("echo: " + message + "4")
            

        if message =='7':    ## same as the previous open directionals except that this one should be UP or DOWN, depending.
            print "7"
            s.write('6')     ## the nature of the pulley makes it difficult to determine which direction this will take you
            self.write_message("echo: " + message + " 7")   ## so be ready to hit the stop Y button


        if message =='8':      ##    STOP Y is the same as stop x
            print "8"
            s.write('8')
            self.write_message("echo: " + message + " 8")
            irpic = ircam.pinoir2(js, cam_mode, c2, x, y, z, stat)
            irpic.run()


        if message =='9':
            print "9"
            s.write('9')
            self.write_message("echo: " + message + " 9")



    def on_close(self):                       ##  if you lose the socket
        print 'Connection was closed...'

application = tornado.web.Application([        ##creates instance of socket
    (r'/ws', WSHandler),                 
])


if __name__ == "__main__":                       ##    since this is the main module
    http_server = tornado.httpserver.HTTPServer(application)      ## opens the socket
    http_server.listen(8888)                                     ## on this port
    tornado.ioloop.IOLoop.instance().start()        ##   this starts the threaded socket loop
        
