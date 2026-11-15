import cv2
import numpy as np

def to_greyscale_frames (video_path, frame_interval):
    # frame interval is time in seconds between fetched frames

    video = cv2.VideoCapture(video_path)
    frames = []
    fps = round(video.get(cv2.CAP_PROP_FPS))

    i = 0
    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break
        if i % round(fps * frame_interval) == 0:
            # convert from BGR to RGB
            greyscale_grid = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frames.append(greyscale_grid)

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

def remove_bg (src_path, dest_path):
    frame_interval = 0.05
    frames = to_greyscale_frames(src_path, frame_interval)

    first_frame = cv2.GaussianBlur(frames[0].astype(np.int16), (5, 5), 0)

    for i in range(1, len(frames)):
        cur_frame = cv2.GaussianBlur(frames[i].astype(np.int16), (5, 5), 0)
        for row in range(len(first_frame)):
            for col in range(len(first_frame[0])):
                if abs(first_frame[row][col] - cur_frame[row][col]) < 20:
                    frames[i][row][col] = 0
                    
    frames[0] = np.zeros(frames[0].shape)

    write_video(dest_path, frames, 1/frame_interval)