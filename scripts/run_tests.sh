#!/bin/bash

# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -
echo 'export PATH="/github/home/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Install HML dependencies
poetry install

# Setup environment variables
. /root/softwares/root6/bin/thisroot.sh
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/root/softwares/madgraph5/Delphes
export ROOT_INCLUDE_PATH=/root/softwares/madgraph5/Delphes/external

# Install additional Python packages
poetry run pip install keras --upgrade
poetry run pip install torch==2.1.0 torchvision>=0.16.0 --extra-index-url https://download.pytorch.org/whl/cpu

# Run tests
poetry run pytest -v --cov=hml --cov-report=xml tests
