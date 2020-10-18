#!/bin/bash
if [[ -e ngrok ]]; then
echo "[*] Ngrok is already installed, no need to setup."
exit

else

printf "[*] Getting system specifications...\n"
sleep 1
system_info=$(uname -m)

if [[ $system_info == 'x86_64' ]]; then
printf "\n[*] Downloading 64bit version of Ngrok...\n"
wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip
if [[ -e ngrok-stable-linux-amd64.zip ]]; then
unzip ngrok-stable-linux-amd64.zip > /dev/null 2>&1
chmod +x ngrok
rm -rf ngrok-stable-linux-amd64.zip
else
printf "\e[1;93m[!] Download error... Terminal, run:\e[0m\e[1;77m pkg install wget\e[0m\n"
exit 1
fi


if [[ $system_info == 'i686' ]]; then
printf "\n[*] Downloading 32bit verson of Ngrok...\n"
wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-386.zip
if [[ -e ngrok-stable-linux-386.zip ]]; then
unzip ngrok-stable-linux-386.zip > /dev/null 2>&1
chmod +x ngrok
rm -rf ngrok-stable-linux-386.zip
else
printf "\e[1;93m[!] Download error... Terminal, run:\e[0m\e[1;77m pkg install wget\e[0m\n"
exit 1
fi
fi
fi
fi


printf "[+] Ngrok installed."
sleep 1
printf "\n[*] Setting up Ngrok Authtoken...\n"
sleep 1
echo [?] Paste Ngrok Authtoken here:
read authtoken
ngrok authtoken $authtoken
printf "[+] Ngrok activated. Configuring files\n"
cd config
echo $authtoken > ngrok_authtoken.txt
printf "[+] Ngrok authtoken saved to config file.\n"
rm -rf ngrok
sleep 1

printf "\n\e[1;93m[!] Setup status: [1/2]\e[0m"
sleep 1


printf "\n\n[*] Installing the required Python Libraries..."
sleep 1
sudo apt-get install python3-tk
sudo pip3 install pyperclip requests zipfile
pip3 install pyngrok

printf "\n\n\e[1;93m[!] Setup status: [2/2]\e[0m"
printf "\n\n[+] Setup is successfully completed."
exit
