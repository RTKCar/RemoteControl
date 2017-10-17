from socket import *
import RPi.GPIO as GPIO
import time
import sys
from datetime import timedelta
from datetime import datetime

# Pin Definitons:
pwmPinThrottle = 18 # Broadcom pin 18 (P1 pin 12)
directionPin = 23 # Broadcom pin 23 (P1 pin 16)
pwmPinSteering = 12 # Broadcom pin 16 (P1 pin 32)

dc1 = 40 # duty cycle (0-100) for PWM pin
dc2 = 7.5 # duty cycle (0-100) for PWM pin

# Pin Setup:
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(pwmPinThrottle, GPIO.OUT) # PWM pin set as output
GPIO.setup(directionPin, GPIO.OUT) # PWM pin set as output
GPIO.setup(pwmPinSteering, GPIO.OUT) # PWM pin set as output
pwmT = GPIO.PWM(pwmPinThrottle, 50)  # Initialize PWM on pwmPin 50Hz frequency
pwmS = GPIO.PWM(pwmPinSteering, 50)  # Initialize PWM on pwmPin 50Hz frequency

# Initial state for Direction:
GPIO.output(directionPin, GPIO.LOW)
pwmS.start(dc2)
timeStart = datetime.now()

def main(arg):
    print(arg)
    global host
    host = arg

host = 'localhost'
main(sys.argv[1])

#TODO input arg

serverSocket = socket(AF_INET, SOCK_STREAM)
#print('1')
serverSocket.bind(('0.0.0.0', 9000))
#print('2')
serverSocket.listen(1)
#vanta pa att klienten ska connecta
(clientSocket, address) = serverSocket.accept()
#print('accepted')
serverSocket.close()

print("Client: " + str(address[0]) + ":" + str(address[1]) + " connected")
running = True

forward = False
backward = False
right = False
left = False


while running:
    #ta emot 8 byte data, konvertera till utf-8 och printa
    #data = clientSocket.recv(8)
    #num = int(data)
    #data2 = clientSocket.recv(8).decode('ascii')
    data = clientSocket.recv(8).decode('utf-8')
    timeNow = datetime.now()
    deltaTime = (timeStart - timeNow).total_seconds()
    global timeStart
    timeStart = datetime.now()
    if data is 'w':
        forward = not forward
        print('Forward toggle: ' + str(forward))
        if forward:
            GPIO.output(directionPin, GPIO.LOW)
            pwmT.start(dc1)
        else:
            pwmT.stop()
    elif data is 's':
        backward = not backward
        print('Backward toggle: ' + str(backward))
        if backward:
            GPIO.output(directionPin, GPIO.HIGH)
            pwmT.start(dc1)
        else:
            pwmT.stop()
    elif data is 'd':
        right = not right
        print('Right toggle: ' + str(right) + " - " + str(deltaTime))
        print('dc2' , dc2)
            #time.sleep(1)
            #pwmS.stop()
    elif data is 'a':
        left = not left
        print('Left toggle: ' + str(left) + " - " + str(deltaTime))
        print('dc2', dc2)
            #time.sleep(1)
            #pwmS.stop()
    if right and dc2 < 8:
        dc2 = dc2 + 1 * deltaTime
        if dc2 > 8:
            dc2 = 8
        pwmS.ChangeDutyCycle(dc2)
    elif left and dc2 > 6:
        dc2 = dc2 - 1 * deltaTime
        if dc2 < 6:
            dc2 = 6
        pwmS.ChangeDutyCycle(dc2)
    #print("data2: ",data2)
    #print("num: ",num)

clientSocket.close()