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
js = SimpleCV.JpegStreamer('10.0.10.149:8080')
time.sleep(4)                                               ## strategic buffering, possibly unnecessary
img1=c.getImage()                 ## push a jpeg to the jpeg socket
img1.drawText("Hello", 10, 5, fontsize=40)
img1.save(js.framebuffer)
cam_mode = int(1)


showimage = int(1)
mapsize = int(10)

stat = "ogp"
sqx = int(272)
sqy = int(144)
vs = VideoStream("/var/www/html/vid.avi", 15, False)

moon = ephem.Moon()
orlando = ephem.Observer()
orlando.lat = '28.41'
orlando.lon =  '-81.29'


class WSHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):     ##required for new tornado security bypass
        return True

    def open(self):
        print 'New connection was opened 1'
        self.write_message("telescope listening")   ## sending message through text socket
        x = int(0)
        y = int(0)
        z = int(0)
        self.x = 0
        self.y = 0
        self.z = 0
        self.live = False
        self.mapping = False
        self.mapsize = mapsize
        self.showimage = showimage
        self.cam_mode = cam_mode
        self.sqx = sqx
        self.sqy = sqy
        ##s.write('n')
        time.sleep(2)
        ##self.write_message(s.readline())
        
        

    def on_message(self, message):

        print 'Incoming message:', message      ## output message to python
        if message.isdigit():
            digits = int(message)
            print 'digits_'+ str(digits)
            if digits>9:
                s.write('x'+ str(digits))
                
        msgsplit = message.split("_")
        print msgsplit[0]
        
        showimage = self.showimage
        mapsize = self.mapsize
        x = self.x
        y = self.y
        z = self.z
        stat = "ogp"
        sqx = self.sqx
        sqy=self.sqy
        cam_mode = self.cam_mode
        wsh2=self
        live = self.live
        mapping = self.mapping

        if msgsplit[0] == 'moon':
            print "moon"
            
            client_utc = str(msgsplit[1] + " " + msgsplit[2])
            print client_utc
	    d = ephem.Date(client_utc)
            orlando.date = d
            print d
            moon.compute(orlando)
            moonaz = str(moon.az)
            moonalt = str(moon.alt)
            ticks = str(time.time())
            moonpoz = str("MOON_POS_ALT_" + moonalt +"__AZ_"+ moonaz)
            self.write_message("moon_" + moonalt + "_" + moonaz )
            self.write_message("time_" + client_utc)
            with picamera.PiCamera() as camera:
                camera.resolution = (544, 288)
                camera.capture('imagesmall.jpg')
            img1 = Image('imagesmall.jpg')
            ##img1 = c.getImage()
            img1.drawText(str("CLIENT_TIME_" + client_utc+"_Orlando_FL"), 10, 30, color=(255,255,255), fontsize=30)
            img1.drawText(str(moonpoz), 10, 5, color=(255,255,255), fontsize=30)
            if moon.alt < 0:
                img1.drawText(str("MOON BELOW HORIZON"), 10, 55, color=(255,255,0), fontsize=30)
            img1.save(js.framebuffer)
            
            moonaz2 = moonaz.split(":")
            moonalt2 = moonalt.split(":")
            print moonaz2[0]
            print moonalt2[0]

            moonalt3 = moonalt2[0]
            if moonalt3 >= 12:
                moonalt4 = "x"+ str(moonalt3)
##                s.write(moonalt4)
                

##            moonaz3 = moonaz2[0]
##            if moonaz3 >= 3:
##                moonaz4 = int(moonaz3) + 100
##                s.write(moonaz4)
        
        if message =='j':            ##    switches for incoming socket events
            print "j"
            x = x + 1
            self.x = x
            self.write_message("echo: " + message + " right " )    
            s.write('s')
            time.sleep(.5)
            irpic = ircam.pinoir2(js, cam_mode, c2, x, y, z, stat,sqx,sqy,s,wsh2,c)
            irpic.run()
        
        if message =='c3':
            cam_mode = 3
            self.cam_mode = cam_mode
            img1 = c2.getImage()
            blobs = img1.findBlobs()
            if blobs:
                img1.drawCircle((blobs[-1].x,blobs[-1].y),30,color=(255,255,255))
                img1.drawCircle((blobs[-1].centroid()),10,color=(255,100,100))
                rgb1 = blobs[-1].meanColor()
                cent = blobs[-1].centroid()

                img1.drawText(str(stat), 10, 10, fontsize=50)
                img1.drawText(str(x), 10, 70, color=(255,255,255), fontsize=25)
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

        
