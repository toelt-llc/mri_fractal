from pathlib import Path
import nibabel as nib
import numpy as np

# Extracts and saves binary masks for each label in the segmentation output file.

# Freesurfer label mapping
index_to_label = {}
with open('FreeSurferColorLUT.txt', 'r') as file:
    for line in file:
        # comments or empty
        if line.startswith('#') or not line.strip():
            continue

        parts = line.split()
        index = int(parts[0])
        label_name = ' '.join(parts[1:-4])
        index_to_label[index] = label_name

bob = Path(r"/home/data/mri_datasets/bobs/scans/t1")
seg = Path(r"/home/data/mri_datasets/bobs/scans/segs/")
# root        = Path("../../Datasets/BOB")

inputs, outputs = [], []

# Collect scans & plan matches
for img in bob.rglob("*T1w.nii*"):
    # print(img)
    rel_path = img.relative_to(bob)
    out_img  = seg / img.name
    # print(out_img)
    # ensure the parent folder for this output exists
    out_img.parent.mkdir(exist_ok=True)
    outputs.append((str(out_img)[:-7]))

# Loop through each segmented file
for p in outputs:

    # create a segmentation_outputs folder alongside the samseg outputs
    sess_dir  = Path(f"{p}") / "segmentation_outputs"
    print(sess_dir)
    sess_dir.mkdir(parents=True, exist_ok=True)


    # load the segmentation volume
    vol_path = f"{p[:-4]}_desc-aseg_dseg.nii.gz"
    img   = nib.load(vol_path)
    data  = img.get_fdata().astype(int)
    labels = np.unique(data)
    labels = labels[labels != 0]              # skip background label 0

    print(f"[{Path(p).stem}] saving masks for labels: {labels}")

    # write one binary mask per label
    for lbl in labels:
        name = index_to_label.get(int(lbl))
        if not name:
            print(f"skipping unknown label {lbl}")
            continue

        mask = (data == lbl).astype(np.uint8)
        mask_img = nib.Nifti1Image(mask, img.affine, img.header)
        mask_fp  = sess_dir / f"{lbl:03d}_{name}.nii.gz"
        nib.save(mask_img, str(mask_fp))
        print(f"wrote {mask_fp}")
        # print(f"wrote {mask_fp.name}")
