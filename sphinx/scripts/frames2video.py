import cv2
import numpy as np
import os

from os.path import isfile, join

def convert_frames_to_video(input_file, output_file, fps):
    frame_array = []
    files = [f for f in os.listdir(input_file) if isfile(join(input_file, f))]
    files.sort(key = lambda x: int(x[5:-4]))

    for i in range(len(files)):
        filename=input_file + files[i]
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        frame_array.append(img)

    out = cv2.VideoWriter(
              output_file,cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
    for i in range(len(frame_array)):
        out.write(frame_array[i])
    out.release()

def main():
    input_file= "path/to/frames"
    output_file = "path/to/video"
    fps = 30
    convert_frames_to_video(input_file, output_file, fps)

if __name__=="__main__":
    main()
