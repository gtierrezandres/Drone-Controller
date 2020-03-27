import pygame

pygame.init()
j = pygame.joystick.Joystick(0)
j.init()

try:
    while True:
        events = pygame.event.get()
        for event in events:

            #check if the joystick is being moved
            if event.type == pygame.JOYAXISMOTION and event.value != 0.0:
                if event.axis == 1 or event.axis == 2:
                    print(f"left joystick value: {event.value}")
                elif event.axis == 3 or event.axis == 4:
                    print(f"right joystick value: {event.value}")
                #print(event.dict, event.joy, event.axis, event.value)

            
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
                    print("△")

                #print □
                elif event.button == 3:
                    print("□")

                #print L1
                elif event.button == 4:
                    print("L1")

                #print R1
                elif event.button == 5:
                    print("R1")

                #print(event.dict, event.joy, event.button, 'pressed')
            #elif event.type == pygame.JOYBUTTONUP:
            #    print(event.dict, event.joy, event.button, 'released')
            
            #check if the event type is an arrow press
            elif event.type == pygame.JOYHATMOTION:
                print(event.dict, event.joy, event.hat, event.value)

#exit out of the loop Ctrl C is pressed
except KeyboardInterrupt:
    print("EXITING NOW")
    j.quit()
