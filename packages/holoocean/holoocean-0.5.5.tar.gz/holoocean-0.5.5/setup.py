from setuptools import setup, find_packages

with open("README.md") as f:
    readme = f.read()

setup(
    name="holoocean",
    version="0.5.5",
    description="An Open-Source Simulator for Marine Robotic Autonomy",
    long_description=readme,
    long_description_content_type="text/markdown",
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