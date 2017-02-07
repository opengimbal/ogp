##!/usr/bin/env python2         
## newsocket.py

## uncomment above for autorun at boot------

## OGP Telescope  --  Main Module

## LIBRARIES 

import tornado.httpserver  
import tornado.websocket
import tornado.ioloop
import tornado.web
import time
import serial
import picamera
from SimpleCV import *
import os
## our library
from ogplab import *
import ircam
from chase2 import *
import ephem

## some important variables


s = serial.Serial('/dev/ttyUSB0', 9600)                     ## serial to arduino

c = SimpleCV.Camera(0,{ "width": 544, "height": 288 })          ## opens a camera
c2 = c           ## or two
js = SimpleCV.JpegStreamer('10.0.10.149:8080') ## set to ip of pi
time.sleep(4)                  ## strategic buffering, possibly unnecessary
img1=c.getImage()                 ## push a jpeg to the jpeg socket
img1.drawText("Hello", 10, 5, fontsize=40)  ## init data written on image in web ui
img1.save(js.framebuffer)   ## writes image to where the iframe can display it in web ui
cam_mode = int(1) ## sets which camera mode you begin in


showimage = int(1) ## start image for leafing thru images with commands
mapsize = int(10) ## denotes the number of steps that the map function grows out to

stat = "ogp"  ## stat variable on web ui image updates as functions are used
sqx = int(272) ## denotes start point on html5 canvas map when you run the mapping function
sqy = int(144) ## same as sqx but for the Y dimension
vs = VideoStream("/var/www/html/vid.avi", 15, False) ##creates a file for video frame recording

moon = ephem.Moon() ## initializes Moon object from piephem library to find moon coordinates 
orlando = ephem.Observer() ## initializes a location object in piephem
orlando.lat = '28.41'  ## latitude data for orlando florida
orlando.lon =  '-81.29'   ## longitudinal data for orlando florida


