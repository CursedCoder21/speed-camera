import pygame
import sys
import numpy as np
import pygame.camera as camera

# Initialize Pygame
pygame.init()

# Set up the camera
pygame.camera.init()
camera_list = pygame.camera.list_cameras()

if len(camera_list) == 0:
    print("No camera detected!")
    sys.exit()

# Use the first available camera
camera = pygame.camera.Camera(camera_list[0])

# Set up the display
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Motion and Speed Tracking")

# Set up variables for motion tracking
prev_frame = None
motion_threshold = 30
speed_multiplier = 0.1

def calculate_speed(motion_pixels):
    # Calculate speed based on the number of motion pixels
    return motion_pixels * speed_multiplier

def main():
    global prev_frame

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Start the camera
        camera.start()

        # Capture a frame from the camera
        frame = camera.get_image()
        frame = pygame.transform.scale(frame, (width, height))
        frame = pygame.surfarray.array3d(frame)

        # Convert the frame to grayscale for motion tracking
        gray_frame = np.mean(frame, axis=2)

        if prev_frame is not None:
            # Calculate the absolute difference between the current and previous frames
            diff_frame = np.abs(gray_frame - prev_frame)

            # Threshold the difference to identify motion pixels
            motion_pixels = np.sum(diff_frame > motion_threshold)

            # Calculate speed based on motion pixels
            speed = calculate_speed(motion_pixels)

            # Display the results
            print(f"Motion Pixels: {motion_pixels}, Speed: {speed}")

        # Update the previous frame
        prev_frame = gray_frame

        # Display the current frame
        pygame.surfarray.blit_array(screen, frame)
        pygame.display.flip()

        # Stop the camera
        camera.stop()

if __name__ == "__main__":
    main()
