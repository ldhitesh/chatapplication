
from email.utils import formatdate #used for date formats
from datetime import datetime #used to get the date and time
import tkinter #for GUI
from socket import AF_INET, socket, SOCK_STREAM #import these for safest
from threading import Thread #for multiple executions
from tkinter import simpledialog # for pop up window

active="" # initialize active to empty string

#function used to encode the messsage into an HTTP format
#input:<message>
#output:<http_format><@@><message>
def Httpmsg(method):
    host = "localhost:33000" #assigning the host and portnumber
    line_break = "\r\n" #for line break
    user_agent = "HTTP_CLIENT" #assigning the user agent an user defined broser
    date = str(datetime.now()) #get sthe date and time of the system

    content_len = len(method) #gets the length of the mesage
    msg1 = "POST" + " " + "/" + " " + "HTTP/1.1" + line_break + "Host: " + host + line_break + "User-Agent: " + user_agent + line_break
    msg2 = msg1 + "content-type:" + "text/plain" + line_break + "Content-Length: " + str(
        content_len) + line_break + "Date: " + date + line_break + line_break + "@@" + method
    msg = msg2 #assigns the fully concatinated message to msg
    return msg #returns the concatinated msg

# Handles receiving of messages.
def receive():
    global current_entry,active #global variables are declared so that it can be used anywhere in program
    while True:
        msg = client_socket.recv(BUFSIZ).decode("utf8") #receives message and assigns to the msg variable
        if("{") not in msg: # checks " { " which is used for the logic purpose
            if (msg != "quit"): #checks whether the message is wuit or not
                if "//" not in msg: #"//" used to get the message part with name of the client

                    msg_list.insert(tkinter.END, msg) #displays in the client window

                else:
                    if ("!!") not in msg: #"!!"used  to identify whether it is 1-to-1 or 1-n delivery
                        dum2, msg = msg.split("//") #splits the message at point"//" into 2 parts

                        msg_list.insert(tkinter.END, msg) # displays the  msg with clients name on client window
                        msg_list.insert(tkinter.END, "delivery method:ONE-TO-ONE") # prints the delivery method on window


                    else:
                        dummy, msg = msg.split("!!") #splits the message at point "!!" into 2 parts
                        dum2, msg = msg.split("//")#splits the message at point"//" into 2 parts
                        msg_list.insert(tkinter.END, msg)# displays the  msg with clients name on client window
                        msg_list.insert(tkinter.END, "delivery method:ONE-TO-N")# prints the delivery method on window
            else:
                client_socket.close() #closes the socket

        else:
            active=msg # assigns the msg to active
            msg_uncoded = text_box.get() #takes the information entered in the text box of clients window
            msg_from_client = Httpmsg(msg_uncoded) #passes msg to the Httpmsg function
            msg_from_client = "$$" + msg_from_client #concatinates the "$$" symbol. used for logic purpose
            text_box.set("")  # Clears input field.
            active = "List of Clients:" + active # active is assigned the list of active clients

            answer = tkinter.simpledialog.askstring("Input", active, parent=root) # pop up window comes where client will enter the dest name
            msg_route(msg_from_client + "^^" + answer) #concatinated with symbol to identify the delivery method
            
#function handles the sending of messages
def msg_route(msg_sending):
    if ("$$" or "%%") not in msg_sending: # check the presence of symbols in the msg
        client_socket.send(bytes(msg_sending, "utf8")) #sends the messgae
        if msg_sending == "#quit":
            client_socket.close()#closes the client socket

    elif ("%%") not in msg_sending:  #checks the symbol which is used for the logic purpose of the code
        dummy, msg_sending = msg_sending.split("$$")    #splits the message at point "$$" into 2 parts
        client_socket.send(bytes(msg_sending, "utf8"))#sends the messgae
        if msg_sending == "#quit":
            client_socket.close()#closes the client socket

    elif ("$$") not in msg_sending:#checks the symbol which is used for the logic purpose of the code
        dummy, msg_sending = msg_sending.split("$$") #splits the message at point "$$" into 2 parts
        client_socket.send(bytes(msg_sending, "utf8"))#sends the messgae
        if msg_sending == "#quit":
            client_socket.close()#closes the client socket

