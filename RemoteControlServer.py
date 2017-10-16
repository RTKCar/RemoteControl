from socket import *

#skapa en streamingsocket med adresstyp internet (TCP) som väntar på klienten
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('localhost', 9000))
serverSocket.listen(1)

#vänta på att klienten ska connecta
(clientSocket, address) = serverSocket.accept()
serverSocket.close()

print("Client: " + str(address[0]) + ":" + str(address[1]) + " connected")
running = True

forward = False

while running:
    #ta emot 8 byte data, konvertera till utf-8 och printa
    data = clientSocket.recv(8).decode('utf-8')
    if data is 'w':
        forward = not forward
        print('Forward toggle: ' + str(forward))

    print(data)

clientSocket.close()