import sys
import remove_background

if len(sys.argv) > 1:
    src_path = sys.argv[1]
    dest_path = "background_removed.mp4"
else:
    sys.exit("Please add command line arguments for source and destination video paths.")

remove_background.remove_bg(src_path, dest_path)