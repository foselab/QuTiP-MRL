from setuptools import setup, find_packages

setup(
    name="QuTiP-MRL",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "matplotlib",
        "qutip"
    ],
    author="FOSELAB@UniBG",
    description="QuTiP-MRL - Qudit circuit simulator",
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
)
