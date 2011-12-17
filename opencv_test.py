#! /usr/bin/python


###
### From http://stackoverflow.com/a/2602410/402807
###


import sys # sys.argv
import os # os.system
import pdb
import cv
import Image # PIL (Python Imaging Library)
import pil_adaptors




def pilFromIpl(cv_im):
    # pil_im = Image.fromstring("L", cv.GetSize(cv_im), cv_im.tostring())

    # TODO how to eventually destruct the pil_im
    return pil_adaptors.Ipl2PIL(cv_im)

def iplFromPil(pil_im):
    # cv_im = cv.CreateImageHeader(pil_im.size, cv.IPL_DEPTH_8U, 3)
    # cv.SetData(cv_im, pil_im.tostring())

    # TODO how to eventually destruct the cv_im
    return pil_adaptors.PIL2Ipl(pil_im)




cv.NamedWindow("w1", cv.CV_WINDOW_AUTOSIZE)
camera_index = 0
capture = cv.CaptureFromCAM(camera_index)

def repeat():
    global capture #declare as globals since we are assigning to them now
    global camera_index
    frame = cv.QueryFrame(capture)


    # here, convert to PIL and back
    f0 = frame
    p1 = pilFromIpl(f0)
    f2 = iplFromPil(p1)

    cv.ShowImage("w1", f2)
    
    c = cv.WaitKey(10)


while True:
    repeat()

