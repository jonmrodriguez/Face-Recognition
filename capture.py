#! /usr/bin/python


'''
Created on Dec 16, 2011

@author: DinkyDogg
'''
import cv
import face_client
import threading
import tempfile

cv.NamedWindow("w1", cv.CV_WINDOW_AUTOSIZE)
camera_index = 0
capture = cv.CaptureFromCAM(camera_index)
client = face_client.FaceClient('a9f54bd412770bf8de1eb6fde4d99c6a', '0646e0f77a6bdb6712c36209d67f38ce')
frame = None

class RequestThread (threading.Thread):
    
    def run(self):
        global frame
        while True:
            frame_copy = frame;
            if frame_copy is not None:
                temp_file_name = tempfile.NamedTemporaryFile(suffix=".jpg").name
                cv.SaveImage(temp_file_name, frame_copy)
                print client.faces_detect(file_name=temp_file_name)
        
        
def capture_and_display():
    global capture #declare as globals since we are assigning to them now
    global camera_index
    global frame
    
    frame = cv.QueryFrame(capture)
    cv.ShowImage("w1", frame)
    
    c = cv.WaitKey(10)
    if(c=="n"): #in "n" key is pressed while the popup window is in focus
        camera_index += 1 #try the next camera index
        capture = cv.CaptureFromCAM(camera_index)
        if not capture: #if the next camera index didn't work, reset to 0.
            camera_index = 0
            capture = cv.CaptureFromCAM(camera_index)

if __name__ == "__main__":
    RequestThread().start()
    while True:
        capture_and_display()
