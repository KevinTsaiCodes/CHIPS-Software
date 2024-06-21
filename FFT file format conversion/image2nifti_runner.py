from helpers import *
import argparse




def parse_args():
    parser = argparse.ArgumentParser(
        description="A CLI tool for automatic Image series to NifTI single file format conversion.",
        epilog="Author: Wei-Chun Kevin Tsai"
    )
    parser.add_argument(
        "-i",
        "--input_directory",
        type=str,
        default="./assets/input_image_file/",
        help="path/to/the/input/image/file/directory (default: ./assets/input_image_file/)"
    )
    parser.add_argument(
        "-o",
        "--output_directory",
        type=str,
        default="./assets/output_nifti_file/",
        help="path/to/the/output/nifti/file/directory (default: ./assets/input_nifti_file/)"
    )
    parser.add_argument(
        "-f",
        "--nifti_filename",
        type=str,
        default="image2nifti.nii.gz",
        help="output/nifti/filename (default: image2nifti.nii.gz)"
    )
    return parser.parse_args()

def main(opt):
    Image2NifTITool(opt.input_directory, opt.output_directory, opt.nifti_filename)

if __name__ == '__main__':
    opt = parse_args()
    main(opt)