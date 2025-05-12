# Data Pipeline Documentation

This repository contains multiple Jupyter notebooks outlining the data processing pipeline for MRI scans, focusing on different anatomical MRI datasets.  
The pipeline is designed to allow evaluation of fractal dimension calculation(s).  
Processing steps include registration, (skull stripping), resizing, segmentation.  

## Notebooks Overview

1. **[1-pipeline.ipynb](./1-pipeline.ipynb)**
   - This notebook displays the possible preprocessing steps and an introduction to the tools used, including registration, skull stripping, and segmentation.  
   - **Key Steps**:
     - Load MRI scans and participant information.
     - **Registration**: Align MRI scans to a template using ANTs.  
     - **Skull Stripping**: Remove non-brain tissue using SynthStrip. (optional step).  
     - **Segmentation**: Segment the brain into different regions using SynthSeg.
     - **Fractal Dimension Calculation**: Calculate the fractal dimension of the brain regions.

2. **[2-fractal.ipynb](./2-fractal.ipynb)**
   - Fractal dimension computation after segmentation.
   - **Key Steps**:
     - **Label Mapping**: Map segmentation labels to anatomical regions using FreeSurfer's LookUpTable.
     - **Fractal Dimension Calculation**: Calculate the fractal dimension for the whole brain and specific regions.
     - **Visualization**: First visualization of the fractal dimension results.

3. **[3a-pipeline_BOB.ipynb](./3a-pipeline_BOB.ipynb)**
   - Processes the BOB dataset, including segmentation and fractal dimension calculation, with analysis.
   - **Key Steps**:
     - Using existing segmentations provided with the dataset.
     - **Fractal Dimension Calculation**: Calculate the fractal dimension for the whole brain and specific regions.
     - **Exploratory Data Analysis (EDA)**: Analyze the fractal dimension results, including comparisons between left and right hemispheres and correlations with age.

4. **[3b-pipeline_BOB_freesurfer-seg.ipynb](./3b-pipeline_BOB_freesurfer-seg.ipynb)**
   - Processes the BOB dataset using Freesurfer(SynthSeg) for segmentation and compares the fractal dimension results with the original segmentation method.
   - **Key Steps**:
     - **Segmentation**: Segment the brain using Freesurfer's SynthSeg tool.
     - **Fractal Dimension Calculation**: Calculate the fractal dimension for the whole brain and specific regions.
     - **Comparison**: Compare the fractal dimension results between the segmentation method and the source segmentation.

5. **[3c-pipeline_dhcp.ipynb](./3c-pipeline_dhcp.ipynb)**
   - Processes the DHCP dataset, including segmentation and fractal dimension calculation.
   - **Key Steps**:
     - **Segmentation**: Segment the brain using SynthSeg.
     - **Fractal Dimension Calculation**: Calculate the fractal dimension for the whole brain and specific regions.
     - **Exploratory Data Analysis (EDA)**: Check the fractal dimension results.

6. **[4-fractal_comparison.ipynb](./4-fractal_comparison.ipynb)**
   - Compares the fractal dimension results between different preprocessing steps and segmentation methods.
   - **Key Steps**:
     - **Comparison**: Compare the fractal dimension results between different preprocessing steps and segmentation methods.

## Detailed features

#### Data Loading
- Load MRI scans and participant information from specified file paths.
- Visualize the MRI scans using utility functions.

#### Registration
- Align MRI scans to a template using ANTs.
- Perform registration with the SyN algorithm.

#### Segmentation
- Segment the brain into different regions using SynthSeg.
- Save the segmented images, with volumes and quality control metrics.

#### Label Mapping
- Map segmentation labels to anatomical regions using FreeSurfer's LookUpTable.
- Identify the regions present in the segmented volume.

#### Fractal Dimension Calculation
- Calculate the fractal dimension of the different brain regions using box-counting method.
- Visualize the fractal dimension results.

#### Exploratory Data Analysis (EDA)
- Analyze the fractal dimension results, including comparisons between left and right hemispheres and correlations with age.
- Visualize the fractal dimension results using box plots and scatter plots.

#### Comparison
- Compare the fractal dimension results between the two segmentation methods.
- Visualize the differences in fractal dimension results.

##### Optional/unused : Skull Stripping
- Remove non-brain tissue using SynthStrip.


## Dependencies

For setup see [installation](../readme.md) and [requirements](../requirements.txt)

- **ANTs**: Advanced Normalization Tools for image registration.
- **Nibabel**: Python library for reading and writing NIfTI files.
- **Pandas**: Data manipulation and analysis library.
- **Matplotlib**: Plotting library for visualization.
- **Porespy**: Library for pore-scale modeling and analysis.
- **Utils**: Custom utility functions for data processing and visualization.
