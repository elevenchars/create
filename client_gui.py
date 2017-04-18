import Tkinter as tk
import client


class MainApplication(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.quitButton = tk.Button(self, text="QUIT", command=self.quit)
        self.quitButton.grid(ipadx=500)


class ServerDialog(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.grid()

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

        self.port_label.grid(row=1, sticky=tk.W+tk.E)
        self.port_field.grid(row=1, column=1)

        self.name_label.grid(row=2, sticky=tk.W)
        self.name_field.grid(row=2, column=1)

        self.confirm_button.grid(columnspan=2, sticky=tk.W+tk.E)

    def connect(self):
        print "attempting connection to " + self.ip_field.get() + ":" + self.port_field.get()
        client.connect(self.ip_field.get(), int(self.port_field.get()),self.name_field.get())
dialog = ServerDialog(None)
dialog.mainloop()

# app = MainApplication()
# app.mainloop()
#TODO: make MainApplication work lol