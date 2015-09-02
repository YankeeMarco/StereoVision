# -*- coding:utf-8 -*- 


#
# Module to display live images from two AVT cameras
#


#
# External dependencies
#
import cv2
import numpy as np
import Vimba


#
# Vimba stereo camera viewer
#
class VmbStereoViewer( object ) :
		
	#
	# Initialization
	#
	def __init__( self, pattern_size, scale_factor = 0.37 ) :
		
		# Initialize Vimba
		Vimba.VmbStartup()

		# The cameras
		stereo_camera = Vimba.VmbStereoCamera( '50-0503326223', '50-0503323406' )

		# Number of image saved
		image_count = 0

		# Live chessboard finding and drawing on the image
		chessboard_enabled = False
		cross_enabled = False
		zoom_enabled = False
		
		# Open the cameras
		stereo_camera.Open()
		
		# Start image acquisition
		stereo_camera.StartCapture( self.FrameCallback )

		# Live display
		while True :

			# Initialize frame status
			self.frames_ready = False

			# Wait for the frames
			while not self.frames_ready : pass

			# Convert the frames to images
			image_left = self.frame_left.image
			image_right = self.frame_right.image

			# Resize image for display
			image_left_displayed = cv2.resize( image_left, None, fx=scale_factor, fy=scale_factor )
			image_right_displayed = cv2.resize( image_right, None, fx=scale_factor, fy=scale_factor )
			
			# Convert grayscale image in color
			image_left_displayed = cv2.cvtColor( image_left_displayed, cv2.COLOR_GRAY2BGR )
			image_right_displayed = cv2.cvtColor( image_right_displayed, cv2.COLOR_GRAY2BGR )

			# Preview the calibration chessboard on the image
			if chessboard_enabled :
				image_left_displayed = self.PreviewChessboard( image_left_displayed, pattern_size )
				image_right_displayed = self.PreviewChessboard( image_right_displayed, pattern_size )

			# Zoom in the middle of the image
			if zoom_enabled :
				w = image_left.shape[1] / 2
				h = image_left.shape[0] / 2
				wd = image_left_displayed.shape[1] / 2
				hd = image_left_displayed.shape[0] / 2
				image_left_displayed[ hd-350:hd+350, wd-400:wd+400 ] = cv2.cvtColor( image_left[ h-350:h+350, w-400:w+400 ], cv2.COLOR_GRAY2BGR )
				image_right_displayed[ hd-350:hd+350, wd-400:wd+400 ] = cv2.cvtColor( image_right[ h-350:h+350, w-400:w+400 ], cv2.COLOR_GRAY2BGR )

			# Display a cross in the middle of the image
			if cross_enabled :
				w = image_left_displayed.shape[1]
				h = image_left_displayed.shape[0]
				w2 = int( w/2 )
				h2 = int( h/2 )
				cv2.line( image_left_displayed, (w2, 0), (w2, h), (0, 255, 0), 2 )
				cv2.line( image_left_displayed, (0, h2), (w, h2), (0, 255, 0), 2 )
				cv2.line( image_right_displayed, (w2, 0), (w2, h), (0, 255, 0), 2 )
				cv2.line( image_right_displayed, (0, h2), (w, h2), (0, 255, 0), 2 )

			# Prepare image for display
			stereo_image = np.concatenate( (image_left_displayed, image_right_displayed), axis=1 )
			
			# Display the image (scaled down)
			cv2.imshow( '{} - {}'.format( stereo_camera.camera_left.id, stereo_camera.camera_right.id ), stereo_image )

			# Keyboard interruption
			key = cv2.waitKey( 1 ) & 0xFF
			
			# Escape key
			if key == 27 :
				
				# Exit live display
				break
				
			# Space key
			elif key == 32 :
				
				# Save images to disk 
				image_count += 1
				print( 'Save images {} to disk...'.format(image_count) )
				cv2.imwrite( 'left{:0>2}.png'.format(image_count), image_left )
				cv2.imwrite( 'right{:0>2}.png'.format(image_count), image_right )
				
			# C key
			elif key == ord('c') :
				
				# Enable / Disable chessboard preview
				chessboard_enabled = not chessboard_enabled		

			# M key
			elif key == ord('m') :
				
				# Enable / Disable display of the middle cross
				cross_enabled = not cross_enabled		

			# Z key
			elif key == ord('z') :
				
				# Enable / Disable zoom in the middle
				zoom_enabled = not zoom_enabled		

		# Stop image acquisition
		stereo_camera.StopCapture()
					
		# Cleanup OpenCV
		cv2.destroyAllWindows()
	
		# Close the cameras
		stereo_camera.Close()

		# Shutdown Vimba
		Vimba.VmbShutdown()

	#
	# Receive the frames from both cameras
	#
	def FrameCallback( self, frame_left, frame_right ) :

		# Save current frame
		self.frame_left = frame_left
		self.frame_right = frame_right

		# Frame ready
		self.frames_ready = True

	#
	# Find the chessboard quickly and draw it
	#
	def PreviewChessboard( self, image, pattern_size ) :
		
		# Find the chessboard corners on the image
		found_all, corners = cv2.findChessboardCorners( image, pattern_size, flags = cv2.CALIB_CB_FAST_CHECK )	
	#	found_all, corners = cv2.findCirclesGridDefault( image, pattern_size, flags = cv2.CALIB_CB_ASYMMETRIC_GRID )	

		# Chessboard found
		if found_all :
			
			# Draw the chessboard corners on the image
			cv2.drawChessboardCorners( image, pattern_size, corners, found_all )
			
		# Return the image with the chessboard if found
		return image
