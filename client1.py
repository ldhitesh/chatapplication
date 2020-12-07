#Lakshmaiah Dinesh, Hitesh
#UTA ID:1001679243
from email.utils import formatdate #used for date formats
from datetime import datetime #used to get the date and time
import tkinter #for GUI
from socket import AF_INET, socket, SOCK_STREAM #import these for safest
from threading import Thread #for multiple executions
import time
import random

client_list=[] # initialize active to empty string
start_val = random.randint(0, 50)
name=""

# function used to encode the messsage into an HTTP format
# input:<message>
# output:<http_format><@@><message>
def Httpmsg(method):
    host = "localhost:33000"  # assigning the host and portnumber
    line_break = "\r\n"  # for line break
    user_agent = "HTTP_CLIENT"  # assigning the user agent an user defined broser
    date = str(datetime.now())  # get sthe date and time of the system

    content_len = len(str(method))  # gets the length of the mesage
    msg1 = "POST" + " " + "/" + " " + "HTTP/1.1" + line_break + "Host: " + host + line_break + "User-Agent: " + user_agent + line_break
    msg2 = msg1 + "content-type:" + "text/plain" + line_break + "Content-Length: " + str(
        content_len) + line_break + "Date: " + date + line_break + line_break +"@@"+ str(method)
    msg = msg2  # assigns the fully concatinated message to msg
    return msg  # returns the concatinated msg


def counter(): #the clock counter starts with this function
    global start_val,client_list,name
    dest="" # initializing the variable to empty string
    send_cnt=0 # initializing the variable to 0
    while True:

        if send_cnt == 7: #checking whether send_Cnt==7
            client_socket.send(bytes("$$","utf8")) # send $$ to server to get the list of clients

            start_val_str=Httpmsg(start_val) #assigning the value we obtained from the Httpmsg function to start_val
            if client_list: #checks if client_list is not empty
                dest = random.choice(client_list) #selects the clients randomly and assigns to dest
                msg_list.insert(tkinter.END, "Local_Val: " + str(start_val) + " send to " + dest) #inserts its values on client window
                client_socket.send(bytes((name + "??" + dest + "##" + start_val_str), "utf8"))  # send the message to server

            send_cnt = 0 #reinitialize the variable to zero

        time.sleep(1) # is used to make the process seep for 1 sec. used for the purpose of counter increment by 1 sec
        start_val = start_val + 1 #start_val increments by 1
        send_cnt = send_cnt + 1  #send_cnt increments by 1




def adjust_clock(src1,remoteTime): #function used to adjust time according to lamports clock
    global start_val
    if (remoteTime < start_val):
        msg_list.insert(tkinter.END, src1 + ":" + str(start_val)) # prints value with the senders name on client window
        msg_list.insert(tkinter.END, "value adjustment not neccesary ") # inserts "value adjustment not neccesary " on client window
    else:
        start_val = remoteTime + 1 #sets the local counter to the new value
        msg_list.insert(tkinter.END, src1 +":" + str(start_val)) # prints value with the senders name on client window
        msg_list.insert(tkinter.END, "value adjusted to->" + str(start_val))  # inserts "value adjusted to with the new new" on client window


# Handles receiving of messages.
def receive():
    global current_entry,client_list,start_val,name, client_socket #global variables are declared so that it can be used anywhere in program

    while True:
        msg = client_socket.recv(BUFSIZ).decode("utf8") #receives message and assigns to the msg variable
        if "!!" not in msg:#symbol "!!" used for the coding purpose
            if "||" in msg:#symbol "||" used for the coding purpose
                src,msg=msg.split("||") #splits the received msg into 2 parts and stores in src and msg variables
                t = int(msg) #t stores the int value of msg
                adjust_clock(src,t)  # calls the function to adjust the counter of the client
            else:
                msg_list.insert(tkinter.END,str(msg)) # prints the msg on clients window
        else:
            client_list1=msg.split("!!") #splits the client_list at "!!"
            del client_list1[0] #deletes the empty value stored in the index 0 of client-list


            for idx,item in enumerate(client_list1): #looping with index
                if item == name: #checks the existece of clients name in client_list
                    client_list1.pop(idx) #removies the src clients name if present
                    break
            client_list=client_list1











def send(event=None):  # event is passed by binders.

    global current_entry,start_val,name  # variable declared globally
    msg = text_box.get()  # takes the info from the tex tbox of the clients window


    if (msg != "quit" and current_entry == 0):  # checks the given condition
        name=msg
        root.title(msg)  # changes the title of the client window to the clients entered name
        client_socket.send(bytes(msg,"utf8"))
        text_box.set("")  # Clears input field.
        current_entry = 1  # changes the value of current_entry

    if msg == "quit":
       on_closing()

    counter_thread = Thread(target=counter)  # receives  thread
    counter_thread.start()  # thread starts





#This function is to be called when the window is closed.
def on_closing(evF66ent=None):
    global name
    client_socket.send(bytes(name+":quit", "utf8"))#send the quit msg to server
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



