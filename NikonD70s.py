from time import sleep
from datetime import datetime
from sh import gphoto2 as gp

import signal, os, subprocess

#kill gphoto2 process that starts when cam connects

def killgphoto2Process():
    p = subprocess.Popen(['ps', '-A'],stdout=subprocess.PIPE)
    out, err = p,communicate()

    #Search for the line that has process
    # We want to Kill

    for line in out.splitlines():
        if b'gvfsd-gphoto2' in line:
            #kill
            pid = int(line.split(None,1)[0])
            os.kill(pid,signal.SIGKILL)

shot_date = datetime.now().strftime("%Y-%m-%d")
shot_time = datetime.now().strftime("%Y-%m-%d %H:%M:%
picID = "PiShots"

clearCommand = ["--folder","/store_00010001/DCIM/101ND70S",\
                "-R","--delete-all-files"]

triggerCommand = ["--trigger-capture"]
downloadCommand = ["--get-all-files"]

folder_name = shot_date + picID
save_location ="/home/pi/Desktop/gphoto/images/"+folder_name

def createSaveFolder():
    try:
        os.makedirs (save_location)

    except:
        print("failed DIR")

    os.chdir(save_location)

def captureImages():
    gp(triggerCommand)
    sleep(3)
    gp (downloadCommand)
    gp(clearCommand)

def renameFiles(ID):
    for filename in os.listdir(","):
        if len(filename)< 13:
            if filename.endswith(".JPG"):
                os.rename(filename,(shot_time +ID + ".JPG"))
                print("Renamed the JPG")


gp(clearCommand)
createSaveFolder()
captureImages()
renameFiles(picID)





    

