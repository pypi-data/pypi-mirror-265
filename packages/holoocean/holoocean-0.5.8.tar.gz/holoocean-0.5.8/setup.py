from setuptools import setup, find_packages

with open("README.md") as f:
    readme = f.read()

setup(
    name="holoocean",
    version="0.5.8",
    description="An Open-Source Simulator for Marine Robotic Autonomy",
    long_description=readme,
    long_description_content_type="text/markdown",
    post_install_message="\033[91mFatal Error: Due to Unreal Engine EULA changes and requirements, HoloOcean can no longer be installed via pypi (An empty installation is being installed instead and should be removed). However, HoloOcean can still be easily installed. Please read the updated installation instructions at https:\\\\holoocean.readthedocs.io for more details.",
    author="BYU Field Robotic Systems Lab, Joshua Mangelson, (and many others)",
    author_email="mangelson@byu.edu",
    url="https://holoocean.readthedocs.io/",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    license='MIT License (BYU Client Code), Unreal EULA for Unreal Code',
    python_requires=">=3.6",
    install_requires=[
        'posix_ipc >= 1.0.0; platform_system == "Linux"',
        'pywin32 <= 228; platform_system == "Windows"',
        'numpy'
    ],
)
