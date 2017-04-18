import Tkinter as tk
import tkMessageBox
import ScrolledText
import client
import re

class MainApplication(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.parent.title("chat")
        self.parent.iconbitmap("gray75")

        self.grid()
        self.quitButton = tk.Button(self, text="QUIT", command=self.quit)
        self.editArea = ScrolledText.ScrolledText(
            master=self,
            wrap=tk.WORD,
            width=20,
            height=10
        )
        self.create_widgets()

    def create_widgets(self):
        self.editArea.grid(sticky=tk.W+tk.E)
        self.editArea.config(state=tk.DISABLED)
        self.quitButton.grid(ipadx=500)


class ServerDialog(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.grid()
        self.parent = parent
        self.parent.resizable(False, False)
        self.parent.title("connect")
        self.parent.iconbitmap("gray12")

        self.ip_label = tk.Label(self, text="IP address")
        self.ip_field = tk.Entry(self)
        self.port_label = tk.Label(self, text="Port")
        self.port_field = tk.Entry(self)
        self.name_label = tk.Label(self, text="Username")
        self.name_field = tk.Entry(self)
        self.confirm_button = tk.Button(self, text="Connect", command=self.connect)

        self.create_items()

    def create_items(self):
        self.ip_label.grid(row=0, sticky=tk.W)
        self.ip_field.grid(row=0, column=1)

        self.port_label.grid(row=1, sticky=tk.W)
        self.port_field.grid(row=1, column=1)

        self.name_label.grid(row=2, sticky=tk.W)
        self.name_field.grid(row=2, column=1)

        self.confirm_button.grid(columnspan=2, sticky=tk.W+tk.E)

    def connect(self):
        print "attempting connection to " + self.ip_field.get() + ":" + self.port_field.get()
        if(self.validate(self.ip_field.get(), self.port_field.get())):

            if(client.connect(self.ip_field.get(), int(self.port_field.get()),self.name_field.get())):
                self.destroy()
                app = MainApplication(self.parent)
                app.mainloop()
            else:
                print "connection failed"
                tkMessageBox.showerror("error!", "connection failed")
        else:
            tkMessageBox.showerror("error!", "invalid port or ip address")

    def validate(self, ip, port):
        ipPattern = re.compile("^(\d{1,3}\.?){4}$")
        portPattern = re.compile("^(\d{1,5})$")

        if(ipPattern.match(ip) and portPattern.match(port)):
            return True
        return False

root = tk.Tk()
dialog = ServerDialog(root)
dialog.mainloop()

# app = MainApplication()
# app.mainloop()
#TODO: make MainApplication work lol