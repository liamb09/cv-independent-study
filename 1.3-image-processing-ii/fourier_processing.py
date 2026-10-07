from PIL import Image
import numpy as np
import sys
import math
import cmath
import scipy.fft as fft
import cv2

def intensity (pixel):
    return 0.299*pixel[0] + 0.587*pixel[1] + 0.114*pixel[2]

def to_freq_domain (pixel_grid, p, q):
    sum = 0
    for row in range(len(pixel_grid)):
        for col in range(len(pixel_grid[row])):
            sum += intensity(pixel_grid[p, q]) * cmath.exp(-2*math.pi*p*row/len(pixel_grid)*1j) * cmath.exp(-2*math.pi*q*col/len(pixel_grid[0])*1j)
    return sum

def hann (pixel_grid):
    h, w, _ = pixel_grid.shape
    for row in range(len(pixel_grid)):
        for col in range(len(pixel_grid[row])):
            pixel_grid[row, col] = pixel_grid[row, col] * (math.sin(math.pi*row/h)**2) * (math.sin(math.pi*col/w)**2)
    return pixel_grid

def gaussian_kernel_in_freq_domain (std_dev, shape, kernel_size=-1):
    if kernel_size == -1:
        kernel_size = math.ceil(2 * math.pi * std_dev)
    variance = std_dev ** 2
    
    h, w, _ = shape
    spatial_kernel = np.zeros((h, w))
    center = (h//2, w//2)

    for row in range(-kernel_size//2, kernel_size//2 - 1):
        for col in range(-kernel_size//2, kernel_size//2 - 1):
            spatial_kernel[center[0]+row, center[1]+col] = 1/(2*math.pi*variance) * math.exp(-0.5 * (row**2 + col**2) / variance)

    freq_kernel = fft.fft2(spatial_kernel)

    ## display gaussian kernel in spatial domain
    # display_new_grid = np.log(1 + spatial_kernel)
    # display_new_grid = (display_new_grid - np.min(display_new_grid)) / (np.max(display_new_grid) - np.min(display_new_grid))*255
    # newimg = Image.fromarray(display_new_grid.astype(np.uint8))
    # newimg.save("gaussian_spatial.jpg")

    ## display gaussian kernel in frequency domain
    # display_new_grid = np.log(1 + np.abs(fft.fftshift(freq_kernel)))
    # display_new_grid = (display_new_grid - np.min(display_new_grid)) / (np.max(display_new_grid) - np.min(display_new_grid))*255
    # newimg = Image.fromarray(display_new_grid.astype(np.uint8))
    # newimg.save("gaussian_freq.jpg")

    return fft.fftshift(freq_kernel)

def low_pass_filter (pixel_grid, std_dev):
    new_grid = np.zeros((pixel_grid.shape[0], pixel_grid.shape[1]))
    for row in range(len(pixel_grid)):
        for col in range(len(pixel_grid[row])):
            new_grid[row, col] = intensity(pixel_grid[row, col])

    new_grid = fft.fft2(new_grid)
    new_grid = fft.fftshift(new_grid)

    freq_gaussian = gaussian_kernel_in_freq_domain(std_dev, pixel_grid.shape)
    
    # component-wise multiplication in frequency domain is equivalent to convolution in spatial domain
    low_pass_w_gaussian = np.multiply(new_grid, freq_gaussian)

    display_new_grid = np.abs(low_pass_w_gaussian)
    display_new_grid = np.log(1 + display_new_grid)
    display_new_grid = (display_new_grid - np.min(display_new_grid)) / (np.max(display_new_grid) - np.min(display_new_grid))*255

    inv_new_grid = fft.ifftshift(low_pass_w_gaussian)
    inv_new_grid = fft.ifft2(inv_new_grid)
    inv_new_grid = fft.ifftshift(inv_new_grid)
    display_inv_new_grid = np.real(inv_new_grid)

    return display_new_grid, display_inv_new_grid

def high_pass_filter (pixel_grid, std_dev, radius=10):
    new_grid = np.zeros((pixel_grid.shape[0], pixel_grid.shape[1]))
    for row in range(len(pixel_grid)):
        for col in range(len(pixel_grid[row])):
            new_grid[row, col] = intensity(pixel_grid[row, col])

    new_grid = fft.fft2(new_grid)
    new_grid = fft.fftshift(new_grid)

    h, w = new_grid.shape
    for row in range(len(new_grid)):
        for col in range(len(new_grid[row])):
            if math.sqrt((h//2-row)**2 + (w//2-col)**2) <= radius:
                new_grid[row, col] = 0

    display_new_grid = np.abs(new_grid)
    display_new_grid = np.log(1 + display_new_grid)
    display_new_grid = (display_new_grid - np.min(display_new_grid)) / (np.max(display_new_grid) - np.min(display_new_grid))*255

    inv_new_grid = fft.ifftshift(new_grid)
    inv_new_grid = fft.ifft2(inv_new_grid)
    display_inv_new_grid = np.abs(inv_new_grid)

    return display_new_grid, display_inv_new_grid

def apply_diagonal_blur (pixel_grid, kernel_size=19):
    new_grid = np.zeros((pixel_grid.shape[0], pixel_grid.shape[1]))
    for row in range(len(pixel_grid)):
        for col in range(len(pixel_grid[row])):
            new_grid[row, col] = intensity(pixel_grid[row, col])
    cv2_image = np.array(new_grid, dtype=np.uint8)
    kernel = np.zeros((kernel_size, kernel_size))
    for i in range(kernel_size):
        kernel[kernel_size-i-1,i] = 1 / kernel_size

    output = cv2.filter2D(cv2_image, -1, kernel)

    return output

def remove_image_blur (pixel_grid, point_spread_func=None): # psf describes blur
    if not point_spread_func:
        point_spread_func = np.zeros((pixel_grid.shape[0], pixel_grid.shape[1]))
        kernel_size = 19
        for i in range(kernel_size):
            point_spread_func[len(pixel_grid)//2 + kernel_size//2-i, len(pixel_grid[0])//2 - kernel_size//2-1+i] = 1 / kernel_size

    new_grid = np.zeros((pixel_grid.shape[0], pixel_grid.shape[1]))
    for row in range(len(pixel_grid)):
        for col in range(len(pixel_grid[row])):
            new_grid[row, col] = intensity(pixel_grid[row, col])
    freq_og_img = fft.fftshift(fft.fft2(new_grid))

    freq_psf = fft.fft2(point_spread_func)
    freq_psf_shifted = fft.fftshift(freq_psf)
    display_new_grid = np.log(1 + np.abs(freq_psf_shifted))
    display_new_grid = (display_new_grid - np.min(display_new_grid)) / (np.max(display_new_grid) - np.min(display_new_grid))*255
    newimg = Image.fromarray(display_new_grid.astype(np.uint8))
    newimg.save("gaussian_freq2.jpg")

    # noise to signal ratio, which describes the ratio of noise power to signal power (unknowable, so we set to constant)
    nsr = 0.03
    recovered_grid = np.zeros((pixel_grid.shape[0], pixel_grid.shape[1])).astype(np.complex128)
    for row in range(len(pixel_grid)):
        for col in range(len(pixel_grid[row])):
            # weiner deconvolution
            recovered_grid[row, col] = freq_og_img[row, col] * freq_psf_shifted[row, col].conjugate() / (nsr + abs(freq_psf_shifted[row, col])**2)
    
    display_new_grid = np.log(1 + np.abs(recovered_grid))
    display_new_grid = (display_new_grid - np.min(display_new_grid)) / (np.max(display_new_grid) - np.min(display_new_grid))*255
    newimg = Image.fromarray(display_new_grid.astype(np.uint8))
    newimg.save("gaussian_freq2.jpg")

    recovered_grid = fft.ifftshift(fft.ifft2(fft.ifftshift(recovered_grid)))

    return np.abs(recovered_grid)


if len(sys.argv) > 3:
    src_path = sys.argv[1]
    dest_path = sys.argv[2]
    inv_dest_path = sys.argv[3]
elif len(sys.argv) > 1:
    src_path = sys.argv[1]
    dest_path = "filtered.jpg"
    inv_dest_path = "inv_filtered.jpg"
else:
    sys.exit("Please add command line arguments for source, fft destination, and inv_ftt destination image paths.")

img = Image.open(src_path).convert("RGB")
pixel_grid = np.array(img)

## Low Pass Filter
# display_new_grid, display_inv_new_grid = low_pass_filter(pixel_grid, 2)
# newimg = Image.fromarray(display_new_grid.astype(np.uint8))
# newimg.save(dest_path)
# newimg = Image.fromarray(display_inv_new_grid.astype(np.uint8))
# newimg.save(inv_dest_path)

## High Pass Filter
display_new_grid, display_inv_new_grid = high_pass_filter(pixel_grid, 2)
newimg = Image.fromarray(display_new_grid.astype(np.uint8))
newimg.save(dest_path)
newimg = Image.fromarray(display_inv_new_grid.astype(np.uint8))
newimg.save(inv_dest_path)

## Add Camera Shake (for testing)
# cv2.imwrite(dest_path, apply_diagonal_blur(pixel_grid))

## Remove Camera Shake
# newimg = Image.fromarray(remove_image_blur(pixel_grid).astype(np.uint8))
# newimg.save(dest_path)

