import Tkinter as tk
import tkMessageBox
import ScrolledText
import client
import re


class ChatWindow(tk.Frame):  # chat window, runs after dialog has prompted user and connected to server
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent  # store root window, set name and icon
        self.parent.title("chat")
        self.parent.iconbitmap("gray75")
        self.parent.resizable(True, True)

        self.grid(sticky=tk.N+tk.S+tk.E+tk.W)  # create widgets
        self.quitButton = tk.Button(self, text="QUIT", command=self.quit)
        self.editArea = ScrolledText.ScrolledText(
            master=self,
            wrap=tk.WORD,
            width=20,
            height=10
        )
        self.inputFrame = tk.Frame(self)
        self.textField = tk.Entry(self.inputFrame)
        self.submitButton = tk.Button(self.inputFrame, text="send", command=self.send_message)

        listener = client.ServerListener(self.update_messages)  # start listener for server
        listener.start()
        self.create_widgets()  # add widgets to the window

    def create_widgets(self):
        self.editArea.grid(sticky=tk.N+tk.S+tk.E+tk.W)  # place chat content window and set it to uneditable
        self.editArea.config(state=tk.DISABLED)
        self.textField.grid(row=0, column=0, sticky=tk.W)  # create bottom bar
        self.submitButton.grid(row=0, column=1, sticky=tk.E)
        self.inputFrame.grid(sticky=tk.N+tk.S+tk.E+tk.W)

    def update_messages(self, content):  # make content window editable, modify, and set to uneditable
        self.editArea.config(state=tk.NORMAL)
        if("name" in content):  # do formatting for command vs chat message
            self.editArea.insert(tk.END, content["name"] + " > " + content["body"] + "\n")
        else:
            self.editArea.insert(tk.END, content["body"] + "\n")
        self.editArea.config(state=tk.DISABLED)

    def send_message(self):  # send message to server if not blank
        if(self.textField.get() != ""):
            client.send({"type" : "message",
                         "body" : self.textField.get()})
            self.textField.delete(0, tk.END)


class ServerDialog(tk.Frame):  # dialog for getting input from user and connecting
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.grid()  # store root window, set name and icon
        self.parent = parent
        self.parent.resizable(False, False)
        self.parent.title("connect")
        self.parent.iconbitmap("gray12")

        self.ip_label = tk.Label(self, text="IP address")  # create widgets
        self.ip_field = tk.Entry(self)
        self.port_label = tk.Label(self, text="Port")
        self.port_field = tk.Entry(self)
        self.name_label = tk.Label(self, text="Username")
        self.name_field = tk.Entry(self)
        self.confirm_button = tk.Button(self, text="Connect", command=self.connect)

        self.create_widgets()  # add widgets to the window

    def create_widgets(self):
        self.ip_label.grid(row=0, sticky=tk.W)
        self.ip_field.grid(row=0, column=1)

        self.port_label.grid(row=1, sticky=tk.W)
        self.port_field.grid(row=1, column=1)

        self.name_label.grid(row=2, sticky=tk.W)
        self.name_field.grid(row=2, column=1)

        self.confirm_button.grid(columnspan=2, sticky=tk.W+tk.E)

    def connect(self):  # connect to server, prompt for input again if connection fails
        print "attempting connection to " + self.ip_field.get() + ":" + self.port_field.get()
        if(self.validate(self.ip_field.get(), self.port_field.get())):
            if(client.connect(self.ip_field.get(), int(self.port_field.get()),self.name_field.get())):
                self.destroy()
                app = ChatWindow(self.parent)
                app.mainloop()
            else:
                print "connection failed"
                tkMessageBox.showerror("error!", "connection failed")
                client.recreate_socket()
        else:
            tkMessageBox.showerror("error!", "invalid port or ip address")

    def validate(self, ip, port):  # validate that the input matches regex for ip and port
        ipPattern = re.compile("^(\d{1,3}\.?){4}$")
        portPattern = re.compile("^(\d{1,5})$")

        if(ipPattern.match(ip) and portPattern.match(port)):
            return True
        return False

root = tk.Tk()  # start root menu and configure
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
dialog = ServerDialog(root)
dialog.mainloop()
