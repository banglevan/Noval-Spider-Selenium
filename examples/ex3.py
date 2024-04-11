import cv2
import numpy as np

# Load the video
cap = cv2.VideoCapture(0)

# Create a Farneback optical flow object
# You can adjust the parameters as needed
farneback = cv2.optflow.createOptFlow_Farneback()

# Loop through each frame of the video
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # If it's not the first frame, calculate optical flow
    if 'previous_gray' in locals():
        # Calculate optical flow between the previous and current frame
        flow = farneback.calc(previous_gray, gray, None)

        # Calculate motion value per frame
        motion_value = np.mean(np.abs(flow))

        # Print or use the motion value as needed
        print("Motion Value:", motion_value)

    # Update the previous frame
    previous_gray = gray

# Release the video capture object
cap.release()