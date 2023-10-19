import cv2
import numpy as np

img = cv2.imread('YOUR PATH TO PICTURE ')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


edges = cv2.Canny(gray, 50, 150)

contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

hair_mask = np.zeros_like(gray)
face_mask = np.zeros_like(gray)
clothes_mask = np.zeros_like(gray)

for contour in contours:
    area = cv2.contourArea(contour)
    perimeter = cv2.arcLength(contour, True)
    hull = cv2.convexHull(contour)
    hull_area = cv2.contourArea(hull)
    solidity = float(area) / hull_area if hull_area > 0 else 0
    
    if solidity < 0.2:
        hair_mask = cv2.fillPoly(hair_mask, pts=[contour], color=255)
    elif area > 5000:
        face_mask = cv2.fillPoly(face_mask, pts=[contour], color=255)
    else:
        clothes_mask = cv2.fillPoly(clothes_mask, pts=[contour], color=255)

hair_contours = cv2.bitwise_and(img, img, mask=hair_mask)
face_contours = cv2.bitwise_and(img, img, mask=face_mask)
clothes_contours = cv2.bitwise_and(img, img, mask=clothes_mask)

cv2.imshow('Original Image', img)
cv2.imshow('Canny Edges', edges)
cv2.imshow('Hair Contours', hair_contours)
cv2.imshow('Face Contours', face_contours)
cv2.imshow('Clothes Contours', clothes_contours)
cv2.waitKey(0)
cv2.destroyAllWindows()