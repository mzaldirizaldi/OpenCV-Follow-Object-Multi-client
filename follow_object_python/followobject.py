import socket
import cv2
import numpy as np
import serial

cap = cv2.VideoCapture(1) # Camera 1
color_lower = np.array([105, 100, 125], np.uint8) #color HSV lower
color_upper = np.array([130, 255, 230], np.uint8) #color HSV upper

subs = 'RESET' #variable detect reset button (currently not working).
arduReset = '#' #variable sending '#' to Arduino

host = '192.168.18.229' #IP
port = 9999 #port
s = socket.socket()

arduino = serial.Serial(port='COM3', baudrate=115200, timeout=2) #Arduino

print('Waiting for connection..') #connecting to server
try:
    s.connect((host, port))
except socket.error as e:
    print(str(e))

print('Connected!')

while True: #capture and detect color (blue)
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (320, 240))
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, color_lower, color_upper)
    contours, _= cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)
    rows, cols, _ = frame.shape
    center_x = int(rows / 2)
    center_y = int(cols / 2)

    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        medium_x = int((x + x + w) / 2) #finding medium
        medium_y = int((y + y + h) / 2)
        obj_x = round(medium_x / 10) #divide the medium by 10 and round the value (for better reading at Arduino)
        obj_y = round(medium_y / 10)

        cv2.line(frame, (medium_x, 0), (medium_x, 480), (0, 255, 0), 2)
        text2 = "mediumX = " + str(medium_x)
        cv2.putText(frame, text2, (0, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.50, (0, 0, 255))

        cv2.line(frame, (0, medium_y), (640, medium_y), (0, 255, 0), 2)
        text3 = "mediumY = " + str(medium_y)
        cv2.putText(frame, text3, (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.50, (0, 0, 255))

        line = arduino.readline()
        string = 'X{0:d}Y{1:d}\n'.format((obj_x), (obj_y)) #string to send to Arduino
        coor = '{0:d}X{1:d}Y{2:s}\n'.format((medium_x), (medium_y), (line.decode('utf-8'))) #string to send to server

        if 'A' in line.decode(): #for detecting if there are null values from servo values
            s.send(coor.encode('utf-8'))
        else:
            s.send("0X0Y0A0B".encode('utf-8'))

        response = s.recv(1024)
        msg = response.decode('utf-8')
        print(msg)

        if subs in msg: #sending reset instruction to Arduino (currently not working)
            arduino.write(arduReset.encode('utf-8'))
            print(arduReset)
        else:
            arduino.write(string.encode('utf-8'))
        break

    cv2.imshow("Output", frame)
    key = cv2.waitKey(1)
    cv2.waitKey(1)
    cv2.waitKey(1)
    cv2.waitKey(1)
    cv2.waitKey(1)
    if key == ord("q"):
        break
s.close()
cv2.destroyAllWindows()
cv2.waitKey(1)
cv2.waitKey(1)
