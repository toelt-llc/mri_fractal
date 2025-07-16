#!/bin/bash

# Convert .mgz segmentation files to .nii.gz format using mri_convert
# This script assumes that mri_convert is available in the PATH

base_dir="/home/data/mri_datasets/bobs/segmentations/samseg_BOB/t1"

for x in "$base_dir"/*_ses-*_space-*; do
    if [ -d "$x" ]; then
        mgz_file="$x/seg.mgz"
        nii_file="$x/seg.nii.gz"

        if [ -f "$mgz_file" ]; then
            mri_convert "$mgz_file" "$nii_file"
        else
            echo "No seg.mgz found in $x"
        fi
    fi
done
