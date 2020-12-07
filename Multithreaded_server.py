
from socket import AF_INET, socket, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR # we import the packages used for safest programming over netwrok
from threading import Thread # to handle multiple clients
import tkinter #for GUI

flag=0 #initialing flag to zero
list_of_clients="" #making the list_of_clients an empty string

#It allows the clients to get connected to the server
def accept_incoming_connections():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address) #prints that client address
        client.send(bytes("Greetings from the cave! Now type your name and press enter! OR Type (quit) to exit!", "utf8")) #greeting message at client window when he enters client name
        addresses[client] = client_address # client address is stored in addresses array
        Thread(target=handle_client, args=(client,)).start() # starts a new thread

#the parsing part is done here
#input: <msessage1><**><message2>
#output:msg1=<message2>
def cutdown_req_msg(Httpmsg): # Httpmsg is the encoded message in HTTP format
   msg=Httpmsg.split("**") #splits the msg into two parts at point " ** "
   msg1=msg[1] #stores second part of the splited message
   return msg1 #returns the message without "**" in it

#handles all the clients
def handle_client(client):  # Takes client socket as argument.
    name = client.recv(BUFSIZ).decode("utf8") #recives the name entered by clients and store in variable "name"

    if (name == "" or name == "quit"):      #when the user has not entered the clients name or he types "quit" in the text box
        msg_list.insert(tkinter.END, "client disconnected") #displays the messages when client window is closed without entering name
        for sock1 in clients:    #notify all clients connected that a particular client left
            sock1.send(bytes("%s has left the chat." % name, "utf8"))


    else:# this line exceutes when a new client is connected
        msg = "%s has joined the chat!" % name # when new clients joins server the message is displayed
        client.send(bytes(msg, "utf8"))       #sends notification to all other connected clients
        display = "%s joined with HOST:%s and PORT:%s" % (name, HOST, PORT) #displays at server window with clients name and host and port numbers
        msg_list.insert(tkinter.END, display) #used to display in server window

        broadcast(bytes(msg, "utf8"))#inform all clients tht a new client is joined
        clients[client] = name # clients name is stored
        identity = name # to store that particular clients name

        while True:
            msg = client.recv(BUFSIZ).decode('utf-8') # receive message from client

            if("||") not in msg: #  "||" used to identify the one to one delivery part of the clients code

                if (msg == "quit"): #checks whether message is "wuit" or what
                    client.send(bytes("quit", "utf8")) # send a quit message to client
                    del clients[client] #delete the particular client
                    for sock1 in clients:
                        sock1.send(bytes("%s has left the chat." % name, "utf8")) #broadcast to all connected clients that a particular client left

                elif "^^" not in msg:               #"^^" is used to identity that message is sent using one-to-N delivery method
                    msg, dum = msg.split("@@")      #"@@" used to get only the message part
                    msg = msg + "//" + identity + ":" + dum # concatinate the message with the client name

                    if msg != bytes("quit", "utf8"): #compares msg with the string "quit"
                        msg_list.insert(tkinter.END, msg + "  " + "delivery method: ONE to N")# to display the delivery method
                        msg = "!!" + msg # concatinated with "!!" to ientify at clients side tht it is an one-to N broadcast

                        for sock in clients: # send message to all clients connected
                            sock.send(bytes(msg, "utf8"))
                    else:
                        client.send(bytes("quit", "utf8"))#send "quit" msg to client
                        client.close() #close the client
                        del clients[client] # delete that particular connected client
                        broadcast(bytes("%s has left the chat." % name, "utf8")) # notify all other clients tht the client left
                        break

                else: #to identity that message is sent using one-to-one delivery method

                    msg, dest = msg.split("^^") #split messages to 2 parts at "^^" point
                    msg, dum = msg.split("@@") #"@@" used to get only the message part
                    msg = msg + "//" + identity + ":" + dum #concatinate the msg with the clients name and clients messages

                    msg_list.insert(tkinter.END,msg + "  " + "delivery method: ONE to ONE" + "  " + "destination:" + dest)# to display the delivery method

                    if msg != bytes("quit", "utf8"): #compares msg whether its "quit" string or what
                        if not dest: # checks whether the destination is empty
                            broadcast(msg, name + ": ") #broadcasts the msgs
                        else:
                            for clt_sock in clients: # to run for number of clients times in server
                                if clients[clt_sock] == dest: # if we find the required destination
                                    clt_sock.send(bytes(msg, "utf8")) #send msg to that particular client
                    else:#closing the client
                        client.send(bytes("quit", "utf8"))#send "quit" msg to client
                        client.close() #close the client
                        del clients[client]# delete that particular connected client
                        broadcast(bytes("%s has left the chat." % name, "utf8")) # notify all other clients tht the client left
                        break

            else: # to get the list of active clients connected to the server
                dum12,msg=msg.split("||") #split messages to 2 parts at "||" point
                list_of_clients = msg # for execution puropse
                for sock12 in clients: # concatinates the clients together and assigns to the list_of_clients

                     list_of_clients= list_of_clients + "{"+ str(clients[sock12]) + "}" #keep on adding the connected clients to the list_of_client variable

                client.send(bytes(list_of_clients, "utf8")) #sends the concatinated message of list of clients

# Broadcasts a message to all the clients.
def broadcast(msg, prefix=""):  # prefix is for name identification.
    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)#send msgs to all clients connected to server

#This function is to be called when the window is closed.
def on_closing(evF66ent=None):
    SERVER.close() #closes the server
    root.quit() #wserver window is closed

if __name__ == "__main__": #code starts from here
    root = tkinter.Tk() #initialize the window manager
    root.title("server window") #assigns the titke for server window

    messages_frame = tkinter.Frame(root)# for designing purpose
    scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
    # Following will contain the messages.
    msg_list = tkinter.Listbox(messages_frame, height=15, width=80, yscrollcommand=scrollbar.set) #size of the window
    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)#Adds the scrollable window
    msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)#used for allignment purpose

    msg_list.insert(tkinter.END, "waiting for connections..:") #add a message at the server window before the clients get connected to them
    msg_list.see(tkinter.END) # to see the short messages

    msg_list.pack()# design purpose
    messages_frame.pack()# for gui design purpose
    root.protocol("WM_DELETE_WINDOW", on_closing) # provokes the on_closing function when clicked on close button of the window
    clients = {} #initialize clients to empty array
    addresses = {}  #initialize addresses to empty array

    HOST = "127.0.0.1"   #assign HOST a value
    PORT = 33000         # assign port value
    BUFSIZ = 1024        #declare buffer size
    ADDR = (HOST, PORT)  # tupling host and port

    SERVER = socket(AF_INET, SOCK_STREAM) #we use TCP sockets so AF_INET and SOCK_STREAM
    SERVER.bind(ADDR) #binds the addr

    SERVER.listen(5) # it can listen upto 5 clients maximum
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start() #thread starts from here
    tkinter.mainloop() #gui part
    ACCEPT_THREAD.join() #adds the thread
    SERVER.close() #close the server
