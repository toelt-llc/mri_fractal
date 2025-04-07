## Installation

### Python env 

### 1. Create a Conda Environment with Python 3.11
[install anaconda](https://www.anaconda.com/download)
Create conda env with python 3.11
```bash
conda create -n mrienv python=3.11
```

Activate the environment:
```bash
conda activate mrienv
```

Install Dependencies
Ensure you are in the `project-root` directory where the `requirements.txt` file is located.
Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

### Other tools

#### DHCP registration templates

For the registration step, the dhcp comes with [registration atlases](https://gin.g-node.org/BioMedIA/dhcp-volumetric-atlas-groupwise) which can be downloaded (1Gb). 

#### Docker
To run the skull-stripping and segmentations models, we use their dockerised version.  
 - [Install docker desktop](https://docs.docker.com/get-started/get-docker/)
 - Pull the 2 necessary images : 
    ```bash 
    docker pull cookpa/synthseg:conda-0.1
    docker pull freesurfer/synthstrip:1.6
    ````

 - The images can also be search within docker desktop using **freesurfer/synthstrip:1.6** and **cookpa/synthseg:conda-0.1**


#### Freesurfer (optional for now)
Although used in development and tests, it is not currently used in the pipeline since the main parts are run on docker.  
Release [7.4.1](https://surfer.nmr.mgh.harvard.edu/fswiki/rel7downloads) is the one used.  