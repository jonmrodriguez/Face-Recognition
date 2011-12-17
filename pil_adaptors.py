#! /usr/bin/python

# from http://pycam.googlecode.com/svn/trunk/openeyes/swiglib/adaptors.py
#
# slightly modified by Jon Rodriguez:
#  changed "import opencv" to "import cv",
#   while changing all occurances of "opencv" to "cv"
#  changed all occurances of "cvmat" to "cvmat"




"""Adaptors to interchange data with numpy and/or PIL

This module provides explicit conversion of OpenCV images/matrices to and from
the Python Imaging Library (PIL) and python's newest numeric library (numpy).

Currently supported image/matrix formats are:
    - 3 x  8 bit  RGB (GBR)
    - 1 x  8 bit  Grayscale
    - 1 x 32 bit  Float

In numpy, images are represented as multidimensional arrays with
a third dimension representing the image channels if more than one
channel is present.
"""

import cv

import PIL.Image

###########################################################################
def Ipl2PIL(input):
    """Converts an OpenCV/IPL image to PIL the Python Imaging Library.

    Supported input image formats are
       IPL_DEPTH_8U  x 1 channel
       IPL_DEPTH_8U  x 3 channels
       IPL_DEPTH_32F x 1 channel
    """

 
    # Jon Rodriguez removed type safety check


    #orientation
    if input.origin == 0:
        orientation = 1 # top left
    elif input.origin == 1:
        orientation = -1 # bottom left
    else:
        raise ValueError, 'origin must be 0 or 1!'

    # mode dictionary:
    # (channels, depth) : (source mode, dest mode, depth in byte)
    mode_list = {
        (1, cv.IPL_DEPTH_8U)  : ("L", "L", 1),
        (3, cv.IPL_DEPTH_8U)  : ("BGR", "RGB", 3),
        (1, cv.IPL_DEPTH_32F) : ("F", "F", 4)
        }

    key = (input.nChannels, input.depth)
    if not mode_list.has_key(key):
        raise ValueError, 'unknown or unsupported input mode'

    modes = mode_list[key]

    return PIL.Image.fromstring(
        modes[1], # mode
        (input.width, input.height), # size tuple
        input.tostring(), # data. Used to say "input.imageData", but Jon Rodriguez changed this to say "input.tostring()" because this python binding doesn't seem to provide .imageData
        "raw",
        modes[0], # raw mode
        input.width, # stride. Used to say "input.widthStep", but Jon Rodriguez changed this to say "input.width" because this python binding doesn't seem to provide .widthStep
        orientation # orientation
        )


###########################################################################
def PIL2Ipl(input):
    """Converts a PIL image to the OpenCV/IPL cvmat data format.

    Supported input image formats are:
        RGB
        L
        F
    """

    if not (isinstance(input, PIL.Image.Image)):
        raise TypeError, 'Must be called with PIL.Image.Image!'
    
    # mode dictionary:
    # (pil_mode : (ipl_depth, ipl_channels)
    mode_list = {
        "RGB" : (cv.IPL_DEPTH_8U, 3),
        "L"   : (cv.IPL_DEPTH_8U, 1),
        "F"   : (cv.IPL_DEPTH_32F, 1)
        }
    
    if not mode_list.has_key(input.mode):
        raise ValueError, 'unknown or unsupported input mode'
    
    result = cv.CreateImageHeader( # Jon Rodriguez turned ".cvCreateImage" into ".CreateImageHeader"
        (input.size[0], input.size[1]),  # size. Used to be of type cv.cvSize but Jon Rodriguez switched it to a tuple
        mode_list[input.mode][0],  # depth
        mode_list[input.mode][1]  # channels
        )

    # set imageData
    cv.SetData(result, input.tostring()) # Jon Rodriguez's line
    return result




