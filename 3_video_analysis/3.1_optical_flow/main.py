import sys
import remove_background
import optical_flow
import video_io

if len(sys.argv) > 1:
    src_path = sys.argv[1]
    dest_path = "background_removed.mp4"
else:
    sys.exit("Please add command line arguments for source and destination video paths.")


frame_interval = 0.02
frames = video_io.extract_greyscale_frames(src_path, frame_interval, 0.2, 2)
video_io.write_video(dest_path, frames, 1)
optical_flow.lucas_kanade(frames[0], frames[1])