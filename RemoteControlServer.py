from socket import *

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('localhost', 9000))
serverSocket.listen(1)
(clientSocket, address) = serverSocket.accept()
serverSocket.close()

print("Client: " + str(address[0]) + ":" + str(address[1]) + " connected")
running = True

forward = False

while running:
    data = clientSocket.recv(8)
    if data is 'w':
        print('Forward toggle: ' + forward)

    print(data.decode('utf-8'))

clientSocket.close()