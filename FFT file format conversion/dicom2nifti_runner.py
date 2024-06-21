import dicom2nifti
import argparse
import os


def parse_args():
    parser = argparse.ArgumentParser(
        description="A CLI tool for automatic DICOM series to NifTI single file format conversion.",
        epilog="Author: Wei-Chun Kevin Tsai"
    )
    parser.add_argument(
        "-i",
        "--input_directory",
        type=str,
        default="./assets/input_dicom_file/",
        help="path/to/the/input/dicom/file/directory (default: ./assets/input_dicom_file/)"
    )
    parser.add_argument(
        "-o",
        "--output_directory",
        type=str,
        default="./assets/output_nifti_file/",
        help="path/to/the/output/nifti/directory (default: ./assets/output_nifti_file/)"
    )
    parser.add_argument(
        "-f",
        "--nifti_filename",
        type=str,
        default="dicom2nifti.nii.gz",
        help="output/nifti/filename (default: dicom2nifti.nii.gz)"
    )
    return parser.parse_args()


def main(opt):
    nifti_file_path = os.path.join(opt.output_directory, opt.nifti_filename)
    dicom2nifti.dicom_series_to_nifti(opt.input_directory, nifti_file_path, reorient_nifti=True)


if __name__ == '__main__':
    opt = parse_args()
    main(opt)
