#Я добавил сюда эту функцию для быстрой подготовки видео
import os
import cv2
from os.path import isfile, join

#Указание директорий видео и директории вырезанных кадров

video_directory = "videos/"
output_directory = "frames/"

def extract_frames(video_dir, output_dir): 

    videos = [f for f in os.listdir(video_dir) if isfile(join(video_dir, f))]

    for video in videos:
        video_path = os.path.join(video_dir, video)
        vidcap = cv2.VideoCapture(video_path)
        success, image = vidcap.read()
        count = 0

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        while success:
            frame_path = os.path.join(output_dir, f"{video}_{count}.png")
            cv2.imwrite(frame_path, image)  # save frame as PNG
            success, image = vidcap.read()
            count += 1

        vidcap.release()


#Вызов функции
extract_frames(video_directory, output_directory)