def send(event=None):  # event is passed by binders.
    global current_entry #variable declared globally
    msg = text_box.get() #takes the info from the tex tbox of the clients window

    if (msg!="quit" and current_entry == 0):# checks the given condition


        root.title(msg) #changes the title of the client window to the clients entered name

        text_box.set("")  # Clears input field.
        current_entry = 1 #changes the value of current_entry
        msg_route(msg) #calls the function "msg_route" to send msg

        if msg == "quit":
            client_socket.close()#closes the client socket
            root.quit()#window is closed

    elif(msg!="quit" and current_entry != 0): # condition check for code purpose
        msg_list.insert(tkinter.END, "Click on the delievery method")#after entering clients name if client sends msg asks him to slect method

    else:
        client_socket.send(bytes("quit", "utf8"))#  msg is quit sent to server
        client_socket.close() #closes the socket
        root.quit()#window is closed

# one to one delivery
def OTO(event=None):
    global active # globally declares active variable
    client_socket.send(bytes("||" , "utf8"))#sends msg to server with "||" to the lists of active clients



#one to N delivery method
def OTN(event=None):

    msg = text_box.get()#takes the information entered in the text box of clients window
    msg = Httpmsg(msg)#passes msg to the Httpmsg function
    msg_route(msg) #calls the function "msg_route" to send msg
    text_box.set("")  # Clears input field.


#This function is to be called when the window is closed.
def on_closing(evF66ent=None):
    client_socket.send(bytes("quit", "utf8"))#send the quit msg to server
    client_socket.close()#closes the client socket
    root.quit()#close the window



if __name__ == "__main__":#code starts from here
    current_entry = 0 #assigns 0 to current_entry

    root = tkinter.Tk()#initialize the window manager
    root.title("Chatter")#assigns the title for client window

    messages_frame = tkinter.Frame(root)# for GUI designing purpose
    text_box = tkinter.StringVar()  # For the messages to be sent.
    text_box.set("enter your name.") #default message at text box of client window
    scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
    msg_list = tkinter.Listbox(messages_frame, height=15, width=80, yscrollcommand=scrollbar.set)#size of the window
    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y) #Adds the scrollable property
    msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)#used for allignment purpose
    msg_list.pack()# GUI design purpose
    messages_frame.pack()# GUI design purpose

    entry_field = tkinter.Entry(root, textvariable=text_box) #space to enter the messages
    entry_field.bind("<Return>", send)
    entry_field.pack()#packs widgets into single pack
    send_button = tkinter.Button(root, text="Send", command=send)# send the msg when clicked on the send button to the send function
    send_button.pack()
    send_button = tkinter.Button(root, text="ONE-TO-ONE", command=OTO)# send the msg when clicked on the OTO button to the send function
    send_button.pack()
    send_button = tkinter.Button(root, text="ONE-TO-N", command=OTN)# send the msg when clicked on the OTN button to the send function
    send_button.pack()
    root.protocol("WM_DELETE_WINDOW", on_closing) #calls the on_Closing function when cicked on exit button on the window

    # ----Now comes the sockets part----
    HOST = "127.0.0.1" #assigns the value to the host
    PORT = 33000  #assigns the value to the port

    BUFSIZ = 1024 #defines the buffer size
    ADDR = (HOST, PORT) #tuples the host and port togethr

    client_socket = socket(AF_INET, SOCK_STREAM) #we use TCP sockets so AF_INET and SOCK_STREAM
    client_socket.connect(ADDR) #connect the socket to the mentioned address
    print(client_socket) #prints the clientsocket on console

    receive_thread = Thread(target=receive) #receives  thread
    receive_thread.start() #thread starts
    tkinter.mainloop()  # Starts GUI execution.
