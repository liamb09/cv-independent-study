# Sprint 1.2

## Deliverables
* Notes on the Image Processing II subsection of First Principles of Computer Vision (`notes_1.3.pdf`)
* Fourier Transform Image Processor code (`fourier_processing.py`)
    - Low Pass Filter: a program to smooth images by removing high-frequency noise via Fourier transform
    - High Pass Filter: a program to reveal edges by removing low-frequency noise via Fourier transform
    - Image Deconvolutor: a program to revert camera shake blur on images based on the known point spread function

* Proof of work
    - `sinusoidal_grating_fft.png`: a sinusoidal grating (left) with 2D Fourier transform applied (right). The two outermost white dots represent the frequency of the sinusoid (both positive and negative), and the center dot represents the zero frequency.
    - `rubiks_cube_lpf.png`: a Rubiks Cube (left) with a Low Pass Filter applied (right)
    - `rubiks_cube_hpf.png`: a Rubiks Cube (left) with a High Pass Filter applied (right)
    - `camera_shake_deconvolution.png`: an image blurred by camera shake (left) that has been sharpened via deconvolution (right)
        - This technique cannot restore the blurred image to full quality due to loss of information