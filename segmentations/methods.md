# List

##
 - Synthseg
[link](https://github.com/BBillot/SynthSeg)
Docker or local
```bash
sudo /home/arnaud/projects/mri_fractal/data_pipeline/synthseg.py --i dhcp_t1.nii.gz --o synsthseg/dhcp_t1_seg.nii.gz
```
whole brain 

## 
 - SamSeg
[link]{https://surfer.nmr.mgh.harvard.edu/fswiki/Samseg}
```bash
run_samseg --input bobs_t1.nii.gz --output samseg --threads 16 
```
whole brain

##
 - FIRST
FSL [link](https://web.mit.edu/fsl_v5.0.10/fsl/doc/wiki/FIRST(2f)StepByStep.html)
MAC ONLY
```bash
run_first_all -d -i bobs_t1.nii.gz -o synsthseg/bobs_t1_firstseg.nii.gz 
```
subparts

##
 - nnUNET (X) -> requires training
    - dbsegment
Local installation and model download [link](https://github.com/LuxImagingAI/DBSegment)
```bash
DBSegment -i samples/ -o samples/synsthseg/db -mp .
```
subparts

##
 - FastSufer
[link](https://github.com/Deep-MI/FastSurfer/blob/dev/doc/overview/EXAMPLES.md#example-1-fastsurfer-docker)
in FastSurfer dir
```bash
python3 myloop.py 
```

subparts
