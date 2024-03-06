import cv2 
import pickle
import numpy as np
import cvzone

video = cv2.VideoCapture('carPark.mp4')
out = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), video.get(cv2.CAP_PROP_FPS), (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))))
with open('CarParkPos', 'rb') as f:
    positions = pickle.load(f)
    
def checking_car_parking_space():
    total_parking_available = 0
    for pos in positions:
        x1, y1 = pos
        crop_car_parking_space = frameTF[y1:y1+48, x1:x1+107]
        white_pixel_count = np.sum(crop_car_parking_space == 255)
        if white_pixel_count < 900:
            total_parking_available += 1
            cv2.rectangle(frame, pos, (pos[0] + 107, pos[1] + 42), (0, 255, 0), 4)
        else:
            cv2.rectangle(frame, pos, (pos[0] + 107, pos[1] + 48), (0, 0, 255), 2)
    return total_parking_available

while True:
    ret, frame = video.read()
    frameTF = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frameTF = cv2.GaussianBlur(frameTF, (3, 3), 1)
    frameTF = cv2.adaptiveThreshold(frameTF, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C ,cv2.THRESH_BINARY_INV, 25, 16)
    frameTF = cv2.medianBlur(frameTF, 5)
    kernel = np.ones((3, 3), np.uint8)
    frameTF = cv2.dilate(frameTF, kernel, iterations=1)
    if ret:
        total_parking_available = checking_car_parking_space()
        cvzone.putTextRect(frame, f'{total_parking_available}/69 LEFT', (50, 50))
        cv2.imshow('Video', frame)
        out.write(frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break 
    else:
        break

video.release()
out.release()
cv2.destroyAllWindows()
