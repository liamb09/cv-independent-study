import cv2
import numpy as np
import video_processing

def remove_bg (src_path, dest_path):
    frame_interval = 0.05
    frames = video_processing.extract_greyscale_frames(src_path, frame_interval)

    first_frame = cv2.GaussianBlur(frames[0].astype(np.int16), (5, 5), 0)

    for i in range(1, len(frames)):
        cur_frame = cv2.GaussianBlur(frames[i].astype(np.int16), (5, 5), 0)
        for row in range(len(first_frame)):
            for col in range(len(first_frame[0])):
                if abs(first_frame[row][col] - cur_frame[row][col]) < 20:
                    frames[i][row][col] = 0
                    
    frames[0] = np.zeros(frames[0].shape)

    video_processing.write_video(dest_path, frames, 1/frame_interval)