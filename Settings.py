HOST = "irc.twitch.tv"
PORT = 6667
PASS = open("properties/authCode.txt", "r").read()
CHANNEL = open("properties/user.txt", "r").read()
MOTOR_STEPS = 100 #11 is closest to 1 degree. 
