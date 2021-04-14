import socket
import time
from tkinter import *

soc = socket.socket()
soc.connect(("127.0.0.1", 8888))


class ChatBox:
    def __init__(self):
        self.root = Tk()
        self.root.title("chatbot")
        self.root.config(width=600, height=700, bg="#cdd6f2")
        # title
        self.head_line = Label(self.root, bg="#c1b8e9", text="This is your chatbot", font="bold", pady=13.5)
        self.head_line.place(relwidth=1)
        # display area
        self.text_area = Text(self.root, width=20, height=2, bg="#eeeeee", font="9", padx=5, pady=5)
        self.text_area.place(relheight=0.68, relwidth=1, rely=0.08)
        self.text_area.configure(cursor="arrow", state=DISABLED)
        self.text_area.tag_configure("sender", foreground='blue')
        self.text_area.tag_configure("receiver", foreground='green')
        # scrollbar
        self.scroll = Scrollbar(self.text_area)
        self.scroll.place(relheight=1, relx=0.974)
        self.scroll.configure(command=self.text_area.yview)

        # input area
        inputframe = Label(self.root, bg="#eeeeee", height=80)
        inputframe.place(relwidth=1, rely=0.8)

        self.msgbox = Entry(inputframe, bg="#FFFFFF", font="9")
        self.msgbox.place(relwidth=0.8, relheight=0.07, rely=0.003, relx=0.001)
        self.msgbox.focus()
        self.msgbox.bind("<Return>", self.enter)
        # send button
        sendButton = Button(inputframe, text="Send", font="bold", width=12, bg="#eeeeee",
                            command=lambda: self.enter(None))
        sendButton.place(relx=0.805, rely=0.006, relheight=0.065, relwidth=0.20)
        # init
        soc.sendall('[system init]'.encode("utf-8"))
        rep = soc.recv(2048).decode("utf-8")
        inline = 'ChatBot Usage\n'
        self.text_area.configure(state=NORMAL)
        self.text_area.insert(END, inline, 'receiver')
        self.text_area.insert(END, rep)
        self.text_area.configure(state=DISABLED)
        self.text_area.see(END)

    def enter(self, event):
        msg = self.msgbox.get()
        self.sendMassage(msg, "You")

    def sendMassage(self, msg, sender):
        if not msg:
            return

        self.msgbox.delete(0, END)
        # display the current time
        outline = "you: " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + '\n'
        msg1 = msg + "\n\n"

        self.text_area.configure(state=NORMAL)
        self.text_area.insert(END, outline, 'sender')
        self.text_area.insert(END, msg1)
        self.text_area.configure(state=DISABLED)

        # response
        soc.sendall(msg.encode("utf-8"))
        rep = soc.recv(2048).decode("utf-8")
        if msg == "bye":
            soc.close()
            sys.exit()
        msg2 = rep + "\n\n"
        inline = "chatbot: " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + '\n'
        self.text_area.configure(state=NORMAL)
        self.text_area.insert(END, inline, 'receiver')
        self.text_area.insert(END, msg2)
        self.text_area.configure(state=DISABLED)
        self.text_area.see(END)


app = ChatBox()
app.root.mainloop()
