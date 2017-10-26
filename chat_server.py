# server.py
#http://www.bogotobogo.com/python/python_network_programming_server_client.php
#https://stackoverflow.com/questions/21233340/sending-string-via-socket-python
#https://stackoverflow.com/questions/11887291/how-to-add-carriage-return-in-python
#https://stackoverflow.com/questions/39535855/send-receive-data-over-a-socket-python3
#https://www.tutorialspoint.com/python/string_replace.htm
#ruby rubyTestScript.rb 127.0.0.1 random
#midwayguy

import sys
import socket
import select
import re
import traceback

HOST = ''                #creates an arbitrary host
SOCKET_LIST = []         #socket list array
RECV_BUFFER = 4096 
PORT = 9020
SOCK_NAME = {}
CHAT_BUFFER = []


def initialConnection (sock):
            sock.send("Welcome to Nate's chat server\r\n")
            print "initialConnection function finished"
 
def helpRequest (sock):
    print ("Help request sent")
    sock.send(("Chat Server Help:"
        "\nhelp:"
        "\ntest:"
        "\nname:"
        "\nget:"
        "\npush:"
        "\ngetrange:"
        "\nSOME UNRECOGNIZED COMMAND"
        "\nadios: Checks for EOF or CLOSE SOCKET\r\n"))

def testRequest (sock, data):
    print ("Test request sent")
    sock.send(data[6:])

def nameRequest (sock, data):
    print ("Name request sent")
    SOCK_NAME[id(sock)] = data.replace('\r\n', '')[6:] #6: discounts first six chars
    print "new connection name = " + SOCK_NAME[id(sock)]
    sock.send("OK\r\n")

def getRequest (sock):
    print ("Get request sent")
    sock.send("\n".join(CHAT_BUFFER) + "\r\n")

def pushRequest (sock, data):
    print ("Push request sent")
    if id(sock) in SOCK_NAME:
        datName = SOCK_NAME[id(sock)]
    else:
        datName = "unknown"
    CHAT_BUFFER.append("%s: %s" % (datName, data.replace('\r\n', '')[6:]))       
    sock.send("OK\r\n")

def getrangeRequest (sock, data):
    print ("GetRange request sent")
    data = data.strip().decode('utf-8')
    split_data = data.split()
    first_int = int(split_data[1])
    second_int = int(split_data[2])+1    
    sock.send("\n".join(CHAT_BUFFER[first_int: second_int]) + "\r\n" )


def unknownRequest (sock, data):
    print ("Unkown request sent")
    sock.send("Error: unrecognized command: %s" % data)
    print ("Unkown request sent" + "\r\n")


def adiosRequest (sock):
    print ("Adios request sent")
    #sock.send("Adios. You will be missed\n\n")
    if id(sock) in SOCK_NAME:
        print "socket deleted"
        del SOCK_NAME[id(sock)]
    if sock in SOCKET_LIST:
        SOCKET_LIST.remove(sock)
    sock.close()   

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)
 
    # add server socket object to the list of readable connections
    SOCKET_LIST.append(server_socket)
 
    print ("Chat server started on port " + str(PORT))
 
    while 1:
        # get the list sockets which are ready to be read through select
        # 4th arg, time_out  = 0 : poll and never block
        ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)
      
        for sock in ready_to_read:
            print "for loop entered"
            # a new connection request recieved
            if sock == server_socket:
                sockfd, addr = server_socket.accept()
                SOCKET_LIST.append(sockfd)
                print ("Client (%s, %s) connected" % addr)
                initialConnection(sockfd)
                #sockfd.send("Welcome to Nate's chat server")
                print "welcome sent"

            # a message from a client, not a new connection
            else:
                # process data recieved from client, 
                try:
                    # receiving data from the socket.
                    data = sock.recv(RECV_BUFFER)
                    data2 = data.strip().decode('utf-8')
                    split_data = data2.split()
                    first_word = split_data[0]
                    print "if statement entered"

                    
                    if data:
                        #print ("this is the stripped data=="+data)
                        #print ("this is the split data=="+first_word)
                        print data

                        if re.match("^help\r\n$", data):
                            helpRequest(sock)
                        elif re.match("^adios\r\n$", data):
                            adiosRequest(sock)
                        elif re.match("^name:\s[^\r\n]+\r\n$", data):
                            nameRequest(sock, data)
                        elif re.match("^test:\s[^\r\n]+\r\n$", data):
                            testRequest(sock, data)
                        elif re.match("^get\r\n$", data):
                            getRequest(sock)
                        elif re.match("^push:\s[^\r\n]+\r\n$", data):
                            pushRequest(sock, data)
                        elif re.match("^getrange(\s\d+){2}\r\n$", data):
                            getrangeRequest(sock,data)
                        else:
                            unknownRequest(sock,data)

                    else:
                        print "else statement entered"
                        # remove the socket that's broken    
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)
                        # at this stage, no data means probably the connection has been broken
                # exception 
                except Exception, err:
                    print "except"
                    print (traceback.format_exc())
                    print ("Unexpected error:", sys.exc_info()[0])
                    continue

    server_socket.close()

if __name__ == "__main__":
    print ("__name__")
    sys.exit(server())  



                                    

            