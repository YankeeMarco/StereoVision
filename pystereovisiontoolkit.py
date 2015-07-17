#! /usr/bin/env python
# -*- coding:utf-8 -*- 


#
# Application to capture, and calibrate stereo cameras
#


#
# External dependencies
#
import argparse
import Calibration
import Viewer


#
# Command line argument parser
#
parser = argparse.ArgumentParser( description='Camera calibration toolkit.' )
parser.add_argument( '-live', action='store_true', default=False, help='Stereo camera live display' )
parser.add_argument( '-rows', action='store', default=15, help='Number of rows in the chessboard pattern' )
parser.add_argument( '-cols', action='store', default=10, help='Number of columns in the chessboard pattern' )
parser.add_argument( '-debug', action='store_true', default=False, help='Display the chessboard on each image' )
parser.add_argument( '-mono', action='store', help='Image files for mono camera calibration' )
parser.add_argument( '-stereo', action='store', nargs=2, metavar=('CAM1FILES', 'CAM2FILES'), help='Image files for stereo camera calibration' )
args = parser.parse_args()


#
# Calibration pattern setup
#
Calibration.pattern_size = ( int(args.rows), int(args.cols) )


#
# Stereo camera live capture
#
if args.live :

	# Stereo camera viewer
	Viewer.VmbStereoViewer()


#
# Mono camera calibration
#
elif args.mono :
	
	# Launch calibration
	Calibration.CameraCalibration( args.mono, args.debug )

#
# Mono camera calibration
#
elif args.stereo :
	
	# Launch calibration
	Calibration.StereoCameraCalibration( args.stereo[0], args.stereo[1], args.debug )

