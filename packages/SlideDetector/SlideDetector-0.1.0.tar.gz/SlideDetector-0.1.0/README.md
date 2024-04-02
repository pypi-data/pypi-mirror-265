# SlideDetect

SlideDetect is a Python tool designed to detect slide changes in videos and save them as individual slides in a PowerPoint presentation. It utilizes computer vision techniques to analyze video frames and identify moments where slide content changes, making it an invaluable resource for capturing presentation slides from recorded lectures, webinars, and other video presentations.

## Installation

SlideDetect requires Python 3.6 or newer. Before installing SlideDetect, ensure you have Python installed on your system. You can download and install SlideDetect using the following command:

```bash
pip install SlideDetect
```

## Usage

After installation, you can use SlideDetect from the command line. Here's how you can detect slides in a video:

```bash
slide-detector <path_to_video> <output_folder> --threshold <threshold_value>
```
* `<path_to_video>`: The path to the video file you want to process.

* `<output_folder>`: The directory where you want to save the extracted slides.

* *(Optional)* `--threshold <threshold_value>`: A numeric threshold value between 0 and 1 for detecting slide changes. Higher values make slide change detection more strict. The default --threshold value is 1 if `--threshold <threshold_value>` has no input.

Example:
```bash
slide-detector "C:\Users\Videos\Example.mp4" "C:\Users\Videos\" --threshold 0.8
```
## Features
* Video Processing: Efficiently processes video files to detect slide changes.

* Slide Extraction: Saves detected slides as individual PowerPoint slides.

* Customizable Threshold: Allows the user to set a custom threshold for slide change detection, accommodating different video qualities and styles.

## Dependencies
SlideDetect depends on the following Python libraries; however, these dependencies will be automatically installed when installing SlideDetect via pip:

* OpenCV
* NumPy
* python-pptx
* Pillow
* tqdm


## License
***SlideDetect is licensed under the GNU General Public License v3.0 (GPLv3). See the LICENSE file for more details or visit <https://www.gnu.org/licenses/gpl-3.0.html>.***

## Contributing
Contributions to SlideDetect are welcome! Please feel free to report issues, suggest features, or submit pull requests.

## Contact
If you have any questions or feedback, please open an issue on the GitHub repository.



