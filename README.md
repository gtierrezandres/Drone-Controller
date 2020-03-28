# Drone-Controller
Handy Python script that will allow you to control your Ryze-Tello Drone with your ps4 Controller. Keep in mind that this repository will only work on linux computers. So far, I have tested it on a raspberry pi 4B+ and Ubuntu 18.04 LTS

## Installation
##### Clone and install requirements:
    $ git clone https://github.com/gtierrezandres/Drone-Controller.git
    $ cd Drone-Controller
    $ pip3 install -r requirements.txt
    
##### The following packages might be needed depending on your system:
    $ pip3 install opencv-python
    $ sudo apt-get install libatlas-base-dev
    $ sudo apt-get install libjasper-dev
    $ sudo apt-get install libqtgui4
    $ sudo apt-get install python3-pyqt5
    $ sudo apt-get install libqt4-test

## Optional
##### I would recommend using a virtual environment. You can use venv in the following way (from Drone-Controller directory):
    $ python3 -m venv venv
    $ source venv/bin/activate
    $ pip3 install -r requirements.txt
This will make sure that all the dependencies will be installed properly
    
## drone_driver.py
##### This python script is used to control the drone.
 
## controller.py
##### This python script can be used for testing. The driver code might be extended to other bluetooth devices and this script could be of great aid in testing a new device.
