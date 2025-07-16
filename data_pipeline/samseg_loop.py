import subprocess
from pathlib import Path

# Run FreeSurfer’s run_samseg command-line tool on each input T1w MRI scan to produce automated brain segmentations.

bob = Path(r"/home/data/mri_datasets/bobs/scans")
seg = Path(r"/home/data/mri_datasets/bobs/segmentations/samseg_BOB")
# root        = Path("../../Datasets/BOB")

inputs, outputs = [], []

# make directory for the output
seg.mkdir(parents=True, exist_ok=True)

# Collect scans & plan matches
for img in bob.rglob("*T1w.nii*"):
    rel_path = img.relative_to(bob)
    out_img  = seg / rel_path

    # ensure the parent folder for this output exists
    out_img.parent.mkdir(parents=True, exist_ok=True)

    inputs.append((str(img)))
    outputs.append((str(out_img)[:-7]))

i = 0
for inp, out_dir in zip(inputs[:], outputs[:]):
    cmd_samseg = f'run_samseg --input {inp} --output {out_dir} --threads 36'
    seg_process = subprocess.run([cmd_samseg], shell = True)

    print(f"DONE {i} + 1/ {len(inputs)}")
    print(out_dir)

# ps 3399608