class WSHandler(tornado.websocket.WebSocketHandler):   ## object that creates tornado wesocket for web ui serial interface 
    def check_origin(self, origin):     ##required for new tornado security bypass
        return True   ## required by library

    def open(self):  ## opens new connection to web ui
        print 'New connection was opened 1'  
        self.write_message("telescope listening")   ## sending message through text socket
	## the next 6 variables keep track of motor movements
        x = int(0) ## map x coordinate starting point  
        y = int(0) ## map y coordinate starting point
        z = int(0) ## focus data starting point
        self.x = 0 ## later on self.x will equal x (scoping)
        self.y = 0 ## same deal as self.x
        self.z = 0 ## same deal as self.x
	## NERTH: x,y,z is in scope of .OPEN()

        self.live = False  ## toggles live image update function on and off
        self.mapping = False ## toggles map making function on an off
        self.mapsize = mapsize ## passing global mapsize to this object
        self.showimage = showimage ## passing starting image leafing number reference to object scope
        self.cam_mode = cam_mode ## passes starting camera mode state from global to object scope
        self.sqx = sqx ## sqx is the ui keyhole square location variable from global to object scope
        self.sqy = sqy ## same thing as sqx on last line
        ##s.write('n')  ## requests alt-az info from arduino sensor
        time.sleep(2)  ## buffering to allow sensor to work
        ##self.write_message(s.readline()) ## prints alt-az into web ui serial
        
        

    def on_message(self, message): ## when a message is recieved...

        print 'Incoming message:', message      ## output message to python
        if message.isdigit():  ## if this message contains numerical digits
            digits = int(message) ## stores parsed digits into a variable
            print 'digits_'+ str(digits)  ## debug data forr python
            if digits>9: ## digits one thru nine are dangerous open motor commands when passed to arduino
                s.write('x'+ str(digits)) ## x is the header for the serial string that gets parsed in the arduino as "gotoy" function coordinates
                ## gotoy function on arduino makes the motors work with the sensor to find requested alt-az coordinates
        msgsplit = message.split("_")  ## parses recieved serial packet -- '_' is the divider 
        print msgsplit[0]  ## prints the parsed out header
        
        showimage = self.showimage ## updates the number of the imaged shown for leafing commands
        mapsize = self.mapsize  ## updates current mapping function image number into this iteration
        x = self.x  ## updates current map x variable into this interation
        y = self.y ## same
        z = self.z ## same
        stat = "ogp"   ## stat denotes current function name on image that gets sent to web ui
        sqx = self.sqx  ## updates keyhole square location into this interation 
        sqy=self.sqy   ## same as last but for y
        cam_mode = self.cam_mode ## updates camera mode into this iteration
        wsh2=self  ## creates self object handle --  this is so i can pass serial info later thru the wsh socket from the next function 
        live = self.live ## updates live image updater toggle switch
        mapping = self.mapping ## updates map function toggle switch

        if msgsplit[0] == 'moon':  ## if header of packet equals the word 'moon'
            print "moon"
            
            client_utc = str(msgsplit[1] + " " + msgsplit[2])   # concatonates moon string universal time code into usable string
            print client_utc   
	    d = ephem.Date(client_utc)  ## creates piephem date object
            orlando.date = d  ## creates date and location variable
            print d
            moon.compute(orlando)  ## gets output from piephem library call
            moonaz = str(moon.az)  ## breaking out the piephem output for moon location azimuth
            moonalt = str(moon.alt) ## breaking out the altitude
            ticks = str(time.time()) ## breaks out the time info
            moonpoz = str("MOON_POS_ALT_" + moonalt +"__AZ_"+ moonaz)  ## concatinates current moon position data for output to web ui
            self.write_message("moon_" + moonalt + "_" + moonaz )  ## sends current moon position to web ui
            self.write_message("time_" + client_utc) ## send time data to web ui

            with picamera.PiCamera() as camera:   ## with pi camera 
                camera.resolution = (544, 288)    ##  at this resolution
                camera.capture('imagesmall.jpg')   ##  put image here
            img1 = Image('imagesmall.jpg')  ## load captured image into variable
            ##img1 = c.getImage()  ##  get image from logitech web cam
            img1.drawText(str("CLIENT_TIME_" + client_utc+"_Orlando_FL"), 10, 30, color=(255,255,255), fontsize=30) ## write data on image
            img1.drawText(str(moonpoz), 10, 5, color=(255,255,255), fontsize=30) ## write data on image
            if moon.alt < 0:    ## if moon is above the horizon
                img1.drawText(str("MOON BELOW HORIZON"), 10, 55, color=(255,255,0), fontsize=30)  ## write moon un-availabilty on image
            img1.save(js.framebuffer) ## push image to iframe in web ui
            
            moonaz2 = moonaz.split(":")  ## divides up the pi ephem output into usable variables
            moonalt2 = moonalt.split(":") ## same
            print moonaz2[0]  
            print moonalt2[0]

            moonalt3 = moonalt2[0]  ## parsed moon altitude from piephem output
            if moonalt3 >= 12:  ## 12 is the lowest altitude for mechanical safety buffer
                moonalt4 = "x"+ str(moonalt3)  ## concatonates command arduino to find these coordinates using motor sensor loop (gotoy)
##                s.write(moonalt4)  ## send command to arduino
                

