from setuptools import setup, find_packages
from pathlib import Path

setup(
    name='gurulearn',
    version='1.0.4',
    description='library for linear_regression and gvgg16 model generation(fixed bugs)',
    author='Guru Dharsan T',
    author_email='gurudharsan123@gmail.com',
    packages=find_packages(),
    install_requires=[
        'opencv-python',
        'scipy',
        'matplotlib',
        'tensorflow==2.13.1',
        'Keras',
        'pandas',
        'numpy',
        'plotly',
        'scikit-learn',
    ],
)
