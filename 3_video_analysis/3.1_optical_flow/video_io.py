import cv2
import numpy as np

def extract_greyscale_frames (video_path, frame_interval, start_time=0, num_frames=-1):
    video = cv2.VideoCapture(video_path)
    frames = []
    fps = round(video.get(cv2.CAP_PROP_FPS))

    i = 0
    first_frame_idx = round(fps * start_time)
    frame_modulus = max(round(fps*frame_interval), 1)
    while video.isOpened():
        ret, frame = video.read()
        if not ret or len(frames) == num_frames:
            break
        if i >= first_frame_idx and (i-first_frame_idx) % frame_modulus == 0:
            # convert from BGR to RGB
            greyscale_grid = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frames.append(greyscale_grid.astype(np.float32))

        i += 1

    video.release()

    # Convert list of frames into a single 4D NumPy array: (num_frames, height, width, 3)
    return np.array(frames)

def write_video (path, greyscale_frames, fps):
    height, width = greyscale_frames[0].shape
    frame_size = (width, height)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(path, fourcc, fps, frame_size, isColor=False)

    for frame in greyscale_frames:
        out.write(frame)

    out.release()