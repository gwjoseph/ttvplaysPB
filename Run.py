import string
from Read import getUser, getMessage
from Socket import openSocket, sendMessage
from Init import joinRoom
import stepper as stepper 

s = openSocket()
joinRoom(s)
readbuffer = ""
stepper.setup()
try:
    while True:
	readbuffer = readbuffer + s.recv(1024)
	temp = string.split(readbuffer, "\n")
	readbuffer = temp.pop()
	# TODO: look into storing the commands in a multi deminsion array[[username],[command]]. this will allow pausing of the motors and displaying username with what command was performed. 
	for line in temp:
	    print(line)
	    if "PING" in line:
		print("sending pong back")
		s.send(line.replace("PING", "PONG"))
		break
	    user = getUser(line)
	    message = getMessage(line)
	    print user + " typed :" + message
	    if "You Suck" in message:
		sendMessage(s, "No, you suck!")
		break
	    if "left\r" == message:
		print("MOOOOVE left")
		stepper.moveLeft()
		break
	    if "right\r" == message:
		print("MOOOOOVE right")
		stepper.moveRight()
		break
	    if "up\r" == message:
		print("MOOOOVE up")
		stepper.moveUp()
		break
	    print(message)
	    if "down\r" == message:
		print("MOOOOOVE down")
		stepper.moveDown()
		break	
except KeyboardInterrupt:  # Press ctrl-c to end the program.
    print ('exiting...')
finally:
    stepper.destroy()
