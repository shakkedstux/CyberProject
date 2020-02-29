# Cyber Final Project - Client/User
# by Shakked Stux


import socket
import select
import threading
import pickle
import time
import Tkinter as tk


def main():
    global clientSocket, page, window, frame
    clientSocket = socket.socket()
    port = 7785
    serverIP = '127.0.0.1'
    clientSocket.connect((serverIP,port))

    window = tk.Tk() # tkinter window
    frame = None
    login_page() # the first page - the log-in page(password, username)

    serverIsFine = True
    while serverIsFine: # while server is still working
        rlist, wlist, xlist = select.select([clientSocket], [clientSocket], [])
        if len(rlist) != 0:
            try:
                input = clientSocket.recv(1024)
                a = threading.Thread(target = new_input, args=(input,))
                a.start()
            except: # means server stopped working
                serverIsFine = False
        try:
            window.update()
        except:
            pass
        break_length = 0.1
        time.sleep(break_length)
    print ("Server is not fine.") # serverIsFine = False


 # ||||||||||||||||||||||||||||||||||||||||||||||


def new_input(input):
    data = pickle.loads(input)
    print (data)
    if page == "login":
        msg_login(data)
    if page == "create":
        msg_create(data)
    if page == "waiting for friends list":
        friends_page(data)
    if page == "waiting for friend requests list":
        friend_requests_page(data)

def msg_login(data):
    if data == "no":
        pass
    else:
        chats_list_page(data)
def msg_create(data):
    if data == []:
        chats_list_page(data)
    elif type(data[0]) == bool:
        pass
    else:
        chats_list_page(data)


def send(string):
    x = pickle.dumps(string)
    clientSocket.send(x)




# |||||||||||||||

def create_new_user(username, password):
    send(["create", username, password])

def login(username, password):
    send(["login", username, password])

def send_new_massage_in_chat(chatKey, theMassage):
    send(["massage", chatKey, theMassage])

def create_new_chat(chatName, chatMembers):
    pass

def add_member_to_chat(chatKey, newMemberUsername):
    send(["add", chatKey, newMemberUsername])

def make_him_manager(chatKey, hisUsername):
    send(["manager", chatKey, hisUsername])

def set_his_name(hisUsername, theName):
    send(["name", hisUsername, theName])

def show_me_chat(chatKey):
    send(["show_chat", chatKey])

def show_me_chat_info(chatKey):
    send(["show_info", chatKey])

def show_me_chats_list():
    send("chats_list")


def show_me_friends_list():
    global page
    send(["friends"])
    page = "waiting for friends list"

def send_friend_request(username):
    send(["friend_request", username])

def show_me_friend_requests_list():
    global page
    send(["friend_requests_list"])
    page = "waiting for friend requests list"

# |||||||||||||||




# Visual - (tkinter). (all the PAGES)

def login_page(): # insert your username and password
    global window, frame, page
    page = "login" # state/page
    if frame is not None: # because this is the first window
        frame.destroy() # destroy page
    frame = tk.Frame(window) # create new page
    Entry1 = tk.Entry(frame)
    Entry2 = tk.Entry(frame)
    Button1 = tk.Button(frame, command = lambda: login(Entry1.get(), Entry2.get()))
    Button1.configure(text='''login''')
    Button2 = tk.Button(frame, command = lambda: create_page())
    Button2.configure(text='''i don't have user''')

    frame.pack()
    Entry1.pack()
    Entry2.pack()
    Button1.pack()
    Button2.pack()

def create_page(): # create new user by inserting username and password
    global window, frame, page
    page = "create"
    frame.destroy()
    frame = tk.Frame(window)
    Entry1 = tk.Entry(frame)
    Entry2 = tk.Entry(frame)
    Button1 = tk.Button(frame, command = lambda: create_new_user(Entry1.get(), Entry2.get()))
    Button1.configure(text='''create''')
    Button2 = tk.Button(frame, command = lambda: login_page())
    Button2.configure(text='''i have user''')

    frame.pack()
    Entry1.pack()
    Entry2.pack()
    Button1.pack()
    Button2.pack()

def chats_list_page(data): # (HOME page)
    global window, frame, page
    page = "chats_list"
    frame.destroy()
    frame = tk.Frame(window)

    button = tk.Button(frame, command = lambda: show_me_friends_list())
    button.configure(text='''friends''')

    button.pack()
    frame.pack()


def friends_page(friends):
    global window, frame, page
    page = "friends"
    frame.destroy()
    frame = tk.Frame(window)

    entry = tk.Entry(frame)
    button = tk.Button(frame, command = lambda: show_me_friend_requests_list())
    button.configure(text='''requests''')
    for friend in friends:
        label = tk.Label(frame)
        label.configure(text=friend)
        label.pack()
    entry.pack()
    button.pack()
    frame.pack()


def friend_requests_page(friend_requests):
    global window, frame, page
    page = "friend_requests"
    frame.destroy()
    frame = tk.Frame(window)

    entry = tk.Entry(frame)
    button1 = tk.Button(frame, command = lambda: send_friend_request(entry.get()))
    button1.configure(text='''request''')
    button2 = tk.Button(frame, command = lambda: show_me_friends_list())
    button2.configure(text='''back''')
    for friend_request in friend_requests:
        label = tk.Label(frame)
        label.configure(text=friend_request)
        label.pack()

    entry.pack()
    button1.pack()
    button2.pack()
    frame.pack()


if __name__ == '__main__':
    main()