import os
import sys
from colorama import Fore, Style
from tqdm import tqdm
import numpy as np
import time
import SimpleITK as sitk


class Image2NifTITool:
    def __init__(self, input_directory: str, output_directory: str, nifti_filename: str):
        self.__input_directory = input_directory
        self.__output_directory = output_directory
        self.__nifti_filename = nifti_filename
        self.__check_directory_exist()
        self.__image2nifti()

    def __check_file_format(self):
        # Ensure the file format is correct
        if not self.__nifti_filename.endswith(".nii") or not self.__nifti_filename.endswith(".nii.gz"):
            print(Fore.RED + f"\nError: {self.__nifti_filename} file format is incorrect.", end="")
            print(Style.RESET_ALL)
            sys.exit(-2)

    def __check_directory_exist(self):
        # Ensure the directory exists
        if not os.path.exists(self.__input_directory):
            os.makedirs(self.__input_directory, exist_ok=True)

        if not os.path.exists(self.__output_directory):
            os.makedirs(self.__output_directory, exist_ok=True)

        if not os.listdir(self.__input_directory):
            print(Fore.RED + f"\nError: No files found in the {self.__input_directory} directory.", end="")
            print(Style.RESET_ALL)
            sys.exit(-1)

    def __image2nifti(self):
        # get lists of image files
        image_files = []
        for files in tqdm(os.listdir(self.__input_directory), ascii=True, desc="obtain-image-files"):
            if files.endswith(".jpeg") or files.endswith(".jpg") or files.endswith(".png"):
                image_files.append(os.path.join(self.__input_directory, files))
            else:
                print(Fore.RED + f"\nError: {files} is not an image file.", end="")
                print(Style.RESET_ALL)
                continue
            time.sleep(0.1)

        # sort the list of image files
        image_files = sorted(image_files)

        # create an empty list to store the images
        image_list = []

        # Read each ndarray of images and append them to the list

        for files in tqdm(image_files, ascii=True, desc="Image-to-NifTI"):
            image = sitk.ReadImage(files)
            image_list.append(image)

            # Create a 3D image volume from the list of images
            image_volume = sitk.JoinSeries(image_list)

            # Write the 3D image volume to a single NIFTI file
            sitk.WriteImage(image_volume, os.path.join(self.__output_directory, self.__nifti_filename))

            time.sleep(0.1)

        print(Fore.GREEN, f"\nSuccessfully converted image series to a NifTI format file, and saved it at directory {self.__output_directory}, with the name of {self.__nifti_filename}.\n")
        print(Fore.GREEN, f"Processed Finished!")
