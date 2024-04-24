# Install hep-ml-lab with pip

## Prerequisites
- Python >= 3.9
- ROOT v6.26/14 (other versions should be OK. Required by Delphes)
- Madgraph5 v3.5.3 (other versions should be OK)
    - pythia8 v8.306 (installed by Madgraph5)
    - Delphes v3.5.0 (installed by Madgraph5)

The `keras` 3.0 requires the `tensorflow` 2.16 or higher, which is also the latest version. Before installing `tensorflow`, you need to install the following NVIDIA® softwares:

- [NVIDIA® GPU](https://www.nvidia.com/drivers) drivers version 450.80.02 or higher.
- [CUDA® Toolkit 11.8](https://developer.nvidia.com/cuda-toolkit-archive).
- [cuDNN SDK 8.6.0](https://developer.nvidia.com/cudnn).

Check the offical page of [tensorflow](https://www.tensorflow.org/install/pip) for more details.

## Installation
```bash
pip install hep-ml-lab
```

This will install the latest version of `keras` without any backends such as `tensorflow`, `pytorch` or `jax`. Since we have only tested `hep-ml-lab` on `tensorflow`, here we show how to install `tensorflow` as a backend. Then you can install `tensorflow` with the following command

```bash
pip install tensorflow[and-cuda]
```

## Fix the issue with tensorflow 2.16
There's an known issue with `tensorflow` 2.16: it couldn't recognize GPUs smoothly like before. So we have to link the related libraries manually. Use the following script to do so:

```bash
# set_nvidia.sh

# Attempt to locate the NVIDIA cudnn library file using Python.
NVIDIA_DIR=$(python -c "import nvidia.cudnn; print(nvidia.cudnn.__file__)" 2>/dev/null)

# Check if the NVIDIA directory variable is set (i.e., cudnn was found).
if [ ! -z "$NVIDIA_DIR" ]; then
    # Get the parent directory of the directory containing the __file__
    NVIDIA_DIR=$(dirname $(dirname $NVIDIA_DIR))

    # Iterate over all directories in the NVIDIA package directory.
    for dir in $NVIDIA_DIR/*; do
        # Check if the directory has a 'lib' subdirectory.
        if [ -d "$dir/lib" ]; then
            # Prepend the library path to LD_LIBRARY_PATH.
            export LD_LIBRARY_PATH="$dir/lib:$LD_LIBRARY_PATH"
        fi
    done
fi
```

Run it in the environment where you installed `tensorflow`:

```bash
bash set_nvidia.sh
```

Now you can test if `tensorflow` recognizes your GPUs:

```bash
python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
```

If it is set up successfully, you will see the following output:
```
[PhysicalDevice(name='/physical_device:GPU:0', device_type='GPU')]
```
