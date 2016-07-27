from SimpleCV import *
import picamera
import time
from time import sleep
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
from fractions import Fraction
##js = SimpleCV.JpegStreamer('0.0.0.0:8080')                        ## opens socket for jpeg out

class pinoir2(object):
    def __init__(self, js, cam_mode, c2, x, y, z, stat, sqx,sqy,s,wsh2,c):
        self.js = js
        self.cam_mode = cam_mode
        self.c2 =c2
        self.c = c
        self.js = js
        self.stat = stat
        self.x = x
        self.y = y
        self.z = z
        self.sqx=sqx
        self.sqy=sqy
        self.s = s
        self.wsh2=wsh2
        
    def run(self):
        wsh2=self.wsh2
        stat = self.stat
        cent = 0
        rgb1 = 0
        x = self.x
        y = self.y
        z = self.z
        sqx =self.sqx
        sqy=self.sqy
        c2 = self.c2
        c= self.c
        s = self.s
        cam_mode = self.cam_mode
        js = self.js
        print cam_mode
        if cam_mode == 1:
##            img1 = c.getImage()
##            blobs = img1.findBlobs()
##            if blobs:
##                img1.drawCircle((blobs[-1].x,blobs[-1].y),30,color=(255,255,255))
##                img1.drawCircle((blobs[-1].centroid()),10,color=(255,100,100))
##                rgb1 = blobs[-1].meanColor()
##                cent = blobs[-1].centroid()
##                img1.drawText(str(cent), 10, 250, color=(255,255,255), fontsize=15)
##                img1.drawText(str(rgb1), 10, 270, color=(255,255,255), fontsize=15)
##
##                img1.drawText(str(stat), 10, 10, fontsize=50)
##                img1.drawText(str(x), 10, 70, color=(255,255,255), fontsize=25)
##                img1.drawText(str(y), 10, 100, color=(255,255,255), fontsize=25)
##
##                img1.drawRectangle(sqx,sqy,25, 25,color=(255,255,255))
##                img1.drawText(str(z), 10, 230, color=(255,255,255), fontsize=15)
##            img1.save(js.framebuffer)
            with picamera.PiCamera() as camera:
                camera.resolution = (544, 288)
                camera.capture('imagesmall.jpg')
            img1 = Image('imagesmall.jpg')
            self.img1 = img1
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

        if cam_mode == 2:
            with picamera.PiCamera() as camera:
                camera.resolution = (2600, 1900)
                camera.capture('/var/www/imagebig.jpg')
            img1 = Image('/var/www/imagebig.jpg')
            self.img1 = img1
            cent = 0
            rgb1 = 0
    
            blobs = img1.findBlobs()
            if blobs:
                crop1 = blobs[-1].x
                crop2 = blobs[-1].y
                crop3 = crop1 - 294
                crop4 = crop2 - 144
            ##    img1 = img1.crop(crop3,crop4,544,288)
                
            blobs = img1.findBlobs()
            if blobs:
                img1.drawCircle((blobs[-1].x,blobs[-1].y),30,color=(255,255,255))
                img1.drawCircle((blobs[-1].centroid()),10,color=(255,100,100))
                rgb1 = blobs[-1].meanColor()
                cent = blobs[-1].centroid()
                img1.drawText(str(cent), 10, 250, color=(255,255,255), fontsize=15)
                img1.drawText(str(rgb1), 10, 270, color=(255,255,255), fontsize=15)

            img1.drawText(str(stat), 10, 10, fontsize=50)
            img1.drawText(str(x), 10, 70, color=(255,255,255), fontsize=25)
            img1.drawText(str(y), 10, 100, color=(255,255,255), fontsize=25)
            img1.drawText(str(z), 10, 230, color=(255,255,255), fontsize=15)
            img1.save(js.framebuffer)
        if cam_mode == 3:
            img1 = c.getImage()
            blobs = img1.findBlobs()
            if blobs:
                img1.drawCircle((blobs[-1].x,blobs[-1].y),30,color=(255,255,255))
                img1.drawCircle((blobs[-1].centroid()),10,color=(255,100,100))
                rgb1 = blobs[-1].meanColor()
                cent = blobs[-1].centroid()
                img1.drawText(str(cent), 10, 250, color=(255,255,255), fontsize=15)
                img1.drawText(str(rgb1), 10, 270, color=(255,255,255), fontsize=15)

                img1.drawText(str(stat), 10, 10, fontsize=50)
                img1.drawText(str(x), 10, 70, color=(255,255,255), fontsize=25)
                img1.drawText(str(y), 10, 100, color=(255,255,255), fontsize=25)

                img1.drawRectangle(sqx,sqy,25, 25,color=(255,255,255))
                img1.drawText(str(z), 10, 230, color=(255,255,255), fontsize=15)
            img1.save(js.framebuffer)
##        if cam_mode == 4:
##            with picamera.PiCamera() as camera:
##                camera.resolution = (2600, 1900)
##                camera.framerate = Fraction(1, 6)
##                camera.shutterspeed = 6000000
##                camera.exposure_mode = 'verylong'
##                camera.iso = 800
##                sleep(10)
##                camera.capture('/var/www/dark.jpg')
##            img1 = Image('/var/www/dark.jpg')
##            self.img1 = img1
##            cent = 0
##            rgb1 = 0
##    
##            blobs = img1.findBlobs()
##            if blobs:
##                crop1 = blobs[-1].x
##                crop2 = blobs[-1].y
##                crop3 = crop1 - 294
##                crop4 = crop2 - 144
##                img1 = img1.crop(crop3,crop4,544,288)
##                
##            blobs = img1.findBlobs()
##            if blobs:
##                img1.drawCircle((blobs[-1].x,blobs[-1].y),30,color=(255,255,255))
##                img1.drawCircle((blobs[-1].centroid()),10,color=(255,100,100))
##                rgb1 = blobs[-1].meanColor()
##                cent = blobs[-1].centroid()
##                img1.drawText(str(cent), 10, 250, color=(255,255,255), fontsize=15)
##                img1.drawText(str(rgb1), 10, 270, color=(255,255,255), fontsize=15)
##
##            img1.drawText(str(stat), 10, 10, fontsize=50)
##            img1.drawText(str(x), 10, 70, color=(255,255,255), fontsize=25)
##            img1.drawText(str(y), 10, 100, color=(255,255,255), fontsize=25)
##            img1.drawText(str(z), 10, 230, color=(255,255,255), fontsize=15)
##            img1.save(js.framebuffer)
        else:
            pass

      

        
if __name__ == '__main__'  :
    js = SimpleCV.JpegStreamer('0.0.0.0:8080')                        ## opens socket for jpeg out

    foo = pinoir2(js)

else:
   pass
