from pathlib import Path
import utils as ut
import pandas as pd

# Performs fractal dimension (FD) analysis on whole-brain segmentations and individual masks for each label.

def parse_filename_metadata(path_str):
    # Example: sub-116056_ses-3mo_space-INFANTMNIacpc_T1w
    name = Path(path_str).stem
    parts = name.split("_")
    participant_id = next((p for p in parts if p.startswith("sub-")), "")
    session_id = next((p for p in parts if p.startswith("ses-")), "")
    return name, participant_id, session_id

ds_info = pd.read_csv('sessions.tsv', sep ='\t')

bob = Path(r"/home/data/mri_datasets/bobs")
seg = Path(r"/home/data/mri_datasets/bobs/segmentations/samseg_BOB")

inputs, outputs = [], []
# Collect scans & plan matches
for img in bob.rglob("*/anat/*T1w.nii*"):
    rel_path = img.relative_to(bob)
    out_img  = seg / "t1"/ img.name

    # ensure the parent folder for this output exists
    out_img.parent.mkdir(parents=True, exist_ok=True)

    inputs.append((str(img)))
    outputs.append((str(out_img)[:-7]))


## Loop

data_folder = Path("/home/data/mri_datasets/bobs/segmentations/samseg_BOB/t1/")

fd_results = []

# loop over whole-brain dseg files
for p in outputs:
    dseg = Path(f"{p}") / "seg.nii.gz"
    filename, participant_id, session_id = parse_filename_metadata(p)
    print(f"processing {dseg.parent.name}")
    # print(f"filename: {filename}, participant_id: {participant_id}, session_id: {session_id}")

    # whole-brain FD
    fd, (mfs, Mfs), _ = ut.fractal_analysis(str(dseg), verbose=False)
    fd_results.append({
        'participant_id': participant_id,
        'session_id':    session_id,
        'label':         None,
        'name':          'whole_brain',
        'fd':            fd,
        'min_box_size':  mfs,
        'max_box_size':  Mfs
    })

    # per-mask FD
    mask_dir = dseg.parent / "segmentation_outputs"
    if not mask_dir.exists():
        print(f" no masks found for {dseg.stem}, skipping masks")
        continue

    for mask_fp in mask_dir.glob("*.nii.gz"):
        # extract label and name from filename "###_LabelName.nii.gz"
        stem = mask_fp.stem
        lbl_str, name = stem.split("_", 1)
        lbl = int(lbl_str)

        fd, (mfs, Mfs), _ = ut.fractal_analysis(str(mask_fp), verbose=False)
        fd_results.append({
            'participant_id': participant_id,
            'session_id':    session_id,
            'label':         lbl,
            'name':          name,
            'fd':            fd,
            'min_box_size':  mfs,
            'max_box_size':  Mfs
        })


df_fd = pd.DataFrame(fd_results)
df_fd = df_fd[
    ['participant_id','session_id','label','name','fd','min_box_size','max_box_size']
]

df_fd_merged = df_fd.merge(
    ds_info,
    on=['participant_id', 'session_id'],
    how='left'
)

# remove any trailing ".nii"
df_fd_merged['name'] = (
    df_fd_merged['name']
      .str.replace(".nii", "")
)

df_fd_merged.to_csv('BOB_fd_results_samseg.csv', index=False)
print("FD results saved to 'BOB_fd_results_samseg.csv'")

# ps 3306060