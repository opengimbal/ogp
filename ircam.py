## OGP IRCAM.PY class library
## this file describes camera modes 1, 2 and 3. 



from SimpleCV import *     ## get your libraries available
import picamera
import time

class pinoir2(object):      ## for use whenever you need a picture taken and passed to the viewer automatically
    def __init__(self, js, cam_mode, c2, x, y, z, stat):    ## these are the arguments that just got passed here
        self.js = js   ## we unpack them individually from the line above 
        self.cam_mode = cam_mode
        self.c2 =c2
        self.js = js
        self.stat = stat
        self.x = x
        self.y = y
        self.z = z
        
    def run(self):  
        stat = self.stat    ## we unpack again into the run definition name space
        x = self.x          
        y = self.y
        z = self.z
        c2 = self.c2
        cam_mode = self.cam_mode
        js = self.js
        print cam_mode
        
        if cam_mode == 1:     ## CAM MODE 1 is a low res shot from the PiCamera
            with picamera.PiCamera() as camera:     
                camera.resolution = (544, 288)      ## declare your desired resolution
                camera.capture('imagesmall.jpg')     ## takes and then saves an image in the main folder
            img1 = Image('imagesmall.jpg')      ## then picks it up from the main folder --- probably inefficient  
            self.img1 = img1                          ## pack the info away -- possibly unecessary
            blobs = img1.findBlobs()                  ## get blob info from image using simpleCV commands
            if blobs:                               ## if any exist then we draw the indicators
                img1.drawCircle((blobs[-1].x,blobs[-1].y),30,color=(255,255,255))   ## draw the indicators
                img1.drawCircle((blobs[-1].centroid()),10,color=(255,100,100))    ##draw the indicators
                rgb1 = blobs[-1].meanColor()     ##  save the rgb value of the centroid of the blob
                cent = blobs[-1].centroid()     ## save the x and y blob centroid values we just obtained

            img1.drawText(str(stat), 10, 10, fontsize=50)       ##  draws the current info onto the current image
            img1.drawText(str(x), 10, 70, color=(255,255,255), fontsize=25)
            img1.drawText(str(y), 10, 100, color=(255,255,255), fontsize=25)
            
            img1.drawText(str(z), 10, 230, color=(255,255,255), fontsize=15)
            img1.drawText(str(cent), 10, 250, color=(255,255,255), fontsize=15)
            img1.drawText(str(rgb1), 10, 270, color=(255,255,255), fontsize=15)
            
            img1.save(js.framebuffer)      ## send the image to the clients viewfinder
            
        if cam_mode == 2:    ## camera mode 2 crops out the area containing the blob centroid of a high res image
            with picamera.PiCamera() as camera:
                camera.resolution = (2600, 1900)  ## take hi res image
                camera.capture('imagebig.jpg')   ## takes image and saves it to the main folder
            img1 = Image('imagebig.jpg')    ## picks it up from the main folder -- inefficient
            self.img1 = img1
            cent = 0    ## reset these variables - possibly unnecessary
            rgb1 = 0
    
            blobs = img1.findBlobs()    ## get blob info from image thanks to this simpleCV command.
            if blobs:                          ## if there is a blob...
                crop1 = blobs[-1].x             ## then crop it down so that... 
                crop2 = blobs[-1].y           ## the blob centroid remains in the center.
                crop3 = crop1 - 294         ## shift x position over half the size of the intended viewfinder
                crop4 = crop2 - 144         ## same with Y position
                img1 = img1.crop(crop3,crop4,544,288)     ## now crop it 
                
            blobs = img1.findBlobs()   ## find centroid info of your new cropped image
            if blobs:      ## if a blob exists
                img1.drawCircle((blobs[-1].x,blobs[-1].y),30,color=(255,255,255))  ## draw a circle around...
                img1.drawCircle((blobs[-1].centroid()),10,color=(255,100,100))   ## the centroid points.
                rgb1 = blobs[-1].meanColor()   ## get info 
                cent = blobs[-1].centroid()    ## get info
                

            img1.drawText(str(stat), 10, 10, fontsize=50)    ## put all the info on the image...
            img1.drawText(str(x), 10, 70, color=(255,255,255), fontsize=25)
            img1.drawText(str(y), 10, 100, color=(255,255,255), fontsize=25)
            img1.drawText(str(z), 10, 230, color=(255,255,255), fontsize=15)
            img1.drawText(str(cent), 10, 250, color=(255,255,255), fontsize=15)
            img1.drawText(str(rgb1), 10, 270, color=(255,255,255), fontsize=15)
            
            img1.save(js.framebuffer)    ## and send it to the viewer.

        if cam_mode == 3:    ## this mode works in much the same way except that...
            img1 = c2.getImage() ## we begin by grabbing an image from the simpleCV webcam (secondary cam)
            blobs = img1.findBlobs()   ## and then just run it through the same process. 
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
            
        else:
            pass

        
if __name__ == '__main__'  :      ## since this isnt the main module, this part of the code doesnt happen
    js = SimpleCV.JpegStreamer('0.0.0.0:8080')                        ## opens socket for jpeg out
    foo = pinoir2(js)

else:
   pass
