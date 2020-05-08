import RPi.GPIO as GPIO
import time
import sys


xAxisMotorPins = (12, 16, 18, 22)    # GPIO pins from the Rpi
xAxisSeqCounter = 0

yAxisMotorPins = (31,33,35,37)
yAxisSeqCounter = 0


seq =   [
        [1,0,0,0],
        [1,1,0,0],
        [0,1,0,0],
        [0,1,1,0],
        [0,0,1,0],
        [0,0,1,1],
        [0,0,0,1],
        [1,0,0,1]
        ]


def setup():
    GPIO.setmode(GPIO.BOARD)       # use PHYSICAL GPIO Numbering
    for pin in xAxisMotorPins:
        GPIO.setup(pin,GPIO.OUT)
        
    for pin in yAxisMotorPins:
        GPIO.setup(pin,GPIO.OUT)

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
def moveSteps(direction, ms, steps,axis):
    if(axis == "x"):
        for i in range(steps):
            stepOneXAxis(direction, ms)
    else:
        for i in range(steps):
            stepOneYAxis(direction, ms)
            
        
def moveRight():
   moveSteps(1,3,11,"x") #11.3777 is a single degree
    
def moveLeft():
    moveSteps(-1,3,11,"x") #11.3777 is a single degree
        
def moveUp():
   moveSteps(1,3,11,"y") #11.3777 is a single degree
    
def moveDown():
    moveSteps(-1,3,11,"y") #11.3777 is a single degree
        
# function used to stop motor
def motorStop():
    for i in range(0,4,1):
        GPIO.output(motorPins[i],GPIO.LOW)
            
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


def userInputLoop():
    while True:
        text = raw_input()
        if(text == "l"):
            moveLeft()
        elif(text == "r"):
            moveRight()

def destroy():
    GPIO.cleanup()             # Release resource
    
if __name__ == '__main__': # Program entrance
     print ('Program is starting...')
     setup()
     try:
        loop() 
        #userInputLoop()
     except KeyboardInterrupt:  # Press ctrl-c to end the program.
         print ('exiting...')
         #destroy() #leaving this here incase I want to use this for something, but the finally block is handling the destroy
     finally:
        destroy()
