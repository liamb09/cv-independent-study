# Sprint 3.1

## Deliverables
* Notes on the Camera Calibration and Optical Flow subsections of First Principles of Computer Vision (`notes_3.1.pdf`)
* Boundary Detection Suite code:
    - Video Inputter: a tool to load a video into a set of pixel grids at a specified frame rate and time (`video_io.py`)
    - Video Frame Compressor: a tool to average pixel values to reduce the resolution of video frames, a crucial step in the Lucas-Kanade method for calculating Optical Flow (`optical_flow.py`)
    - Video Outputter: a tool to save a set of pixel grids to a video at a specified frame rate (`video_io.py`)

* Proof of work
    - `compressed_frame1.bmp` and `compressed_frame2.bmp`: the output of the video frame compression so that two frames' optical flow is reduced to the single-pixel level