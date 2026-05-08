import cv2

def draw_box(frame, x, y, w, h):
    x1 = int(x - w/2)
    y1 = int(y - h/2)
    x2 = int(x + w/2)
    y2 = int(y + h/2)

    cv2.rectangle(frame, (x1,y1), (x2,y2), (0,0,255), 2)