![XSS_scope](https://i.imgur.com/rSRvUx3.png)

XSScope is a XSS payload generator platform with an aim of increaing the impact of an XSS during Bug Hunting. Using 8 modules that XSScope offers, advanced XSS can be simply use with 1 click.

## Features
- Automatic payload generator for Bug Hunting (Blind, Stored, Reflected & DOM XSS)
- Camera Hijacking
- Get every Entry form value that victim enters in the website
- Get victim's cookies (if any)
- Keylogger  
 
 *Funny modules:*  
- Change every link in the website
- Change every image in the website
- Clickjacker (redirect to another URI once user click somewhere on the website)

## Installation
Download the Github repo into your local machine:  
```https://github.com/kleiton0x00/XSScope.git```  
Download all the required libraries:  
```
tk
pyngrok
zipfile
pyperclip
requests
```
Note: Zipfile is not required if you are using Linux/MacOS.

## Usage
**NOTE**: Before running script, make sure to put your [Ngrok Authtoken](https://ngrok.com/) into _/xsscope-master/ngrok_authtoken.txt_  
To run the software, simply enter the command:  
```python3 xsscope.py```

For more detailed usage please refer the [Wiki](https://github.com/kleiton0x00/XSScope/wiki/Usages)

## FAQ
Please refer to the [Wiki](https://github.com/kleiton0x00/XSScope/wiki/FAQ)

## Gallery
#### XSScope IN ACTION
##### XSScope Main Interface.  
![XSScope_in_action1](https://i.imgur.com/0o0Xrfs.png)  
##### Creating an Agent Module.  
![XSScope_in_action2](https://i.imgur.com/ICTM3bo.png)  
##### Generated XSS Payloads  
![XSScope_in_action3](https://i.imgur.com/c7DESrZ.png)  

## Contribution, Credits & License

Ways to contribute

- Suggest a feature
- Report a bug
- Fix something and open a pull request
- Spread the word

Licensed under the GNU GPLv3, see [LICENSE](https://github.com/kleiton0x00/XSScope/blob/master/LICENSE) for more information.

The Favicon Webcam Image generated is taken & modified from [wybircal](https://github.com/wybiral).

## Contact
For any problem, copyright disclaimers, etc. please feel free to email me: ```kurtikleiton@gmail.com```