##            moonaz3 = moonaz2[0]  ## grabs azimuth output from pi ephem output
##            if moonaz3 >= 3:   ## mechanical buffer for azimuth (compass)
##                moonaz4 = int(moonaz3) + 100   ## add 100 to pass an azimuth request
##                s.write(moonaz4)  ## command arduino to find azimuth
        
        if message =='j':            ##    switches for incoming socket events
            print "j"    
            x = x + 1    ## mapping movement goes right   
            self.x = x  ## passes movement change to object scope
            self.write_message("echo: " + message + " right " )  ## talkback to web ui  
            s.write('s')  ## tells aduino to move right one 'step'
            time.sleep(.5)  ## wait for motor to move
            irpic = ircam.pinoir2(js, cam_mode, c2, x, y, z, stat,sqx,sqy,s,wsh2,c)  ## create camera function instance
            irpic.run()  ## runs camera function instance
        
        if message =='c3':  ## changes which camera is current camera in use
            cam_mode = 3  ## mode 3 is the logitech webcam
            self.cam_mode = cam_mode   
            img1 = c2.getImage()  ## get image from logitech webcam
            blobs = img1.findBlobs()  ## simple cv finds the strongest color blob
            if blobs:
                img1.drawCircle((blobs[-1].x,blobs[-1].y),30,color=(255,255,255))  ## circle shows you the blob location on the image
                img1.drawCircle((blobs[-1].centroid()),10,color=(255,100,100)) ## this one shows the centroid of the blob
                rgb1 = blobs[-1].meanColor() ## gets rgb data of blob
                cent = blobs[-1].centroid()  ## puts centroid data into a variable

                img1.drawText(str(stat), 10, 10, fontsize=50)  ## writes status data onto image
                img1.drawText(str(x), 10, 70, color=(255,255,255), fontsize=25) ##
                img1.drawText(str(y), 10, 100, color=(255,255,255), fontsize=25)
                img1.drawRectangle(sqx,sqy,25, 25,color=(255,255,255))

                img1.drawText(str(z), 10, 230, color=(255,255,255), fontsize=15)
                img1.drawText(str(cent), 10, 250, color=(255,255,255), fontsize=15)
                img1.drawText(str(rgb1), 10, 270, color=(255,255,255), fontsize=15)
            img1.save(js.framebuffer)
            self.write_message("echo: " + message + " " + str(cam_mode) )    

        if message =='c2':
            cam_mode = 2
            self.cam_mode = cam_mode
            irpic = ircam.pinoir2(js, cam_mode, c2, x, y, z, stat,sqx,sqy,s,wsh2,c)
            irpic.run()
            self.write_message("echo: " + message + " " + str(cam_mode) )    

        if message =='vid':
            message = 'blank'
            framecount = 1
            while(framecount < 300): #record @ 15fps
                pth1="/var/www/html/images/image"
		pth3=".png"
	 	pth= pth1 + str(framecount) + pth3
   		img1=Image(pth) 
	        img1.save(vs)
               ## time.sleep(0.1)
               ## c.getImage().save(js.framebuffer)
               ## time.sleep(0.1)
                framecount = framecount + 1

        if message =='vid2':
            framecount = 0
            message = 'blank'
            while(framecount < 300): #record @ 15fps
                img1 = c.getImage()
		time.sleep(10)
                framecount = framecount + 1
                pth1 = "/var/www/html/images/image"
                pth3 = ".png"
                pth = pth1 + str(framecount) + pth3
                print pth
                img1.save(pth)
                img1.save(js.framebuffer)
		

        if message =='vid3':
            framecount = 2
            message = 'blank'
            while(framecount < 300): #playback @ 15fps
                pth1 = "/var/www/html/images/image"
                pth3 = ".png"
                pth = pth1 + str(framecount) + pth3
                img2 = Image(pth)
                print pth
                img2.save(js.framebuffer)
                framecount = framecount + 1
		##time.sleep(5)



        if message =='c1':
            cam_mode = 1
            self.cam_mode = cam_mode
            img1 = c.getImage()
            img1.save(js.framebuffer)
            irpic = ircam.pinoir2(js, cam_mode, c2, x, y, z, stat,sqx,sqy,s,wsh2,c)
            irpic.run()
            self.write_message("echo: " + message + " " + str(cam_mode) )    

        if message =='h':
            print "h"
            x = x - 1
            self.x = x
            self.write_message("echo: " + message + " left" )
            s.write('q')
            irpic = ircam.pinoir2(js, cam_mode, c2, x, y, z, stat,sqx,sqy,s,wsh2,c)
            irpic.run()
            
        if message == 'squ':
            print "squ"
            sqy = self.sqy
            sqy = sqy + 25
            self.write_message("echo: "+str(sqy)+" sighting square")
            self.sqy=sqy
        if message == 'sqd':
            print "sqd"
            sqy = self.sqy
            sqy = sqy - 25
            self.write_message("echo: "+str(sqy)+" sighting square")
            self.sqy=sqy
        if message == 'sql':
            print "sql"
            sqx = self.sqx
            sqx = sqx + 25
            self.write_message("echo: "+str(sqx)+" sighting square")
            self.sqx=sqx
        if message == 'sqr':
            print "sqr"
            sqx = self.sqx
            sqx = sqx - 25
            self.write_message("echo: "+str(sqx)+" sighting square")
            self.sqx=sqx
            

        if message =='p':
            stat = "mapsizing"
            print "p"
            mapsize = mapsize + 1
            self.mapsize= mapsize
            self.write_message("echo: " + message + " mapsize " + str(mapsize))
            print "n"
            self.write_message("echo: " + message + " map" )
            wsh = tornado.websocket.WebSocketHandler        ## wsh holds some socket info
            wsh2 = self                                    ## wsh2 holds the name of the instance  
            map = so(mapsize, js, wsh, wsh2, c2, cam_mode,c)               ##  make an istance of the mapper --SO stands for seek out 
            self.map = map
            map.histo()                                   ##  histogram is necessary before run
  
        if message =='l':
            stat = "mapsizing"
            print "l"
            mapsize = mapsize - 1
            self.mapsize = mapsize
            self.write_message("echo: " + message + " mapsize " + str(mapsize))
            print "n"
            self.write_message("echo: " + message + " map" )

            wsh = tornado.websocket.WebSocketHandler        ## wsh holds some socket info
            wsh2 = self                                    ## wsh2 holds the name of the instance  
            map = so(mapsize, js, wsh, wsh2, c2, cam_mode,c)               ##  make an instance of the mapper --SO stands for seek out 
            self.map = map
            map.histo()                                   ##  histogram is necessary before run
  
            
        if message =='y':
            print "y"
            y = y + 1
            self.y = y
            self.write_message("echo: " + message + " up   ")
            s.write('w')
            time.sleep(.5)
            irpic = ircam.pinoir2(js, cam_mode, c2, x, y, z, stat,sqx,sqy,s,wsh2,c)
            irpic.run()

        if message =='g':
            print "g"
            y = y - 1
            self.y = y
            self.write_message("echo: " + message + " down   ")
            s.write('a')
            time.sleep(.5)
            irpic = ircam.pinoir2(js, cam_mode, c2, x, y, z, stat,sqx,sqy,s,wsh2,c)
            irpic.run()

        if message =='z':
            stat = "mapping down"
            print "z- map down"
            y = y - 1
            self.y = y
            self.write_message("echo: " + message + " map down   ")
            s.write('l')
            time.sleep(1)
            irpic = ircam.pinoir2(js, cam_mode, c2, x, y, z, stat,sqx,sqy,s,wsh2,c)
            irpic.run()

        if message =='a':
            stat = "mapping left"
            print "a- map left"
            x = x-1
            self.x = x
            self.write_message("echo: " + message + " map left   ")
            d = 'l'
            s.write('k')
            time.sleep(1)
            irpic = ircam.pinoir2(js, cam_mode, c2, x, y, z, stat,sqx,sqy,s,wsh2,c)
            irpic.run()

        if message =='w':
            stat = "mapping up"
            print "w- map up"
            y = y + 1
            self.y = y
            self.write_message("echo: " + message + " map up   ")
            d = 'u'
            s.write('o')
            time.sleep(1)
            irpic = ircam.pinoir2(js, cam_mode, c2, x, y, z, stat,sqx,sqy,s,wsh2,c)
            irpic.run()

        if message =='s':
            stat = "mapping right"
            print "s- map right"
            x = x + 1
            self.x = x
            self.write_message("echo: " + message + " map right   ")
            d = 'r'
            s.write('p')
            time.sleep(1)
            irpic = ircam.pinoir2(js, cam_mode, c2, x, y, z, stat,sqx,sqy,s,wsh2,c)
            irpic.run()

        if message =='b':           ## MAPPER
            if mapping == True:
                print "a"
