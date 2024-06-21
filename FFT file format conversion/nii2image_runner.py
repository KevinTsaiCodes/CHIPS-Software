import nibabel as nib
import matplotlib.pyplot as plt
import numpy as np
import cv2
import argparse
from colorama import Style, Fore


"""
Reference: Converting A NIfTI File To An Image Sequence Using Python
https://ianmcatee.com/converting-a-nifti-file-to-an-image-sequence-using-python/
"""

def parse_args():
    parser = argparse.ArgumentParser(
        description="A CLI tool for automatic NifTI single file to series of image format conversion.",
        epilog="Author: Wei-Chun Kevin Tsai"
    )
    parser.add_argument(
        "-i",
        "--input_path",
        type=str,
        default="./assets/input_nifti_file/input_brain.nii.gz"
    )
    parser.add_argument(
        "-o",
        "--output_directory",
        type=str,
        default="./assets/output_nifti_file/"
    )
    parser.add_argument(
        "-f",
        "--factor",
        type=float,
        default=0.2,
        help="A parameter that controls the brightness adjustment of an image (default: 0.2)"
    )
    return parser.parse_args()


def adjust_brightness(image, factor:float):
    return np.clip(image * factor, 0, 255).astype(np.uint8)


def main(opt):
    scanFilePath = opt.input_path
    scan = nib.load(scanFilePath)
    scanArray = scan.get_fdata()
    scanArrayShape = scanArray.shape
    # get the header of the nifti file
    scanHeader = scan.header
    print(f"{Fore.RED}The scan header is as follows: \n{scanHeader}{Style.RESET_ALL}")
    
    pixDim = scanHeader['pixdim'][1:4]
    aspectRatios = [pixDim[1] / pixDim[2], pixDim[0] / pixDim[2], pixDim[0] / pixDim[1]]
    newScanDims = np.multiply(scanArrayShape, pixDim)
    newScanDims = (round(newScanDims[0]), round(newScanDims[1]), round(newScanDims[2]))
    
    factor = opt.factor

    outputPath = opt.output_directory
    
    # Iterate and save scan slices along 2nd dimension (Axial View)
    for i in range(scanArrayShape[2]):
        outputArray = cv2.resize(scanArray[:, :, i], (newScanDims[1], newScanDims[0]))
        outputArray = cv2.rotate(outputArray, cv2.ROTATE_90_CLOCKWISE)
        outputArray_dark = adjust_brightness(outputArray, factor=0.4)  # Adjust factor as needed
        cv2.imwrite(outputPath + str(i) + '.png', outputArray_dark)

    print(f"{Fore.GREEN}All slices saved to {outputPath}{Style.RESET_ALL}")


if __name__ == "__main__":
    print(f"{Fore.GREEN}Starting Process...{Style.RESET_ALL}")
    opt = parse_args()
    main(opt)