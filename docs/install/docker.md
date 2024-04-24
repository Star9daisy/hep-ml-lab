# Use hep-ml-lab in Docker

## hml-env image
`hml-env` is a comprehensive programming environment designed to facilitate research and development at the intersection of high-energy physics and machine learning. 

This image is based on `nvidia/cuda:11.8.0-cudnn8-devel-ubuntu20.04`. Below is a pre-installed software list:

| Type                | Version                                                                                          |
| ------------------- | ------------------------------------------------------------------------------------------------ |
| General             | shell: zsh (oh-my-zsh)                                                                           |
|                     | Python: 3.11.5 (Miniconda)                                                                       |
| High energy physics | [ROOT](https://root.cern): 6.26.14                                                               |
|                     | [LHAPDF](https://lhapdf.hepforge.org): 6.5.3                                                     |
|                     | [MadGraph5_aMC@NLO](https://launchpad.net/mg5amcnlo): 3.5.3 (with Pythia8 and Delphes installed) |

You can use `hep-ml-lab` in a Docker container. The Docker image (`hml-env`) is available on [Docker Hub](https://hub.docker.com/r/star9daisy/hml-env). This way, you can avoid the hassle of installing the NVIDIA® softwares.

## Prerequisites
However, you still need to install the NVIDIA® drivers on your host machine. The `hml-env` image is built on top of the `nvidia/cuda` image, which requires the NVIDIA® drivers to be installed on the host machine. Check the [official page](https://hub.docker.com/r/star9daisy/hml-env) for more details of prerequisites.


## Start a container
Once you have installed the NVIDIA® drivers, you can pull the `hml-env` image with the following command:

```bash
docker pull star9daisy/hml-env
```

Then start a container with the following command:

```bash
docker run -it --gpus all star9daisy/hml-env
```

## Use `pip` to continue installation of `hep-ml-lab`
Check this part in the [pip installation guide](pip.md) for more details.