##                s.write('n')
                time.sleep(1)
##                self.write_message(s.readline())
                self.write_message("echo: " + message + " map" )        
                wsh = tornado.websocket.WebSocketHandler        ## wsh holds some socket info
                wsh2 = self       ## wsh2 holds the name of the instance  
                map = self.map
                map.run()                        

        if message =='map':           ## MAPPER
            if mapping == False:
                mapping = True
                print "n"
                self.write_message("echo: " + message + " map" )
                wsh = tornado.websocket.WebSocketHandler        ## wsh holds some socket info
                wsh2 = self                                    ## wsh2 holds the name of the instance  
                map = so(mapsize, js, wsh, wsh2, c2, cam_mode,c)               ##  make an istance of the mapper --SO stands for seek out 
                self.map = map
                map.histo() ##  histogram is necessary before run
                ## print map.mySet                      ## print map log data array
                print mapping
                self.mapping = mapping
                self.write_message("m" )
            else:
                mapping = False
                self.mapping = mapping
                print mapping
           


        if message == 'c':
            wsh = tornado.websocket.WebSocketHandler        ## wsh holds some socket info
            wsh2 = self  ## wsh2 holds the name of the instance
            cchase = chase4(js, wsh, wsh2, c2, sqx, sqy, cam_mode,c)
            cchase.run()
                    

        if message == 'golive':
            wsh = tornado.websocket.WebSocketHandler        ## wsh holds some socket info
            wsh2 = self    ## wsh2 holds the name of the instance
            if live == False:
                live = True
                cchase = chase3(js, wsh, wsh2, c2, sqx, sqy, cam_mode,c)
                cchase.run()
                print live
                self.live = live
            else:
                live = False
                self.live = live
                print live

        if message == 'live':
            wsh = tornado.websocket.WebSocketHandler        ## wsh holds some socket info
            wsh2 = self    ## wsh2 holds the name of the instance
            if live == True:
                cchase = chase3(js, wsh, wsh2, c2, sqx, sqy, cam_mode,c)
                cchase.run()
            print live

             

                

        if message == 'x':
            showimage = showimage - 1
            self.showimage = showimage
            pth1 = "/var/www/html/images/image"
            pth3 = ".png"
            pth = pth1 + str(showimage) + pth3
            apath = os.path.abspath(pth)
            self.write_message(pth)
            print showimage
            img1 = Image(pth)
            img1.save(js.framebuffer)

            
        if message == 'v':
            showimage = showimage + 1
            self.showimage = showimage
            pth1 = "/var/www/html/images/image"
            pth3 = ".png"
            pth = pth1 + str(showimage) + pth3
            apath = os.path.abspath(pth)
            self.write_message(pth)
            print showimage
            img1 = Image(pth)
            img1.save(js.framebuffer)
