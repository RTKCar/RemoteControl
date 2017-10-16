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
    data = clientSocket.recv(8).decode('utf-8')
    if data is 'w':
        forward = not forward
        print('Forward toggle: ' + str(forward))

    print(data)

clientSocket.close()