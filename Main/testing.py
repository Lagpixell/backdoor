import cv2
def webcamsnap_get():
    try:
        cam = cv2.VideoCapture(0)
        r, frame = cam.read()
        if r != True:
            raise ValueError("Can't read frame")

        cv2.imwrite('cam.png', frame)

        #cv2.waitKey()
        
        
    except Exception as e:
        print("[!] Couldn't get a snap of the webcam: {}.".format(e))


def file_len(filename):
    with open(filename, "rb") as f:
        print("1")
        data = f.read()
        print(len(data))


x = 1
if x == 1:
    
    webcamsnap_get()
    file_len("cam.png")

