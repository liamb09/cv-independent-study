# Sprint 1.2

## Deliverables
* Notes on the Image Processing II subsection of First Principles of Computer Vision (`notes_1.3.pdf`)
* Fourier Transform Image Processor code (`fourier_processing.py`)
    - Low Pass Filter: a program to smooth images by removing high-frequency noise via fourier transform
    - High Pass Filter: a program to reveal edges by removing low-frequency noise via fourier tranform
    - Image Deconvolutor: a program to revert camera shake blur on images based on the known point spread function

* Proof of work
    - Image with Gaussian Blur (a linear filter) applied (`gaussian_blur.png`, original on left, filtered on right)
    - Image with Bilateral Filter (a nonlinear filter) applied (`bilateral_filter.png`, original on left, filtered on right)