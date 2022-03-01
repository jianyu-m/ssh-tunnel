import paramiko
from sshtunnel import SSHTunnelForwarder
import tkinter as tk
from pystray import MenuItem as item
import pystray
from PIL import Image, ImageTk
import json

conf = None

with open("ssh.json", "r") as f:
    conf = json.load(f)

tunnels = [(r[0], r[1]) for r in conf['tunnels']]

localPorts = [(r[2], r[3]) for r in conf['tunnels']]

server = SSHTunnelForwarder(
    (conf['server'], conf['port']),
    ssh_username=conf['user'],
    ssh_password=conf['passwd'],
    remote_bind_addresses=tunnels,
    local_bind_addresses=localPorts
)

window = tk.Tk()

has_start = False

def start():
    global button
    global has_start
    if has_start:
        print("Stopping")
        server.stop()
        button['text'] = "Start!"
        has_start = False
    else:
        print("Starting")
        server.start()
        button['text'] = "Stop!"
        has_start = True

button = tk.Button(
    text="Start!",
    width=25,
    height=5,
    command=start,
)
button.pack()

icon = None

def switch_menu():
    return "Stop" if has_start else "Start"

def start_task():
    image=Image.open("ssh.ico")

    menu=(item("Switch", menu_switch), item('Restart', menu_restart),item('Quit', quit_window))
    icon=pystray.Icon("name", image, "SSH Tunnel", menu)
    icon.run()
    return icon

# Define a function for quit the window
def quit_window(icon, item):
    icon.stop()
    # window.destroy()

def hide_window():
   window.withdraw()

def menu_switch():
    start()

def menu_restart():
    start()
    start()

menu_switch()

icon = start_task()

# try:
#     window.mainloop()
# except:
#     print("stop")
#     server.stop()