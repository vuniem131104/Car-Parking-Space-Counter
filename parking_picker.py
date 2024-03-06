import cv2 
import pickle 

try:
    with open('CarParkPos', 'rb') as f:
        positions = pickle.load(f)
except:
    positions = []
h, w = 48, 107

def mouse_click(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        positions.append((x, y))
    if event == cv2.EVENT_RBUTTONDOWN:
        for idx, pos in enumerate(positions):
            x1, y1 = pos 
            if x1<x<x1+w and y1<y<y1+h:
                positions.pop(idx)
                
    with open('CarParkPos', 'wb') as f:
        pickle.dump(positions, f)
        

while True:
    img = cv2.imread('carParkImg.png')
    for pos in positions:
        cv2.rectangle(img, pos, (pos[0] + w, pos[1] + h), (255,0,255), 2)
    cv2.imshow('Image', img)
    cv2.setMouseCallback('Image', mouse_click)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break 