import sys
import remove_background
import optical_flow
import video_processing

if len(sys.argv) > 1:
    src_path = sys.argv[1]
    dest_path = "background_removed.mp4"
else:
    sys.exit("Please add command line arguments for source and destination video paths.")


frame_interval = 0.02
frames = video_processing.extract_greyscale_frames(src_path, frame_interval, 0.2, 2)
video_processing.write_video(dest_path, frames, 1)