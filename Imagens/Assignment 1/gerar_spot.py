import cv2

img = cv2.imread("spots.tif")
cv2.imshow("ver", img)
cv2.waitKey(0)
white = (255, 255, 255)
img[177, 214] = img[176:178, 213] = img[175,213] = img[178:180,215] = white
img[179:182,216] = img[181:183,217] = img[173, 211] = img[174:177, 212] = img[178, 214] = white
img[182:184,217:219] = white
cv2.imshow("ver2", img)
cv2.waitKey(0)
cv2.imwrite("newSpots.tif", img)