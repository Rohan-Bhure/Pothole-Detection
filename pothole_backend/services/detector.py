import cv2

def draw_boxes(image_path, preds, output_path):
    image = cv2.imread(image_path)

    for pred in preds:
        x, y, w, h = pred['x'], pred['y'], pred['width'], pred['height']

        x1 = int(x - w/2)
        y1 = int(y - h/2)
        x2 = int(x + w/2)
        y2 = int(y + h/2)

        cv2.rectangle(image, (x1,y1), (x2,y2), (0,0,255), 2)

    cv2.imwrite(output_path, image)
    return output_path