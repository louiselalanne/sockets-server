import socket
from threading import Thread

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    #(addr family IPV4, TCP socket)

ip_address='127.0.0.1'
port=8000

server.bind((ip_address,port))
server.listen()

clients=[]

print('Server is running...')

def broadcast(message, connection):
    for people in clients:
        if people!=connection:
            try:
                people.send(message.encode('utf-8'))
            except:
                remove(people)

def remove(connection):
    if connection in clients:
        clients.remove(connection)


def clientthread(conn, addr):
    conn.send("Welcome to this chatroom!".encode('utf-8'))
    while True:
        try:
            message = conn.recv(2048).decode('uft-8') #just 2048 bits
            if message:
                print("<"+addr[0]+"> "+message)
                message_to_send = "<"+addr[0]+">"+message
                broadcast(message_to_send,conn)
            else:
                remove(conn) 
        except:
            continue

while True:
    #This accept() method accepts any connection request made to the server and returns 2 parameters -
        #1. The socket object of the client that is trying to connect
        #2. Their IP Address and Port number in the form of a tuple
    conn, addr=server.accept()
    clients.append(conn)
    print(addr[0]+' conected')

    new_thread=Thread(target=clientthread,args=(conn,addr))
    new_thread.start()
