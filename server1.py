# Lakshmaiah Dinesh, Hitesh
# UTA ID:1001679243
from socket import AF_INET, socket, SOCK_STREAM, SOL_SOCKET, \
    SO_REUSEADDR  # we import the packages used for safest programming over netwrok
from threading import Thread  # to handle multiple clients
import tkinter  # for GUI
import time
import random

list_of_clients = ""


# It allows the clients to get connected to the server
def accept_incoming_connections():
    while True:
        client, client_address = SERVER.accept()
        # print("%s:%s has connected." % client_address) #prints that client address
        # client.send(bytes("Greetings from the cave! Now type your name and press enter! OR Type (quit) to exit!", "utf8")) #greeting message at client window when he enters client name
        addresses[client] = client_address  # client address is stored in addresses array
        Thread(target=handle_client, args=(client,)).start()  # starts a new thread


# handles all the clients
def handle_client(client):  # Takes client socket as argument.
    global list_of_clients
    name = client.recv(BUFSIZ).decode("utf8")  # recives the name entered by clients and store in variable "name"
    identity = name

    if (
            name == "" or name == "quit"):  # when the user has not entered the clients name or he types "quit" in the text box
        msg_list.insert(tkinter.END,
                        "client disconnected")  # displays the messages when client window is closed without entering name
        for sock1 in clients:  # notify all clients connected that a particular client left
            sock1.send(bytes("%s has left the chat." % name, "utf8"))


    else:  # this line exceutes when a new client is connected
        msg = "%s has joined the chat!" % name  # when new clients joins server the message is displayed
        client.send(bytes(msg, "utf8"))  # sends notification to all other connected clients
        display = "%s joined with HOST:%s and PORT:%s" % (
        name, HOST, PORT)  # displays at server window with clients name and host and port numbers
        msg_list.insert(tkinter.END, display)  # used to display in server window

        # broadcast(bytes(msg, "utf8"))#inform all clients tht a new client is joined
        clients[client] = name  # clients name is stored


        while True:
            msg = client.recv(BUFSIZ).decode('utf-8')  # receive message from client
            if ":quit" in msg:
                quitClient,dummy = msg.split(":")
                for item in clients:
                    if clients[item] == quitClient:
                        del clients[item]
                        break



            else:

                if "$$" not in msg: # checks whether "$$" present in msg
                    msg, msg1 = msg.split("@@") #splits the msg int 2 part at @@
                    addr,msg=msg.split("##") #splits the msg int 2 part at @@
                    msg = msg + identity + ":" + msg1 #concatenate the msg with the identity i.e client name
                    headers = msg.split("\r\n") #split the msg at "\r\n" and store in headers
                    for item in headers:
                        msg_list.insert(tkinter.END, item) # insert all items present in headers on server window

                    addr_src,addr_dest=addr.split("??")  #splits the msg int 2 part at ??
                    for clt_sock in clients:  # to run for number of clients times in server
                        if clients[clt_sock] == addr_dest:  # if we find the required destination
                            clt_sock.send(bytes(addr_src + "||" + msg1, "utf8"))  # send msg to that particular client



                else:
                    list_of_clients = ""

                    for sock_cli in clients:
                        list_of_clients = list_of_clients + "!!" + clients[sock_cli]
                    client.send(bytes(list_of_clients, "utf8"))  # send msg to that particular client


# Broadcasts a message to all the clients.
def broadcast(msg, prefix=""):  # prefix is for name identification.
    for sock in clients:
        sock.send(bytes(prefix + msg, "utf8"))  # send msgs to all clients connected to server


# This function is to be called when the window is closed.
def on_closing(evF66ent=None):
    SERVER.close()  # closes the server
    root.quit()  # wserver window is closed


if __name__ == "__main__":  # code starts from here
    root = tkinter.Tk()  # initialize the window manager
    root.title("server window")  # assigns the titke for server window

    messages_frame = tkinter.Frame(root)  # for designing purpose
    scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
    # Following will contain the messages.
    msg_list = tkinter.Listbox(messages_frame, height=15, width=80, yscrollcommand=scrollbar.set)  # size of the window
    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)  # Adds the scrollable window
    msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)  # used for allignment purpose

    msg_list.insert(tkinter.END,
                    "waiting for connections..:")  # add a message at the server window before the clients get connected to them
    msg_list.see(tkinter.END)  # to see the short messages

    msg_list.pack()  # design purpose
    messages_frame.pack()  # for gui design purpose
    root.protocol("WM_DELETE_WINDOW",
                  on_closing)  # provokes the on_closing function when clicked on close button of the window
    clients = {}  # initialize clients to empty array
    addresses = {}  # initialize addresses to empty array

    HOST = "127.0.0.1"  # assign HOST a value
    PORT = 33000  # assign port value
    BUFSIZ = 1024  # declare buffer size
    ADDR = (HOST, PORT)  # tupling host and port

    SERVER = socket(AF_INET, SOCK_STREAM)  # we use TCP sockets so AF_INET and SOCK_STREAM
    SERVER.bind(ADDR)  # binds the addr

    SERVER.listen(5)  # it can listen upto 5 clients maximum
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()  # thread starts from here
    tkinter.mainloop()  # gui part
    ACCEPT_THREAD.join()  # adds the thread
    SERVER.close()  # close the server

