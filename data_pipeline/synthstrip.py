#!/usr/bin/env python3

from __future__ import print_function

# -------------------------------- SynthStrip --------------------------------

# This is a short wrapper script around a Docker-ized version of SynthStrip.
# The aim of this script is to minimize the effort required to use the
# SynthStrip docker container by automatically mounting any necessary input
# and output files paths. This script can be used with the same syntax as the
# default FreeSurfer `mri_synthstrip` command (use the --help flag for more info).
# Upon first use, the relevant docker image will be automatically pulled from
# DockerHub. To use a different SynthStrip version, update the variable below.
# https://hub.docker.com/r/freesurfer/synthstrip
version = '1.6'

# ----------------------------------------------------------------------------

import os
import sys
import subprocess
import shutil

# Sanity check on env
if shutil.which('docker') is None:
    print('Cannot find docker in PATH. Make sure it is installed.')
    exit(1)

# Since we're wrapping a Docker image, we want to get the full paths of all input and output
# files so that we can mount their corresponding paths. Tedious, but a fine option for now...
flags = ['-i', '--input', '-o', '--output', '-m', '--mask', '--model']

# Loop through the arguments and expand any necessary paths
idx = 1
args = []
paths = []
while idx < len(sys.argv):
    arg = sys.argv[idx]
    args.append(arg)
    if arg in flags:
        idx += 1
        path = os.path.realpath(os.path.abspath(sys.argv[idx]))
        args.append(path)
        paths.append(path)
    idx += 1
args = ' '.join(args)

# Get the unique mount points
mounts = list(set([os.path.dirname(p) for p in paths]))
mounts = ' '.join(['-v %s:%s' % (p, p) for p in mounts])

#print('Running SynthStrip from Docker')

# Get image tag
image = 'freesurfer/synthstrip:' + version

# Let's check to see if we have this container on the system
proc = subprocess.Popen('docker images -q %s' % image,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        universal_newlines=True)
stdout, stderr = proc.communicate()
if proc.returncode != 0:
    print(stderr)
    print('Error running docker command. Make sure Docker is installed.')
    exit(proc.returncode)

# If not, let's download it. Normally, docker run will do this automatically,
# but we're trying to be transparent here...
if not stdout:
    print('Docker image %s is not installed. Downloading now. This only needs to be done once.' % image)
    proc = subprocess.Popen('docker pull %s' % image, shell=True)
    proc.communicate()
    if proc.returncode != 0:
        print('Error running docker pull.')
        exit(proc.returncode)

# Go ahead and run the entry point
command = 'docker run %s %s %s' % (mounts, image, args)
proc = subprocess.Popen(command, shell=True)
proc.communicate()
if proc.returncode == 137:
    print('Container ran out of memory, try increasing RAM in Docker preferences.')
    exit(proc.returncode)
if proc.returncode != 0:
    print('Error running image.')
    exit(proc.returncode)
