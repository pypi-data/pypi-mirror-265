from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="beep_utils",
    version="0.0.5",
    author="Lucas Pinho",
    description="Beep Saúde ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["beep_utils"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[]
)
