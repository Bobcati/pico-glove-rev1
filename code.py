#import board support libraries, including HID.
import board
import digitalio
import analogio
import usb_hid

#import imu library
import adafruit_mpu6050                  
import busio
from math import atan2, degrees

from time import sleep
 
#set up IMU
i2c = busio.I2C(board.GP15, board.GP14)
mpu = adafruit_mpu6050.MPU6050(i2c)
 
#Libraries for communicating as a Keyboard device
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)

#Define buttons        
spaceButton = digitalio.DigitalInOut(board.GP9)
spaceButton.direction = digitalio.Direction.INPUT
spaceButton.pull = digitalio.Pull.UP

rightButton = digitalio.DigitalInOut(board.GP2)
rightButton.direction = digitalio.Direction.INPUT
rightButton.pull = digitalio.Pull.UP

leftButton = digitalio.DigitalInOut(board.GP6)
leftButton.direction = digitalio.Direction.INPUT
leftButton.pull = digitalio.Pull.UP

modeSwitch = digitalio.DigitalInOut(board.GP21)
modeSwitch.direction = digitalio.Direction.INPUT 
modeSwitch.pull = digitalio.Pull.UP

mode = 1

def debounce():
    sleep(0.04)                

def vector_2_degrees(x, y):
    angle = degrees(atan2(y, x))
    if angle < 0:
        angle += 360
    return angle


# Given an accelerometer sensor object return the inclination angles of X/Z and Y/Z
# Returns: tuple containing the two angles in degrees
def get_inclination(_sensor):
    x, y, z = _sensor.acceleration
    return vector_2_degrees(x, z), vector_2_degrees(y, z)

                                             
while True:
    #print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (mpu.acceleration))                
    #print("Gyro X:%.2f, Y: %.2f, Z: %.2f degrees/s" % (mpu.gyro))
    # sleep(0.01)
    angle_xz, angle_yz = get_inclination(mpu)
    print("XZ angle = {:6.2f}deg   YZ angle = {:6.2f}deg".format(angle_xz, angle_yz))
    #sleep(0.2)
    if not spaceButton.value: 
        keyboard.press(Keycode.SPACE)
        debounce()  
    #Gyroscope control mode
    if mode == 1:              
        if not spaceButton.value: 
            keyboard.press(Keycode.SPACE)
            debounce()  
        if angle_xz > 120 and angle_xz < 150:
            keyboard.press(Keycode.RIGHT_ARROW)
            debounce()
        elif angle_xz > 270 and angle_xz < 320:
            keyboard.press(Keycode.LEFT_ARROW)         
            debounce() 
        elif angle_xz < 270 and angle_xz > 260:
            keyboard.release(Keycode.LEFT_ARROW)                     
            keyboard.release(Keycode.RIGHT_ARROW)                                        
            debounce()
        if not modeSwitch.value:
            mode = 2
            print("mode switched to: " + str(mode))
            debounce()
            sleep(0.5)
    #Manual control mode
    elif mode == 2:
        if not spaceButton.value:                                
            keyboard.press(Keycode.SPACE)
            debounce() 
        if not leftButton.value:                                                                                                     
            keyboard.press(Keycode.LEFT_ARROW)
            print("left")
        elif not rightButton.value:
            keyboard.press(Keycode.RIGHT_ARROW)
            print("right")
        else:
            keyboard.release(Keycode.LEFT_ARROW)                     
            keyboard.release(Keycode.RIGHT_ARROW)                                        
            debounce()
        if not modeSwitch.value:
            mode = 1
            print("mode switched to: " + str(mode))
            debounce()
            sleep(0.5)
    keyboard.release(Keycode.SPACE)
    keyboard.release(Keycode.LEFT_ARROW)
    keyboard.release(Keycode.RIGHT_ARROW)
    debounce()
    
