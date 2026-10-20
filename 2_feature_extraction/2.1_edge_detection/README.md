# Sprint 2.1

## Deliverables
* Notes on the Edge Detection subsection of First Principles of Computer Vision (`notes_2.1.pdf`)
* Edge Detection Suite code:
    - Edge Detector using Gradient: a program to identify edges in an image via the Gradient Operator (`differential_ed.py`)
    - Edge Detector using Laplacian: a program to identify edges in an image via the Laplace Operator (`differential_ed.py`)
    - Canny Edge Detector: an implementation of Canny Edge Detection, which is widely used today (`canny_ed.py`)

* Proof of work
    - `gradient_edge_detection.png`: the output of a gradient edge detection algorithm (right) applied to an image of a Rubiks Cube (left)
    - `laplacian_edge_detection.png`: the output of a laplacian edge detection algorithm (right) applied to an image of a Rubiks Cube (left)
    - `canny_edge_detection.png`: the output of the Canny Edge Detection algorithm with various values of $\sigma$ applied to an image of a motorcycle. As is evident by the images, Canny Edge Detection is particularly useful in that changing the value of $\sigma$ allows you to specify the level of detail of the calculated edges.