import cv2
from picamera2 import Picamera2
import numpy as np
import sys 
import time 

def detect_and_draw_faces(frame):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        print('Hemos detectado una cara, sonríe')
        print('Proyecto Desbloqueado')
        
    return frame





def detect_color(frame):
    # Define color ranges for red, blue, and black
    lower_red = np.array([0, 0, 100], dtype=np.uint8)
    upper_red = np.array([100, 100, 255], dtype=np.uint8)

    lower_blue = np.array([100, 0, 0], dtype=np.uint8)
    upper_blue = np.array([255, 100, 100], dtype=np.uint8)

    lower_black = np.array([0, 0, 0], dtype=np.uint8)
    upper_black = np.array([50, 50, 50], dtype=np.uint8)

    # Create masks for each color range
    mask_red = cv2.inRange(frame, lower_red, upper_red)
    mask_blue = cv2.inRange(frame, lower_blue, upper_blue)
    mask_black = cv2.inRange(frame, lower_black, upper_black)

    # Count non-zero pixels in each mask
    red_pixels = np.count_nonzero(mask_red)
    blue_pixels = np.count_nonzero(mask_blue)
    black_pixels = np.count_nonzero(mask_black)

    # Check which color has the most non-zero pixels
    max_pixels = max(red_pixels, blue_pixels, black_pixels)

    if max_pixels == red_pixels and max_pixels > 140:
        return "Red"
    elif max_pixels == blue_pixels and max_pixels > 140:
        return "Blue"
    elif max_pixels == black_pixels and max_pixels > 140:
        return "Black"
    else:
        return "Unknown"

def stream_video():
    picam = Picamera2()
    picam.preview_configuration.main.size = (1280, 720)
    picam.preview_configuration.main.format = "RGB888"
    picam.preview_configuration.align()
    picam.configure("preview")
    picam.start()

    colores_objetivo= ['Red', 'Blue', 'Black',' Blue']
    sequence=list()

    while True:
        print(sequence)
        print('Vamos a detectar colores')
        input('Presione tecla para continuar')
        frame = picam.capture_array()
        cv2.imshow("picam", frame)
        # Detect the presence of red, blue, or black color
        color = detect_color(frame)
        print(f"{color} detectado")
        if color!= "Unknown":
            sequence.append(color) 
        if sequence[0]!= "Red":
            sequence= list()
        if len(sequence)>1 and sequence[1]!= "Blue":
            sequence= list()
        if len(sequence)>2 and sequence[2]!= "Black":
            sequence= list()
        if len(sequence)>3 and sequence[3]!= "Blue":
            sequence= list()

        if sequence == colores_objetivo:
            print('Tracker activado')
            while True:
                frame = picam.capture_array()
                frame_with_faces = detect_and_draw_faces(frame)
                cv2.imshow("picam", frame_with_faces)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    stream_video()
