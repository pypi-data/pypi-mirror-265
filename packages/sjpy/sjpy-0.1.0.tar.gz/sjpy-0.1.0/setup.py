from setuptools import find_packages, setup

setup(
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
name='sjpy',
version='0.1.0',
author='Kacper Remzak',
author_email='remzak.k@gmail.com',
description='Polish dictionary API for python',
packages=find_packages(),
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: MIT License',
'Operating System :: OS Independent',
],
python_requires='>=3.6',
)