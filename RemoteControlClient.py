from pynput import keyboard
from socket import *

class KeyEvent:
    class Event:
        Pressed = 1
        Released = 2

    def __init__(self, key="", type=0):
        self.key = key
        self.type = type

class KeyboardListener:
    def __init__(self):
        self._event = list()
        self._keyStatus = dict()

    def getEvent(self):
        if(self._event):
            return self._event.pop(0)
        return False

    def on_press(self, key):
        key=key.char

        if key not in self._keyStatus:
            self._keyStatus[key] = False
        if not self._keyStatus[key]:
            self._event.append(KeyEvent(key, KeyEvent.Event.Pressed))
            self._keyStatus[key] = True


    def on_release(self, key):
        key=key.char
        if key not in self._keyStatus:
            self._keyStatus[key] = True
        if self._keyStatus[key]:
            self._event.append(KeyEvent(key, KeyEvent.Event.Released))
            self._keyStatus[key] = False

def main(arg):
    print(arg)
    global host
    host = arg

#Borde ligga i KeyboardListener klassen
k = KeyboardListener()
listener = keyboard.Listener(on_press=k.on_press, on_release=k.on_release)

running = False

host = '192.168.43.101'
main(sys.argv[1])

#Skapar socket med Address Family 'Internet' och är en streaming socket
clientSocket = socket(AF_INET, SOCK_STREAM)
try:
    #Connectar tiill servern och startar keyboard listener
    clientSocket.connect((host, 9000))
    listener.start()
    running = True
except TimeoutError:
    print("Could not connect to server")
    exit(1)

print("Connected to:", host, ":9000")
#print("Connected to: localhost:9000")
while running:
    if not listener.running:
        listener = keyboard.Listener(on_press=k.on_press, on_release=k.on_release)
        listener.start()
    event = k.getEvent()
    if event:
        if event.type is KeyEvent.Event.Pressed:
            print('key pressed: ' + str(event.key))
            #data = event.key + ':1'
            #clientSocket.sendall(data.encode('utf-8'))
            clientSocket.sendall(event.key.encode('utf-8'))
        elif event.type is KeyEvent.Event.Released:
            print('key released: ' + str(event.key))
            #data = event.key + ':0'
            #clientSocket.sendall(data.encode('utf-8'))
            clientSocket.sendall(event.key.encode('utf-8'))
