# importing the necessary libraries
import cv2
import numpy as np
import time 

# Creating a VideoCapture object to read the video
cap = cv2.VideoCapture('test.mp4')
 
# Start time
n=0
start = time.time()
# stop
s = True
# Loop until the end of the video
while (cap.isOpened()):
    # Capture frame-by-frame
    if s:
        ret, frame = cap.read()
        n+=1
        frame = cv2.resize(frame, (540, 380), fx = 0, fy = 0,
                         interpolation = cv2.INTER_CUBIC)
    
    # Display the resulting frame
    cv2.imshow('Frame', frame)
 
    # using cv2.Canny() for edge detection.
    edge_detect = cv2.Canny(frame, 100, 200)
    cv2.imshow('Edge detect', edge_detect)

    k = cv2.waitKey(1) & 0xFF
    if k is ord('q'):
        break
    elif k is ord('s'):
        if s:
            s = False
        else:
            s=True
        

 

# End time
end = time.time()
# Time elapsed
seconds = end - start
print ("Time taken : {0} seconds".format(seconds))

# Calculate frames per second
fps  = n / seconds
print("Estimated frames per second : {0}".format(fps))
	
# release the video capture object
cap.release()
# Closes all the windows currently opened.
cv2.destroyAllWindows()