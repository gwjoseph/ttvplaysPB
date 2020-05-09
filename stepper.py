import RPi.GPIO as GPIO
import time
import sys
import Settings as settings


xAxisMotorPins = (12, 16, 18, 22)    # GPIO pins from the Rpi
xAxisSeqCounter = 0

yAxisMotorPins = (31,33,35,37)
yAxisSeqCounter = 0


seq =  [[1,0,0,0],
        [1,1,0,0],
        [0,1,0,0],
        [0,1,1,0],
        [0,0,1,0],
        [0,0,1,1],
        [0,0,0,1],
        [1,0,0,1]]

#setup the gpio pins for both motors
def setup():
    GPIO.setmode(GPIO.BOARD)
    for pin in xAxisMotorPins:
        GPIO.setup(pin,GPIO.OUT)
        
    for pin in yAxisMotorPins:
        GPIO.setup(pin,GPIO.OUT)

# takes a single half step for the X axis motor and keep track of the GPIO pin output sequence
def stepOneXAxis(direction,ms):
    global xAxisSeqCounter
    for pin in range (len(xAxisMotorPins)):
        if(seq[xAxisSeqCounter][pin] == 1):
            GPIO.output(xAxisMotorPins[pin], True)
        else:
            GPIO.output(xAxisMotorPins[pin], False)
            
    xAxisSeqCounter += direction
        
    if(xAxisSeqCounter > (len(seq)-1)):
        xAxisSeqCounter = 0
    elif(xAxisSeqCounter < 0):
        xAxisSeqCounter = len(seq)-1
    if(ms<3):       # the delay can not be less than 3ms, otherwise it will exceed speed limit of the motor
        ms = 3
    time.sleep(ms*0.001)

# takes a single half step for the Y axis motor and keep track of the GPIO pin output sequence
def stepOneYAxis(direction,ms):
    global yAxisSeqCounter
    for pin in range (len(yAxisMotorPins)):
        if(seq[yAxisSeqCounter][pin] == 1):
            GPIO.output(yAxisMotorPins[pin], True)
        else:
            GPIO.output(yAxisMotorPins[pin], False)
            
    yAxisSeqCounter += direction
        
    if(yAxisSeqCounter > (len(seq)-1)):
        yAxisSeqCounter = 0
    elif(yAxisSeqCounter < 0):
        yAxisSeqCounter = len(seq)-1
    if(ms<3):       # the delay can not be less than 3ms, otherwise it will exceed speed limit of the motor
        ms = 3
    time.sleep(ms*0.001)


# continuous rotation function, the parameter steps specifies the rotation cycles, every four steps is a cycle
def moveSteps(direction, ms, steps, axis):
    # have the axis check on the outside of the loop so you don't do the axis check done on each step loop.
    if(axis == "x"):
        for i in range(steps):
            stepOneXAxis(direction, ms)
    elif(axis == "y"):
        for i in range(steps):
            stepOneYAxis(direction, ms)
            
            
#TODO:  see about having the motors actually turn 1 degree and not 
# method to make the x axis motor turn right        
def moveRight():
   moveSteps(-1,3,settings.MOTOR_STEPS,"x") #11.3777 is a single degree
    
# method to make the x axis motor turn left  
def moveLeft():
    moveSteps(1,3,settings.MOTOR_STEPS,"x") #11.3777 is a single degree

# method to make the y axis motor turn up  
def moveUp():
   moveSteps(1,3,settings.MOTOR_STEPS,"y") #11.3777 is a single degree

# method to make the y axis motor turn down  
def moveDown():
    moveSteps(-1,3,settings.MOTOR_STEPS,"y") #11.3777 is a single degree
        
# function used to stop the x axis motor
def stopXAxisMotor():
    for i in range(len(xAxisMotorPins)):
        GPIO.output(xAxisMotorPins[i],GPIO.LOW)
        
# function used to stop the y axis motor
def stopXAxisMotor():
    for i in range(len(yAxisMotorPins)):
        GPIO.output(yAxisMotorPins[i],GPIO.LOW)

#loop method that will keep an open while loop turning the motors back and forth roughly 360 degrees
def loop():
    while True:
        for i in range (360):
            moveRight()
            moveDown()
        time.sleep(0.5)
        for i in range (360):
            moveLeft()
            moveUp()
        time.sleep(0.5)

# method that will listen for terminal input this is used for testing motors locally and debugging
def userInputLoop():
    while True:
        text = raw_input()
        if(text == "l"):
            moveLeft()
        elif(text == "r"):
            moveRight()

def destroy():
    GPIO.cleanup()  # Release resource
    
# Leaving this main method here incase you need to run the motors locally for debugging
#  if __name__ == '__main__': # Program entrance
     #  print ('Program is starting...')
     #  setup()
     #  try:
        #  loop() 
        #  #userInputLoop()
     #  except KeyboardInterrupt:  # Press ctrl-c to end the program.
         #  print ('exiting...')
     #  finally:
        #  destroy()
