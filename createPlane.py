import cv2
import numpy as np

img = cv2.imread('aaaaa.png') #resmi okuduk.

if img is None: 
    print("Image is not found.")  #resim var mı yok mu kontrolü.
else:
    horizontal_repeat_number = 3  #yatay tekrar sayısı.
    vertical_repeat_number = 3  #dikey tekrar sayısı. 

    plane = np.tile(img, (horizontal_repeat_number, vertical_repeat_number, 1)) # 3x3 görüntü oluşturuldu.

    plane = cv2.resize(plane, (2800, 1600))

    cv2.imshow('Created Plane', plane) #Görüntüyü ekranda göster.

    cv2.waitKey(0) #0 tuşuna basılana kadar görüntü açık kalır. 

    cv2.destroyAllWindows() #0 tuşuna basıldığında tüm pencereleri kapatır.

    cv2.imwrite('createdPlane.png',plane) #Oluşturduğumuz düzlemi kaydeder.
     


