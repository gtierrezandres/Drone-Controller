# Drone-Controller
Handy Python script that will allow you to control your Ryze-Tello Drone with your ps4 Controller

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
    
## Pairing ps4 controller with your computer:
    $ bluetoothctl
    [bluetooth]# power on
    [bluetooth]# agent on
    [bluetooth]# agent-default
    [bluetooth]# scan on
    
##### Now bluetooth devices will apper. Look for your ps4 controller and enter its code:
    [bluetooth]# pair XX:XX:XX:XX:XX:XX
    
