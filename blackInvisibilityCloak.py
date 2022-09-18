import cv2
import time
import numpy as np
fourcc = cv2.VideoWriter_fourcc(*"XVID")
output_file = cv2.VideoWriter("output.avi", fourcc, 20.0, (640, 480))
cap = cv2.VideoCapture(0)
time.sleep(2)
bg = 0
for i in range(60):
    ret, bg = cap.read()
bg = np.flip(bg, axis = 1)
while(cap.isOpened()):
    ret, img = cap.read()
    if not ret:
        break
    img = np.flip(img, axis = 1)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_black = np.array([30, 30, 0])
    upper_black = np.array([104, 153, 70])

    mask_1 = cv2.inRange(hsv, lower_black, upper_black)


    lower_black = np.array([30, 30, 20])
    upper_black = np.array([174, 153, 70])

    mask_2 = cv2.inRange(hsv, lower_black, upper_black)

    mask_1 = mask_1 + mask_2


    #Open and expand the image where there is mask 1 (color)
    mask_1 = cv2.morphologyEx(mask_1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    mask_1 = cv2.morphologyEx(mask_1, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8))

    mask_2 = cv2.bitwise_not(mask_1)

    #Keeping only the part of the images without the black color 
    res_1 = cv2.bitwise_and(img, img, mask=mask_2)

    #Keeping only the part of the images with the black color
    res_2 = cv2.bitwise_and(bg, bg, mask=mask_1)

    #Generating the final output by merging res_1 and res_2
    final_output = cv2.addWeighted(res_1, 1, res_2, 1, 0)
    output_file.write(final_output)
    #Displaying the output to the user
    cv2.imshow("Black Screen", final_output)
    cv2.waitKey(1)


cap.release()
out.release()
cv2.destroyAllWindows()
