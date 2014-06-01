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
from SimpleCV import *
## our library
from ogp3 import *

## some important variables

s = serial.Serial('/dev/ttyUSB0', 9600)                     ## serial to arduino

c = SimpleCV.Camera(0,{ "width": 544, "height": 288 })          ## opens a camera
##c2 = SimpleCV.Camera(1,{ "width": 544, "height": 288 })           ## or two
js = SimpleCV.JpegStreamer('0.0.0.0:8080')                        ## opens socket for jpeg out
time.sleep(4)                                               ## strategic buffering, possibly unnecessary
c.getImage().save(js.framebuffer)                 ## push a jpeg to the jpeg socket

##autocalibration
acu = int(1)
acd = int(1)
acl = int(1)
acr = int(3)

showimage = int(1)
mapsize = int(8)
stepsize = int(75)

stat = "ogp"



class WSHandler(tornado.websocket.WebSocketHandler):      

    def open(self):
        print 'New connection was opened'
        self.write_message("telescope listening")   ## sending message through text socket
        x = int(0)
        y = int(0)
        z = int(0)
        self.x = 0
        self.y = 0
        self.z = 0
        self.mapsize = mapsize
        self.showimage = showimage


    def on_message(self, message):

        print 'Incoming message:', message      ## output message to python
        showimage = self.showimage
        mapsize = self.mapsize
        x = self.x
        y = self.y
        z = self.z
        stat = "ogp"

        
        if message =='j':            ##    switches for incoming socket events
            print "j"
            x = x + 1
            self.x = x
            self.write_message("echo: " + message + " right " )    
            d = 'r'
            ms = 50
            s.write('4')
            mov = acx(s, d, ms, acu, acd, acl, acr)
            mov.run()
            img1 = c.getImage()
            hud1 = hud(img1, js, stat, x, y, z)
            hud1.run()
        if message =='h':
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
            img1 = c.getImage()
            hud1 = hud(img1, js, stat, x, y, z)
            hud1.run()

        if message =='p':
            stat = "mapsizing"
            print "p"
            mapsize = mapsize + 1
            self.mapsize= mapsize
            self.write_message("echo: " + message + " mapsize " + str(mapsize))
            img1 = c.getImage()
            hud1 = hud(img1, js, stat, x, y, z)
            hud1.run()
        if message =='l':
            stat = "mapsizing"
            print "l"
            mapsize = mapsize - 1
            self.mapsize = mapsize
            self.write_message("echo: " + message + " mapsize " + str(mapsize))
            img1 = c.getImage()
            hud1 = hud(img1, js, stat, x, y, z)
            hud1.run()
            
            
        if message =='y':
            print "y"
            y = y + 1
            self.y = y
            self.write_message("echo: " + message + " up   ")
            d = 'u'
            ms = 50
            s.write('6')
            mov = acx(s, d, ms, acu, acd, acl, acr)
            mov.run()
            img1 = c.getImage()
            hud1 = hud(img1, js, stat, x, y, z)
            hud1.run()

        if message =='g':
            print "g"
            y = y - 1
            self.y = y
            self.write_message("echo: " + message + " down   ")
            d = 'd'
            ms = 50
            s.write('9')
            mov = acx(s, d, ms, acu, acd, acl, acr)
            mov.run()
            img1 = c.getImage()
            hud1 = hud(img1, js, stat, x, y, z)
            hud1.run()  
        if message =='z':
            stat = "mapping down"
            print "z- map down"
            y = y - 1
            self.y = y
            self.write_message("echo: " + message + " map down   ")
            d = 'd'
            ms = 250
            s.write('9')
            mov = acx(s, d, ms, acu, acd, acl, acr)
            mov.run()
            img1 = c.getImage()
            hud1 = hud(img1, js, stat, x, y, z)
            hud1.run()
        if message =='a':
            stat = "mapping left"
            print "a- map left"
            x = x-1
            self.x = x
            self.write_message("echo: " + message + " map left   ")
            d = 'l'
            ms = 250
            s.write('2')
            mov = acx(s, d, ms, acu, acd, acl, acr)
            mov.run()
            img1 = c.getImage()
            hud1 = hud(img1, js, stat, x, y, z)
            hud1.run()
        if message =='w':
            stat = "mapping up"
            print "w- map up"
            y = y + 1
            self.y = y
            self.write_message("echo: " + message + " map up   ")
            d = 'u'
            ms = 250
            s.write('6')
            mov = acx(s, d, ms, acu, acd, acl, acr)
            mov.run()
            img1 = c.getImage()
            hud1 = hud(img1, js, stat, x, y, z)
            hud1.run()
        if message =='s':
            stat = "mapping right"
            print "s- map right"
            x = x + 1
            self.x = x
            self.write_message("echo: " + message + " map right   ")
            d = 'r'
            ms = 250
            s.write('4')
            mov = acx(s, d, ms, acu, acd, acl, acr)
            mov.run()
            img1 = c.getImage()
            hud1 = hud(img1, js, stat, x, y, z)
            hud1.run()

        if message =='b':           ## MAPPER 
            print "b"
            self.write_message("echo: " + message + " map" )        
            m = int(5)
            wsh = tornado.websocket.WebSocketHandler        ## wsh holds some socket info
            wsh2 = self       ## wsh2 holds the name of the instance  
            map = self.map
            map.run()                                   ##  histogram is necessary before run

        if message =='n':           ## MAPPER 
            print "n"
            self.write_message("echo: " + message + " map" )        
            m = int(5)
            wsh = tornado.websocket.WebSocketHandler        ## wsh holds some socket info
            wsh2 = self                                    ## wsh2 holds the name of the instance  
            map = so(mapsize, c, m, js, wsh, wsh2)               ##  make an istance of the mapper --SO stands for seek out 
            self.map = map
            map.histo()                                   ##  histogram is necessary before run
           ## print map.mySet                      ## print map log data array

        if message == 'c':
            wsh = tornado.websocket.WebSocketHandler        ## wsh holds some socket info
            wsh2 = self                                    ## wsh2 holds the name of the instance  
            cchase = chase(c, js, wsh, wsh2)
            cchase.run()

        if message == 'k':
            wsh = tornado.websocket.WebSocketHandler        ## wsh holds some socket info
            wsh2 = self                                    ## wsh2 holds the name of the instance  
            ac = autocal(c, js, wsh, wsh2)
            ac.run()
        if message == 'x':
            showimage = showimage - 1
            self.showimage = showimage
            pth1 = "images/image"
            pth3 = ".png"
            pth = pth1 + str(showimage) + pth3
            print showimage
            img1 = Image(pth)
            img1.save(js.framebuffer)
        if message == 'v':
            showimage = showimage + 1
            self.showimage = showimage
            pth1 = "images/image"
            pth3 = ".png"
            pth = pth1 + str(showimage) + pth3
            print showimage
            img1 = Image(pth)
            img1.save(js.framebuffer)

        if message =='t':
            print "t"
            s.write('t')
            self.write_message("echo: " + message + " focus out")            
        if message =='f':
            print "f"
            s.write('f')
            self.write_message("echo: " + message + " focus in")            


        if message =='2':
            print "2"
            s.write('2')
            self.write_message("echo: " + message + " 2")

        if message =='3':
            print "3"
            s.write('3')
            self.write_message("echo: " + message + "3")
            img1 = c.getImage()
            stat = "ogp -  stop x"
            hud1 = hud(img1, js, stat, x, y, z)
            hud1.run()


        if message =='4':
            print "4"
            s.write('4')
            self.write_message("echo: " + message + "4")
            

        if message =='7':
            print "7"
            s.write('6')
            self.write_message("echo: " + message + " 7")


        if message =='8':
            print "8"
            s.write('8')
            self.write_message("echo: " + message + " 8")

            img1 = c.getImage()
            stat = "ogp -  stop y"
            hud1 = hud(img1, js, stat, x, y, z)
            hud1.run()


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
        
