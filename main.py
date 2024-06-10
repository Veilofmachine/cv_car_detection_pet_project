#Необходимые импорты 
import os
import re
import cv2
import numpy as np
from os.path import isfile, join
import matplotlib.pyplot as plt
import imutils
#указание рабочей директории откуда берутся кадры
col_frames = os.listdir('frames/')

#сортировка файлов
col_frames.sort(key=lambda f: int(re.sub('\D', '', f)))

#создание пустого листа для хранения кадров
col_images=[]

for i in col_frames:
    #Этот код просматривает кадры и добавляет в ранее созданный лист
    img = cv2.imread('frames/'+i)
    col_images.append(img)
#Взятое рандомное число
i = 8

for frame in [i, i+1]:
    plt.imshow(cv2.cvtColor(col_images[frame], cv2.COLOR_BGR2RGB))
    plt.title("frame: "+str(frame))
    plt.show()

# конвертация кадров в чб
grayA = cv2.cvtColor(col_images[i], cv2.COLOR_BGR2GRAY)
grayB = cv2.cvtColor(col_images[i+1], cv2.COLOR_BGR2GRAY)

#различие между кадрами
plt.imshow(cv2.absdiff(grayB, grayA), cmap = 'gray')
plt.show()

diff_image = cv2.absdiff(grayB, grayA)

# создание стандартного трешхолда
ret, thresh = cv2.threshold(diff_image, 30, 255, cv2.THRESH_BINARY)

# картинка после трешхолда
plt.imshow(thresh, cmap = 'gray')
plt.show()

#применение дилатации
kernel = np.ones((3,3),np.uint8)
dilated = cv2.dilate(thresh,kernel,iterations = 1)
plt.imshow(dilated, cmap = 'gray')
plt.show()


# создание зоны детекции
plt.imshow(dilated)
cv2.line(dilated, (0, 800),(2000,800),(800, 0, 0))
plt.show()

#поиск контуров
contours, hierarchy = cv2.findContours(thresh.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
valid_cntrs = []

for i,cntr in enumerate(contours):
    x,y,w,h = cv2.boundingRect(cntr)
    if (x <= 2000) & (y >= 400) & (cv2.contourArea(cntr) >= 100):
        valid_cntrs.append(cntr)      
len(valid_cntrs)

dmy = col_images[13].copy()

cv2.drawContours(dmy, valid_cntrs, -1, (127,200,0), 2)
cv2.line(dmy, (0, 400),(2000,400),(400, 2000, 2000))
plt.imshow(dmy)
plt.show()
kernel = np.ones((4,4),np.uint8)

#Стиль шрифта
font = cv2.FONT_HERSHEY_SIMPLEX

#Директория для сохранения результата в фреймах
pathIn = "frames_save/"

for i in range(len(col_images)-1):
    
    #нахождение разницы кадров, трешхолдинг дилатация и контуры
    grayA = cv2.cvtColor(col_images[i], cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(col_images[i+1], cv2.COLOR_BGR2GRAY)
    diff_image = cv2.absdiff(grayB, grayA)
    ret, thresh = cv2.threshold(diff_image, 30, 255, cv2.THRESH_BINARY)

    dilated = cv2.dilate(thresh,kernel,iterations = 1)
    
    contours, hierarchy = cv2.findContours(dilated.copy(), cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    
    #появление контуров в зоне детекеции
    valid_cntrs = []
    for cntr in contours:
        x,y,w,h = cv2.boundingRect(cntr)
        if (x <= 1200) & (y >= 320) & (cv2.contourArea(cntr) >= 200):
            if (y >= 360) & (cv2.contourArea(cntr) < 160):
                break
            valid_cntrs.append(cntr)
            
    #добавление фреймов контуров к фреймам без
    new_frames = col_images[i].copy()
    cv2.drawContours(new_frames, valid_cntrs, -1, (827,800,0), 2)
    
    cv2.putText(new_frames, "vehicles detected: " + str(len(valid_cntrs)), (55, 15), font, 0.6, (0, 180, 0), 2)
    cv2.line(new_frames, (0, 360),(2000,360),(400, 2000, 2000))
    cv2.imwrite(pathIn+str(i)+'.png',new_frames)  

#название видео из сложенных кадров
pathOut = 'example_car_detection.mp4'

# стандартный фпс итогового видео
fps = 14.0

frame_array = []
files = [f for f in os.listdir(pathIn) if isfile(join(pathIn, f))]

files.sort(key=lambda f: int(re.sub('\D', '', f)))

for i in range(len(files)):
    filename=pathIn + files[i]
    
    #чтение кадров и добавление в массив картинок
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width,height)
    frame_array.append(img)

out = cv2.VideoWriter(pathOut,cv2.VideoWriter_fourcc(*'DIVX'), fps, size)

for i in range(len(frame_array)):
    #создание массива картинок
    out.write(frame_array[i])

out.release()