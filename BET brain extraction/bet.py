import matplotlib.pyplot as plt
import os
import ants
import SimpleITK as sitk
from colorama import Fore, Style
import time
from tqdm import tqdm
import argparse
import numpy as np
from antspynet.utilities import brain_extraction  # import brain_extraction_toolbox
import sys



"""
BET: A re-implmentation of Brain Extraction Tool
Reference:
Fast Robust Automated brain Extraction by Stephen M Smith, 2002, Human Brain Mapping
"""


def parse_args():
    parser = argparse.ArgumentParser(
        description="A CLI tool for automatic MRI T2-FLAIR brain extraction.",
        epilog="Author: Wei-Chun Kevin Tsai"
    )
    parser.add_argument(
        "-i",
        "--input_path",
        type=str,
        default="./assets/raw_data/T2-FLAIR.nii.gz",
        help="path/to/the/input/nifti/file (default: ./assets/raw_data/T2-FLAIR.nii.gz)"
    )
    parser.add_argument(
        "-low_thr",
        "--low_thresh",
        type=float,
        default=0.5,
        help="An inclusive lower threshold for voxels to be included in the mask. If not given, defaults to image mean. (default: 0.5)"
    )
    parser.add_argument(
        "-high-thr",
        "--high_thresh",
        type=float,
        help="An inclusive upper threshold for voxels to be included in the mask. If not given, defaults to image max."
    )

    parser.add_argument(
        "-cleanup",
        "--cleanup",
        type=int,
        help="If > 0, morphological operations will be applied to clean up the mask by eroding away small or weakly-connected areas, and closing holes (default: 2). If cleanup is > 0, the following steps are applied. (1) Erosion with radius 2 voxels. (2) Retain largest component. (3) Dilation with radius 1 voxel. (4) Morphological closing.",
        default=2
    )    
    return parser.parse_args()


def add_suffix_to_filename(filename: str, suffix:str) -> str:
    """
        Takes a NIfTI filename and appends a suffix.

        Args:
            filename : NIfTI filename
            suffix : suffix to append

    Returns:
        str : filename after append the suffix
    """
    try:
        if filename.endswith('.nii'):
            result = filename.replace('.nii', f'_{suffix}.nii')
            return result
        elif filename.endswith('.nii.gz'):
            result = filename.replace('.nii.gz', f'_{suffix}.nii.gz')
            return result
        else:
            raise RuntimeError('filename with unknown extension')
    
    except AttributeError as e:
        pass

    finally:
        print(f"{Fore.GREEN}Processed Finished!")

def run(input_path: str, low_thresh: float, high_thresh: float, cleanup: int):
    raw_data_path = ants.image_read(input_path, reorient="IAL")
    prob_brain_mask = brain_extraction(raw_data_path, modality="flair", verbose=True)  # generate the probabilty brain mask
    final_brain_mask = ants.get_mask(prob_brain_mask, low_thresh=low_thresh, high_thresh=high_thresh, cleanup=cleanup)
    output_folder = os.path.join("assets", "bet_result")
    os.makedirs(output_folder, exist_ok=True)  # create the output folder for the NifTI after BET procedure.
    output_brain_data = add_suffix_to_filename(input_path.split("/")[-1], suffix="brain_mask")
    output_brain_path = os.path.join(output_folder, output_brain_data)
    final_brain_mask.to_file(output_brain_path)


def main(opt):
    if not opt.input_path.split("/")[-1].endswith(".nii.gz"):
        print(f"{Fore.RED}The extension of the input file must ends with "".nii.gz""")
        sys.exit(-1)  # error code -1 means error extension of the input file
    else:
        input_path = opt.input_path
    low_thresh = opt.low_thresh
    high_thresh = opt.high_thresh
    if opt.cleanup <= 0:
        print(f"{Fore.RED}The cleanup value must larger than 0.\ncleanup value (current): {opt.cleanup}.\nType -h or --help for more details on how to use the cleanup command.{Style.RESET_ALL}", end="")
        sys.exit(-2)  # error code -2 means error value
    else:
        cleanup = opt.cleanup
    run(input_path, low_thresh, high_thresh, cleanup)

if __name__ == '__main__':
    opt = parse_args()
    main(opt)