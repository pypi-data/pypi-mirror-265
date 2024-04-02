
import re
import os
import subprocess

from setuptools import find_packages, setup

VERSION = "1.2.2"

# add the README.md file to the long_description
with open("README.md", "r") as fh:
    long_description = fh.read()


def get_cuda_version():
    nvcc_paths = ["nvcc", "/usr/local/cuda/bin/nvcc"]
    for nvcc in nvcc_paths:
        try:
            output = subprocess.check_output([nvcc, "--version"]).decode()
            match = re.search(r"release (\d+\.\d+)", output)
            if match:
                return float(match.group(1))
        except FileNotFoundError:
            continue
    print("nvcc is not installed.")
    return None


cuda_version = get_cuda_version()


if cuda_version is not None:
    if 11.0 <= cuda_version < 12.0:
        dali = "nvidia-dali-cuda110"
    elif 12.0 <= cuda_version < 13.0:
        dali = "nvidia-dali-cuda120"
    else:
        dali = "nvidia-dali-cuda110"
        print("WARNING! Unsupported CUDA version. Some training/inference features will not work.")
else:
    dali = "nvidia-dali-cuda110"
    print("WARNING! CUDA not found. Some training/inference features will not work.")

print(f"Found CUDA version: {cuda_version}, using DALI: {dali}")


# basic requirements
install_requires = [
    "fiftyone",
    "h5py",
    "hydra-core",
    "imgaug",
    "kaleido",  # export plotly figures as static images
    "kornia",
    "lightning",
    "matplotlib",
    "moviepy",
    "opencv-python",
    "pandas>=2.0.0",
    "pillow",
    "plotly",
    "pytest",
    "scikit-learn",
    "seaborn",
    "streamlit",
    "tensorboard",
    "torchtyping",
    "torchvision",
    "typeguard",
    "typing",
    dali,
    # PyPI does not support direct dependencies, so we remove this line before uploading from PyPI
    # "segment_anything @ git+https://github.com/facebookresearch/segment-anything.git",
]

# additional requirements
extras_require = {
    "dev": {
        "black",
        "flake8",
        "isort",
        "Sphinx",
        "sphinx_rtd_theme",
        "sphinx-rtd-dark-mode",
        "sphinx-automodapi",
        "sphinx-copybutton",
    },
    "extra_models": {
        "lightning-bolts",  # resnet-50 trained on imagenet using simclr
    },
}

# collect all data and script files
data_files = []
for root, dirs, files in os.walk("data"):
    data_files.extend([os.path.join(root, f) for f in files])
for root, dirs, files in os.walk("scripts"):
    data_files.extend([os.path.join(root, f) for f in files])


setup(
    name="lightning-pose",
    packages=find_packages(exclude=("data", "docs", "scripts", "tests")),
    version=VERSION,
    description="Semi-supervised pose estimation using pytorch lightning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Dan Biderman and Matt Whiteway",
    install_requires=install_requires,
    extras_require=extras_require,
    author_email="danbider@gmail.com",
    url="https://github.com/danbider/lightning-pose",
    keywords=["machine learning", "deep learning", "computer_vision"],
    package_data={"lightning_pose": data_files},
    include_package_data=True,
)
