# Arduino through Python

This repository contains two parts: the Python code (request.py) that send requests and the arduino script (2wayCOM.ino) which takes follows the Python Command.

To add more devices:

1. Write the reading/actuating of those devices in Arduino
2. Come up with a unique key word for calling
3. Write a request function in Python using the key word
