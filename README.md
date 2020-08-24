![XSS_scope](https://i.imgur.com/rSRvUx3.png)

XSScope is a XSS payload generator platform with an aim of increaing the impact of an XSS during Bug Hunting by remote hijacking webcam and keylogging.

## Features
- Automatic payload generator for Bug Hunting
- Camera Hijacking
- Keylogger

## Installation
Download the Github repo into your local machine:  
```https://github.com/kleiton0x00/XSScope.git```  
Download pyngrok for Python3 in Linux:  
```pip3 install pyngrok```

## Usage
**NOTE**: Before running script, make sure to put your [Ngrok Authtoken](https://ngrok.com/) into _/xsscope-master/ngrok_authtoken.txt_  
To run the software, simply enter the command:  
```python3 server.py```

For more detailed usage please refer the Wiki.

## Contribution, Credits & License

Ways to contribute

- Suggest a feature
- Report a bug
- Fix something and open a pull request
- Spread the word

Licensed under the GNU GPLv3, see [LICENSE](https://github.com/kleiton0x00/XSScope/blob/master/LICENSE) for more information.

The Favicon Webcam Image generated is taken & modified from [wybircal](https://github.com/wybiral).
