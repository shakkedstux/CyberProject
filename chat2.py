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

    for i in data:
        print (i)
        """
        chatKey = "Fr"
        button = tk.Button(frame, command = lambda: show_me_chat(chatKey))
        button.configure(text=i)
        button.pack()
        """

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


"""
def login_page():
    global state, root
    state = "create"
    try:
        print("D")
        root.destroy()
    except:
        pass
    root = tk.Tk()
    root.geometry("600x450+650+150")
    root.minsize(148, 1)
    root.maxsize(1924, 1055)
    root.resizable(1, 1)
    root.title("New Toplevel")
    root.configure(background="#d9d9d9")

    Entry1 = tk.Entry(root)
    Entry1.place(relx=0.317, rely=0.244,height=44, relwidth=0.357)
    Entry1.configure(background="white")
    Entry1.configure(disabledforeground="#a3a3a3")
    Entry1.configure(font="TkFixedFont")
    Entry1.configure(foreground="#000000")
    Entry1.configure(insertbackground="black")

    Entry2 = tk.Entry(root)
    Entry2.place(relx=0.317, rely=0.467,height=44, relwidth=0.357)
    Entry2.configure(background="white")
    Entry2.configure(disabledforeground="#a3a3a3")
    Entry2.configure(font="TkFixedFont")
    Entry2.configure(foreground="#000000")
    Entry2.configure(insertbackground="black")

    Button1 = tk.Button(root, command = lambda: login(Entry1.get(), Entry2.get()))
    Button1.place(relx=0.433, rely=0.733, height=33, width=56)
    Button1.configure(activebackground="#ececec")
    Button1.configure(activeforeground="#000000")
    Button1.configure(background="#d9d9d9")
    Button1.configure(disabledforeground="#a3a3a3")
    Button1.configure(foreground="#000000")
    Button1.configure(highlightbackground="#d9d9d9")
    Button1.configure(highlightcolor="black")
    Button1.configure(pady="0")
    Button1.configure(text='''submit''')

    Button2 = tk.Button(root, command = create_page)
    Button2.place(relx=0.833, rely=0.733, height=33, width=56)
    Button2.configure(activebackground="#ececec")
    Button2.configure(activeforeground="#000000")
    Button2.configure(background="#d9d9d9")
    Button2.configure(disabledforeground="#a3a3a3")
    Button2.configure(foreground="#000000")
    Button2.configure(highlightbackground="#d9d9d9")
    Button2.configure(highlightcolor="black")
    Button2.configure(pady="0")
    Button2.configure(text='''i have user''')

def create_page():
    global state, root
    state = "create"
    try:
        print("kk")
        root.destroy()
    except:
        pass
    root = tk.Tk()
    root.geometry("600x450+650+150")
    root.minsize(148, 1)
    root.maxsize(1924, 1055)
    root.resizable(1, 1)
    root.title("New Toplevel")
    root.configure(background="#d9d9d9")

    Entry1 = tk.Entry(root)
    Entry1.place(relx=0.317, rely=0.244,height=44, relwidth=0.357)
    Entry1.configure(background="white")
    Entry1.configure(disabledforeground="#a3a3a3")
    Entry1.configure(font="TkFixedFont")
    Entry1.configure(foreground="#000000")
    Entry1.configure(insertbackground="black")

    Entry2 = tk.Entry(root)
    Entry2.place(relx=0.317, rely=0.467,height=44, relwidth=0.357)
    Entry2.configure(background="white")
    Entry2.configure(disabledforeground="#a3a3a3")
    Entry2.configure(font="TkFixedFont")
    Entry2.configure(foreground="#000000")
    Entry2.configure(insertbackground="black")

    Button1 = tk.Button(root, command = lambda: create_new_user(Entry1.get(), Entry2.get()))
    Button1.place(relx=0.433, rely=0.733, height=33, width=56)
    Button1.configure(activebackground="#ececec")
    Button1.configure(activeforeground="#000000")
    Button1.configure(background="#d9d9d9")
    Button1.configure(disabledforeground="#a3a3a3")
    Button1.configure(foreground="#000000")
    Button1.configure(highlightbackground="#d9d9d9")
    Button1.configure(highlightcolor="black")
    Button1.configure(pady="0")
    Button1.configure(text='''submit''')

    Button2 = tk.Button(root, command = login_page)
    Button2.place(relx=0.833, rely=0.733, height=33, width=56)
    Button2.configure(activebackground="#ececec")
    Button2.configure(activeforeground="#000000")
    Button2.configure(background="#d9d9d9")
    Button2.configure(disabledforeground="#a3a3a3")
    Button2.configure(foreground="#000000")
    Button2.configure(highlightbackground="#d9d9d9")
    Button2.configure(highlightcolor="black")
    Button2.configure(pady="0")
    Button2.configure(text='''i have user''')


class chatsListPage:
    def __init__(self, top):
        global state
        state = "chatsList"
        print("sss")
        top.geometry("600x450+650+150")
        top.minsize(148, 1)
        top.maxsize(1924, 1055)
        top.resizable(1, 1)
        top.title("New Toplevel")
        top.configure(background="#d9d9d9")

        self.Button1 = tk.Button(top, command = self.submit_login)
        self.Button1.configure(activebackground="#ececec")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#d9d9d9")
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''submit''')
        self.Button1.place(relx=0.433, rely=0.733, height=33, width=56)
"""

if __name__ == '__main__':
    main()


"""
first - moving between pages - like example in internet (ctrl + d "frb25") - with frames and classes maybe.
make a pukash design
coding
and finally - improve design


"""