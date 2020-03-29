import pygame
import time

pygame.init()
j = pygame.joystick.Joystick(0)
j.init()

try:
    while True:
        events = pygame.event.get()
        for event in events:

            #check for joystick activity
            if event.type == pygame.JOYAXISMOTION and event.value != 0:
                if event.axis == j.get_axis(0) or event.axis == j.get_axis(1):
                    x_axis = j.get_axis(0)
                    y_axis = j.get_axis(1)
                    left = x_axis < -0.5
                    right = x_axis > 0.5
                    top = y_axis < -0.5
                    bottom = y_axis > 0.5
                    print( f"left joystick values: (top: {top}), (bottom: {bottom})" )
                elif event.axis == 3 or event.axis == 4:
                    print(f"right joystick value: {event.value}")
                #print(event.dict, event.joy, event.axis, event.value)

            # check for L2 and R2 activity
            elif event.type == pygame.JOYBALLMOTION:
                print(event.dict, event.joy, event.ball, event.rel)


            #check if the event type is a button press
            elif event.type == pygame.JOYBUTTONDOWN:
                #print X
                if event.button == 0:
                    print("X")

                #print O
                elif event.button == 1:
                    print("O")
                
                #print △
                elif event.button == 2:
                    print("Triangle")

                #print □
                elif event.button == 3:
                    print("Square")

                #print L1
                elif event.button == 4:
                    print("L1")

                #print R1
                elif event.button == 5:
                    print("R1")

                #print(event.dict, event.joy, event.button, 'pressed')
            #elif event.type == pygame.JOYBUTTONUP:
            #    print(event.dict, event.joy, event.button, 'released')
            
            #check for arrow activity
            elif event.type == pygame.JOYHATMOTION:
                #print(event.dict, event.joy, event.hat, event.value)
                #print(event.hat)
                print(event.value)
                #print(type(event.value))


#exit out of the when loop Ctrl+C is pressed
except KeyboardInterrupt:
    print("EXITING NOW")
    j.quit()
