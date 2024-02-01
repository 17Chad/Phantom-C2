# Phantom-C2
Agents written in C, server in Python3.8

To get the server up and listening:

Listening on 0.0.0.0 (all interfaces) port 5000
#python3.8 c2-working.py 

To get the C implant running:

Compile it first, I'm just using gcc  
#gcc -o client main.c networking.c command.c

Then just run it, it should call into the server 127.0.0.1:5000
#./client



