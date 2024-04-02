# SlideDetect - A tool for detecting slide changes in videos and saving them as PowerPoint slides.
# Copyright (C) 2024 Nindo Punturi
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/gpl-3.0.html>.

from setuptools import setup, find_packages

def read_readme():
    try:
        with open("README.md", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "Long description could not be read from README.md"
    
setup(
    name='SlideDetector',
    version='0.1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'slide-detector=slide_detector.slide_detector:main',
        ],
    },
    install_requires=[
        'opencv-python-headless',
        'numpy',
        'python-pptx',
        'Pillow',
        'tqdm',
    ],
    python_requires='>=3.6',
    description='A tool for detecting slide changes in videos and saving them as PowerPoint slides.',
    long_description=read_readme(),
    long_description_content_type='text/markdown',
    author='gitrandoname',
    author_email='165725564+gitrandoname@users.noreply.github.com',
    keywords='video processing slide detection PowerPoint',
    project_urls={
        'Source': 'https://github.com/gitrandoname/SlideDetect.git',
        'Tracker': 'https://github.com/gitrandoname/SlideDetect/issues',},
    license='GPLv3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)