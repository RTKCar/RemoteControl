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
        self._event = False
        self._keyStatus = dict()

    def getEvent(self):
        e = self._event
        self._event = False
        return e

    def on_press(self, key):
        key=key.char

        if key not in self._keyStatus:
            self._keyStatus[key] = False
        if not self._keyStatus[key]:
            self._event = KeyEvent(key, KeyEvent.Event.Pressed)
            self._keyStatus[key] = True


    def on_release(self, key):
        key=key.char
        if key not in self._keyStatus:
            self._keyStatus[key] = True
        if self._keyStatus[key]:
            self._event = KeyEvent(key, KeyEvent.Event.Released)
            self._keyStatus[key] = False


#Borde ligga i KeyboardListener klassen
k = KeyboardListener()
listener = keyboard.Listener(on_press=k.on_press, on_release=k.on_release)

running = False

#Skapar socket med Address Family 'Internet' och är en streaming socket
clientSocket = socket(AF_INET, SOCK_STREAM)
try:
    #Connectar tiill servern och startar keyboard listener
    clientSocket.connect(('localhost', 9000))
    listener.start()
    running = True
except TimeoutError:
    print("Could not connect to server")
    exit(1)

print("Connected to: localhost:9000")
while running:
    if not listener.running:
        listener = keyboard.Listener(on_press=k.on_press, on_release=k.on_release)
        listener.start()
    event = k.getEvent()
    if event is not False:
        if event.type is KeyEvent.Event.Pressed:
            print('key pressed: ' + str(event.key))
            clientSocket.sendall(event.key.encode('utf-8'))
        elif event.type is KeyEvent.Event.Released:
            print('key released: ' + str(event.key))
            clientSocket.sendall(event.key.encode('utf-8'))
