# data/utils.py

import shlex
import subprocess
import sys
import matplotlib.pyplot as plt
import nibabel as nib
import os
import platform
import numpy as np
import random, math
import sklearn.metrics as skl

def visualize_nifti_depth(file_path, slices=3, save=False):
    """
    Visualize the depth slices of a NIfTI file along all three axes.

    Parameters:
    file_path (str): Path to the NIfTI file.
    slices (int): Number of slices to visualize along each axis.
    save (bool): Whether to save the figure.
    """
    # Load 
    img = nib.load(file_path)
    data = img.get_fdata()
    if data.ndim != 3:
        raise ValueError("The NIfTI file must be 3-dimensional.")

    # middle slices + slice size
    mid_slice_x = data.shape[0] // 2
    mid_slice_y = data.shape[1] // 2
    mid_slice_z = data.shape[2] // 2
    fifth_x = data.shape[0] // 5
    fifth_y = data.shape[1] // 5
    fifth_z = data.shape[2] // 5

    slices_x = [data[mid_slice_x - fifth_x, :, :], data[mid_slice_x, :, :], data[mid_slice_x + fifth_x, :, :]]
    slices_y = [data[:, mid_slice_y - fifth_y, :], data[:, mid_slice_y, :], data[:, mid_slice_y + fifth_y, :]]
    slices_z = [data[:, :, mid_slice_z - fifth_z], data[:, :, mid_slice_z], data[:, :, mid_slice_z + fifth_z]]

    # figure
    fig, axes = plt.subplots(3, 3, figsize=(8, 8))

    # x-axis plots
    for ax, slice_data in zip(axes[0], slices_x):
        ax.imshow(slice_data.T, cmap='gray', origin='lower')
        ax.axis('off')

    # y-axis plots
    for ax, slice_data in zip(axes[1], slices_y):
        ax.imshow(slice_data.T, cmap='gray', origin='lower')
        ax.axis('off')

    # z-axis plots
    for ax, slice_data in zip(axes[2], slices_z):
        ax.imshow(slice_data.T, cmap='gray', origin='lower')
        ax.axis('off')

    plt.tight_layout()
    if save:
        plt.savefig('nifti_depth_visualization.png')

    return fig

