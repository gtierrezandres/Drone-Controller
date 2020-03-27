from djitellopy import Tello
import cv2
import pygame
import numpy as np
import time

# Speed of the drone
S = 60
# Frames per second of the pygame window display
FPS = 25

X = 0
O = 1
triangle = 2
square = 3
L1 = 4
R1 = 5
options_button = 9

class FrontEnd(object):
    """ Maintains the Tello display and moves it through the keyboard keys.
        Press escape key to quit.
        The controls are:
            - T: Takeoff
            - L: Land
            - Arrow keys: Forward, backward, left and right.
            - A and D: Counter clockwise and clockwise rotations
            - W and S: Up and down.
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

        # In case streaming is on. This happens when we quit this program without the escape key.
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

            time.sleep(1 / FPS)

        # Call it always before finishing. To deallocate resources.
        self.tello.end()

    def buttonDown(self, button):
        """ Update velocities based on key pressed
        Arguments:
            key: pygame key
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
        """ Update velocities based on key released
        Arguments:
            key: pygame key
        """
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
