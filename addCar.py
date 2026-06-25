import cv2
import numpy as np
import random
from createPlane import plane

car_png = cv2.imread('car_gray.png', cv2.IMREAD_UNCHANGED)

if car_png is None:
    print("Car image is not found.")
else:
    car_width = 15  #arabanın genişliği
    car_height = 31 #arabanın boyutu
    car_png = cv2.resize(car_png, (car_width, car_height)) #arabaların yeni boyutu

    copied_plane = plane.copy() #Başta yaptığımız düzlemi kopyaladık

    car_bgr = car_png[:, :, :3]
    car_mask = car_png[:, :, 3] / 255.0

    plane_height, plane_width, _ = copied_plane.shape #Kopyalanan düzlemin boy ve en değerlerini alır.

    numberOfCars = 5 #Düzlemde istediğimiz araba sayısı.

    for _ in range(numberOfCars):  #Belirtilen adet kadar döngüyü çalıştırıyoruz.
        x = random.randint(0, plane_width - car_width)      #Rastgele koordinatlar oluşturarak arabaların spawn olacağı x koordinatları belirlenir
        y = random.randint(0, plane_height - car_height)    #Rastgele koordinatlar oluşturarak arabaların spawn olacağı y koordinatları belirlenir.

        area = copied_plane[y : y + car_height, x : x + car_width] #Arabanın spawn olacağı bölge.

        for c in range(0, 3):
            area[:, :, c] = (1.0 - car_mask) * area[:, :, c] + car_mask * car_bgr[:, :, c]

        copied_plane[y : y + car_height, x : x + car_width] = area

cv2.namedWindow('Simulation', cv2.WINDOW_NORMAL) #Plane with Car başlıklı bir pencere oluşturulur.
cv2.resizeWindow('Plane with Car', 1400, 800)

cv2.imshow('Plane with Car', copied_plane)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite('planeWithCar.png', copied_plane)