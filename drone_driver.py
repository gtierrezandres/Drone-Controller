from djitellopy import Tello
import cv2
import pygame
import numpy as np
import time
import os

# Speed of the drone
S = 60
# Frames per second of the pygame window display
FPS = 25

# Buttons used
X = 0
O = 1
triangle = 2
square = 3
L1 = 4
R1 = 5
L2 = 6
R2 = 7
share_button = 8
options_button = 9


photos = "photos"
videos = "videos"

imgCount = 0

os.path.exists(os.path.abspath(("Drone-Controller")))
# Check if a directory exists for storing pictures and recording video
if not os.path.exists(os.path.abspath(photos)) and not os.path.exists(os.path.abspath(videos)):
    os.mkdir(os.path.join(os.getcwd(), photos))
    os.mkdir(os.path.join(os.getcwd(), videos))

else:
    img_dir = os.path.abspath(photos)
    vid_dir = os.path.abspath(videos)

    if len(os.listdir(img_dir)) != 0:
        for f in os.listdir(img_dir):
            os.remove(os.path.join(img_dir, f))

    if len(os.listdir(img_dir)) != 0:
        for file in os.listdir(vid_dir):
            os.remove(os.path.join(vid_dir, file))



class FrontEnd(object):
    """ Maintains the Tello display and moves it through the buttonboard buttons.
        Press escape button to quit.
        The controls are:
            - Triangle: Takeoff
            - Square: Land
            - Arrow buttons: Forward, backward, left and right
            - L1 and R1: Counter clockwise and clockwise rotations
            - L2 and R2: Snap and record a video
            - X and O: Up and down
            - Options: turns off drone
            - Share:
    """

    def __init__(self):
        # Init pygame
        pygame.init()

        # Init joystick
        self.j = pygame.joystick.Joystick(0)
        self.j.init()


        # Creat pygame window
        pygame.display.set_caption("Tello video stream")
        self.screen = pygame.display.set_mode([960, 720])

        # Init Tello object that interacts with the Tello drone
        self.tello = Tello()

        # Drone velocities between -100~100
        self.for_back_velocity = 0
        self.left_right_velocity = 0
        self.up_down_velocity = 0
        self.yaw_velocity = 0
        self.speed = 10

        self.send_rc_control = False

        # create update timer
        pygame.time.set_timer(pygame.USEREVENT + 1, 50)

    def run(self):

        if not self.tello.connect():
            print("Tello not connected")
            return

        if not self.tello.set_speed(self.speed):
            print("Not set speed to lowest possible")
            return

        # In case streaming is on. This happens when we quit this program without the escape button.
        if not self.tello.streamoff():
            print("Could not stop video stream")
            return

        if not self.tello.streamon():
            print("Could not start video stream")
            return

        frame_read = self.tello.get_frame_read()

        should_stop = False
        while not should_stop:

            for event in pygame.event.get():
                if event.type == pygame.USEREVENT + 1:
                    self.update()
                elif event.type == pygame.QUIT:
                    should_stop = True
                elif event.type == pygame.JOYBUTTONDOWN:
                    if event.button == options_button:
                        should_stop = True
                    else:
                        self.buttonDown(event.button)
                elif event.type == pygame.JOYHATMOTION:
                    if event.value == (0, 0):
                        self.buttonUp(event.value)
                        #print("hello from run")
                    else:
                        self.buttonDown(event.value)

                elif event.type == pygame.JOYBUTTONUP:
                    self.buttonUp(event.button)

            if frame_read.stopped:
                frame_read.stop()
                break

            self.screen.fill([0, 0, 0])
            frame = cv2.cvtColor(frame_read.frame, cv2.COLOR_BGR2RGB)
            frame = np.rot90(frame)
            frame = np.flipud(frame)
            frame = pygame.surfarray.make_surface(frame)
            self.screen.blit(frame, (0, 0))
            pygame.display.update()
            frameRet = frame_read.frame

            time.sleep(1 / FPS)

        # Call it always before finishing. To deallocate resources.
        self.tello.end()

    def buttonDown(self, button):
        """ Update velocities based on button pressed
        Arguments:
            button: pygame button
        """
        if button == (0, 1):  # set forward velocity
            self.for_back_velocity = S
        elif button == (0, -1):  # set backward velocity
            self.for_back_velocity = -S
        elif button == (-1, 0):  # set left velocity
            self.left_right_velocity = -S
        elif button == (1, 0):  # set right velocity
            self.left_right_velocity = S
        elif button == X:  # set up velocity
            self.up_down_velocity = S
        elif button == O:  # set down velocity
            self.up_down_velocity = -S
        elif button == L1:  # set yaw counter clockwise velocity
            self.yaw_velocity = -S
        elif button == R1:  # set yaw clockwise velocity
            self.yaw_velocity = S

    def buttonUp(self, button):
        """ Update velocities based on button released
        Arguments:
            button: pygame button
        """

        global imgCount

        if button == (0, 0):
            #print("hello from buttonUp")
            self.for_back_velocity = 0
            self.left_right_velocity = 0
        elif button == X or button == O:  # set zero up/down velocity
            self.up_down_velocity = 0
        elif button == L1 or button == R1:  # set zero yaw velocity
            self.yaw_velocity = 0
        elif button == triangle:  # takeoff
            self.tello.takeoff()
            self.send_rc_control = True
        elif button == square:  # land
            self.tello.land()
            self.send_rc_control = False
        elif button == L2:
            cv2.imwrite(os.path.join(os.path.abspath(photos), f"picture{imgCount}.jpg"), self.tello.get_frame_read().frame)
            imgCount+=1
            print("Photo Taken!!!")

    def update(self):
        """ Update routine. Send velocities to Tello."""
        if self.send_rc_control:
            self.tello.send_rc_control(self.left_right_velocity, self.for_back_velocity, self.up_down_velocity,
                                       self.yaw_velocity)


def main():
    frontend = FrontEnd()

    # run frontend
    frontend.run()


if __name__ == '__main__':
    main()
