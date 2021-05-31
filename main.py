import cv2
import numpy as np
import os

def get_image_name():
    dirs = os.listdir()
    imgDirs = []
    for dir in dirs:
        if dir.find("virtual_paint_image") == 0:
            imgDirs.append(dir)
    num = []
    for dir in imgDirs:
        try:
            num.append(int(dir[19:-4]))
        except ValueError:
            pass
    try:
        number = max(num)
    except ValueError:
        number = 0
    return "virtual_paint_image" + str(number+1) + ".jpg"

cap = cv2.VideoCapture(0)

blue_points = []
yellow_points = []
orange_points = []
lst = []

blue_lower = np.array([100, 80, 0])
blue_upper = np.array([140,255, 255])

yellow_lower = np.array([10, 70, 120])
yellow_upper = np.array([30, 255, 255])

orange_lower = np.array([0, 90, 20])
orange_upper = np.array([10, 255, 255])


while True:
    succeed, img = cap.read()
    imgResult = img.copy()
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    mask_blue = cv2.inRange(imgHSV, blue_lower, blue_upper)
    blue_contours, heirarchy = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    mask_yellow = cv2.inRange(imgHSV, yellow_lower, yellow_upper)
    yellow_contours, heirarchy = cv2.findContours(mask_yellow, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    mask_orange = cv2.inRange(imgHSV, orange_lower, orange_upper)
    orange_contours, heirarchy = cv2.findContours(mask_orange, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for c in blue_contours:
        area = cv2.contourArea(c)
        if area >= 500:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(img, (x, y), (x+w, y+h), (255,0,0), 3)
            cv2.circle(imgResult, (x+w//2, y), 10, (255,0,0), cv2.FILLED)
            blue_points.append((x+w//2, y))
            lst.append((x+w//2, y))
            print(area)

    for c in yellow_contours:
        area = cv2.contourArea(c)
        if area >= 500:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(img, (x, y), (x+w, y+h), (0,255,255), 3)
            cv2.circle(imgResult, (x+w//2, y), 10, (0,255,255), cv2.FILLED)
            yellow_points.append((x+w//2, y))
            lst.append((x+w//2, y))
            print(area)

    for c in orange_contours:
        area = cv2.contourArea(c)
        if area >= 500:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(img, (x, y), (x+w, y+h), (0,0,255), 3)
            cv2.circle(imgResult, (x+w//2, y), 10, (0,0,255), cv2.FILLED)
            orange_points.append((x+w//2, y))
            lst.append((x+w//2, y))
            print(area)

    for point in blue_points:
        cv2.circle(imgResult, point, 10, (255,0,0), cv2.FILLED)
    
    for point in yellow_points:
        cv2.circle(imgResult, point, 10, (0,255,255), cv2.FILLED)
        
    for point in orange_points:
        cv2.circle(imgResult, point, 10, (0,0,255), cv2.FILLED)
    
    # cv2.imshow("Frame", img)
    # cv2.imshow("Mask Yellow", mask_yellow)
    # cv2.imshow("Maks Orange", mask_orange)
    # cv2.imshow("Maks Blue", mask_blue)
    imgResult = cv2.flip(imgResult, 1)
    cv2.imshow("Virtual Paint", imgResult)

    k = cv2.waitKey(10)

    if k == ord('c'):
        blue_points = []
        yellow_points = []
        orange_points = []

    if k == ord('z'):
        pt = lst[-1]
        if pt in blue_points:
            blue_points.remove(pt)
        if pt in yellow_points:
            yellow_points.remove(pt)
        if pt in orange_points:
            orange_points.remove(pt)
        lst.remove(pt)

    if k == ord('s'):
        name = get_image_name()
        cv2.imwrite(name, imgResult)

    if k == ord('w'):
        img = np.zeros_like(img)
        for point in blue_points:
            cv2.circle(img, point, 10, (255,0,0), cv2.FILLED)
        for point in yellow_points:
            cv2.circle(img, point, 10, (0,255,255), cv2.FILLED)
        for point in orange_points:
            cv2.circle(img, point, 10, (0,255,0), cv2.FILLED)
        name = get_image_name()
        cv2.imwrite(name, img)

    if k == ord('q'):
        break
