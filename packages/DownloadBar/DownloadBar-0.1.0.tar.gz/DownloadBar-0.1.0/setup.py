from setuptools import setup, find_packages

setup(
name='DownloadBar',
version='0.1.0',
author='Dikshant Ghimire',
author_email='dikkughimire@gmal.com',
description='A simple package for displaying the download progress bar with percentage in Command Line',
packages=find_packages(),
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: MIT License',
'Operating System :: OS Independent',
],
python_requires='>=3.6',
entry_points={"console_scripts": ["DownloadBar = src.main:main"]},
)

