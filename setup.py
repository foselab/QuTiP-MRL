from setuptools import setup, find_packages

setup(
    name="quditlib",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "matplotlib",
        "qutip"
    ],
    author="fabiopievani",
    description="Qudit circuit simulator",
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
)