def which(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
        if is_exe(os.path.join(os.getenv('FREESURFER_HOME'),'bin',program)):
            return os.path.join(os.getenv('FREESURFER_HOME'),'bin',program)
        if is_exe(os.path.join('.',program)):
            return os.path.join('.',program)

    return None

def run_cmd(cmd,err_msg):
    """
    execute the comand
    """
    clist = cmd.split()
    progname=which(clist[0])
    if (progname) is None:
        print('ERROR: '+ clist[0] +' not found in path!')
        sys.exit(1)
    clist[0]=progname
    cmd = ' '.join(clist)
    print('#@# Command: ' + cmd+'\n')

    args = shlex.split(cmd)
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if stderr != b'':
        print('ERROR: '+ err_msg)

    return stdout

def is_docker_running():
    """Check if Docker daemon is running."""
    try:
        subprocess.run(["docker", "info"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

def start_docker():
    """Start Docker daemon based on the OS."""
    system = platform.system()

    try:
        if system == "Linux":
            print("Starting Docker daemon on Linux...")
            subprocess.run(["sudo", "systemctl", "start", "docker"], check=True)
        elif system == "Darwin":  # macOS
            print("Starting Docker daemon on macOS...")
            subprocess.run(["open", "-a", "Docker"], check=True)
        elif system == "Windows":
            print("Starting Docker daemon on Windows...")
            subprocess.run(["powershell", "Start-Service", "docker"], check=True, shell=True)
        else:
            print(f"Unsupported OS: {system}")
            sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Failed to start Docker: {e}")
        sys.exit(1)

def fractal_analysis(volume_path, verbose=True):
    ### NIFTI IMAGE LOADING ###
    image_path = volume_path
    img = nib.load(image_path)
    nii_header = img.header
    imageloaded = img.get_fdata()
    imageloaded.shape
    ### CHECK THE IMAGE ISOTROPY ###
    voxels_size = nii_header['pixdim'][1:4]
    ### COMPUTING THE MINIMUM AND MAXIMUM SIZES OF THE IMAGE ###
    L_min = voxels_size[0]
    if verbose : print(f'The voxel size is {voxels_size[0]} x {voxels_size[1]} x {voxels_size[2]} mm^3')
    if verbose : print(f'Shape of the image : {imageloaded.shape}')
    if verbose : print(f'The minimum size of the image is {L_min} mm')
    Ly=imageloaded.shape[0]
    Lx=imageloaded.shape[1]
    Lz=imageloaded.shape[2]
    if Lx > Ly:
        L_Max = Lx
    else:
        L_Max = Ly
    if Lz > L_Max:
        L_Max = Lz
    if verbose : print(f'The maximum size of the image is {L_Max} mm')
    ### NON-ZERO VOXELS OF THE IMAGE: NUMBER AND Y, X, Z COORDINATES ###
    voxels=[]
    for i in range(Ly):
        for j in range(Lx):
            for k in range(Lz):
                if imageloaded[i,j,k]>0:
                    voxels.append((i,j,k))
    voxels=np.asarray(voxels)
    if verbose : print(f'The non-zero voxels in the image are (the image volume) {voxels.shape[0]} / {math.prod(imageloaded.shape)}')
    ### LOGARITHM SCALES VECTOR AND COUNTS VECTOR CREATION ###
    Ns = []
    scales = []
    stop = math.ceil(math.log2(L_Max))
    for exp in range(stop+1):
        scales.append(2**exp)
    scales = np.asarray(scales)
    random.seed(1)
    ### THE 3D BOX-COUNTING ALGORITHM WITH 20 PSEUDO-RANDOM OFFSETS ###
    for scale in scales:
        if verbose : print(f'Computing scale {scale}...')
        Ns_offset=[] 
        for i in range(20): 
            y0_rand = -random.randint(0,scale)
            yend_rand = Ly+1+scale
            x0_rand = -random.randint(0,scale)
            xend_rand = Lx+1+scale
            z0_rand = -random.randint(0,scale)
            zend_rand = Lz+1+scale
            # computing the 3D histogram
            H, edges=np.histogramdd(voxels, bins=(np.arange(y0_rand,yend_rand,scale), np.arange(x0_rand,xend_rand,scale), np.arange(z0_rand,zend_rand,scale)))
            Ns_offset.append(np.sum(H>0))
            # print(f'======= Offset {i+1}: x0_rand = {x0_rand}, y0_rand = {y0_rand}, z0_rand = {z0_rand}, count = {np.sum(H>0)}')
        Ns.append(np.mean(Ns_offset))
    ### AUTOMATED SELECTION OF THE FRACTAL SCALING WINDOW ### 
    minWindowSize = 5 # in the logarithm scale, in the worst case, 5 points cover more than 1.2 decades, which should be the minimum fractal scaling window possible, to define an object as fractal (Marzi et al., Scientific Reports 2020)
    scales_indices = [] 

    for step in range(scales.size, minWindowSize-1, -1):
        for start_index in range(0, scales.size-step+1):
            scales_indices.append((start_index, start_index+step-1))
    scales_indices = np.asarray(scales_indices)    

    k_ind = 1 # number of indipendent variables in the regression model
    R2_adj = -1
    for k in range(scales_indices.shape[0]):
        coeffs=np.polyfit(np.log2(scales)[scales_indices[k,0]:scales_indices[k,1] + 1], np.log2(Ns)[scales_indices[k,0]:scales_indices[k,1] + 1], 1)
        n = scales_indices[k,1] - scales_indices[k,0] + 1 
        y_true = np.log2(Ns)[scales_indices[k,0]:scales_indices[k,1] + 1]
        y_pred = np.polyval(coeffs,np.log2(scales)[scales_indices[k,0]:scales_indices[k,1] + 1])
        R2=skl.r2_score(y_true,y_pred)
        R2_adj_tmp = 1 - (1 - R2)*((n - 1)/(n - (k_ind + 1)))
        if verbose : print(f'In the interval [{scales[scales_indices[k,0]]}, {scales[scales_indices[k,1]]}] voxels, the FD is {-coeffs[0]} and the determination coefficient adjusted for the number of points is {R2_adj_tmp}')
        R2_adj = round(R2_adj, 3)
        R2_adj_tmp = round(R2_adj_tmp, 3)
        if R2_adj_tmp > R2_adj:
            R2_adj = R2_adj_tmp
            FD = -coeffs[0]
            mfs = scales[scales_indices[k,0]]
            Mfs = scales[scales_indices[k,1]]
            fsw_index = k
            coeffs_selected = coeffs
        FD = round(FD, 4)
    ### FRACTAL ANALYSIS RESULTS ###
    mfs = mfs * L_min
    Mfs = Mfs * L_min
    # print("mfs automatically selected:", mfs)
    # print("Mfs automatically selected:", Mfs)
    print("FD automatically selected:", FD)

    return FD