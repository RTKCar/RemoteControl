from socket import *

host = 'localhost'

#skapa en streamingsocket med adresstyp internet (TCP) som väntar på klienten
serverSocket = socket(AF_INET, SOCK_STREAM)
#print('1')
serverSocket.bind((host, 9000))
#print('2')
serverSocket.listen(1)

#print('väntar på client')
#vänta på att klienten ska connecta
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
    if data is 'w':
        forward = not forward
        print('Forward toggle: ' + str(forward))
    elif data is 's':
        backward = not backward
        print('Backward toggle: ' + str(backward))
    elif data is 'a':
        left = not left
        print('Left toggle: ' + str(left))
    elif data is 'd':
        right = not right
        print('Right toggle: ' + str(right))
    else:
        print("data: ",data)
    #print("data2: ",data2)
    #print("num: ",num)

clientSocket.close()

def main(arg):
    print(arg)
    global host
    host = arg

main(sys.argv[1])