##

        if message =='t':
            print "t"
            s.write('t')
            time.sleep(1)
            s.write('c')
            self.write_message("echo: " + message + " focus out")            
        if message =='f':
            print "f"
            s.write('f')
            time.sleep(1)
            s.write('c')

            self.write_message("echo: " + message + " focus in")            


        if message =='2':
            print "2"
            s.write('2')
            self.write_message("echo: " + message + " 2")

        if message =='3':
            print "3"
            s.write('3')
            self.write_message("echo: " + message + "3")
            irpic = ircam.pinoir2(js, cam_mode, c2, x, y, z, stat,sqx,sqy,s,wsh2,c)
            irpic.run()


        if message =='4':
            print "4"
            s.write('4')
            self.write_message("echo: " + message + "4")
            

        if message =='7':
            print "7"
            s.write('6')
            self.write_message("echo: " + message + " 7")

        if message =='mx':
            print "sensor"
            s.write('n')
            time.sleep(1)
            data= s.readline()
            self.write_message(data)
            with picamera.PiCamera() as camera:
                camera.resolution = (544, 288)
                camera.capture('imagesmall.jpg')
            img1 = Image('imagesmall.jpg')
            ##img1 = c.getImage()
            img1.drawText(str("Your Position Data:"), 10, 5, color=(255,255,255), fontsize=30)
            img1.drawText(str("ALT-->" + data + "<--AZ"), 10, 40, color=(255,255,0), fontsize=30)
            img1.save(js.framebuffer)
            

        if message =='8':
            print "8"
            s.write('8')
            self.write_message("echo: " + message + " 8")
            irpic = ircam.pinoir2(js, cam_mode, c2, x, y, z, stat,sqx,sqy,s,wsh2,c)
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

        
