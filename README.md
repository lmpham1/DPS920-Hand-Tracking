# Hand Movement Tracking with OpenCV

This file includes the instructions on how to run this project.
The full project report can be found in the [report.md file](report.md)

## Dependencies
- [opencv](https://opencv.org/)
- [numpy](https://numpy.org/)
  
## Set Up
Fork and clone this project:
```
git clone ...
```
If you already have `socv` environment set up with `anaconda`, just activate the environment:
```console
conda activate socv
```
If not, you can install the [dependencies](#dependencies) individually to set up the environment

## Running The Program
To run the program, you must have a live video feed (webcam or camera)
When you have everything set up, run the following command for each method:
- The segmentation method:
    ```console
    python contour.py
    ```
- The dense optical flow method:
    ```console
    python optical-flow.py
    ```