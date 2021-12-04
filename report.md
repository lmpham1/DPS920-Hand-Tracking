# Project Report for DPS920
Author: Le Minh Pham

## Honest Declaration

We, Le Minh Pham & Chike Browne, declare that the attached assignment is our own work in accordance with the Seneca Academic Policy.  We have not copied any part of this assignment, manually or electronically, from any other source including web sites, unless specified as references. We have not distributed our work to other students.

## Tasks Allocation

| #   | Name         | Task(s)                                                                                            |
| --- | ------------ | -------------------------------------------------------------------------------------------------- |
| 1   | Le Minh Pham | Implemented dense optical flow method, segmentation method, tested and planned future improvements |

## About This Project
**Hand Movement Tracking with OpenCV** is a video processing project in which the goal is to explore different approaches on how to detect and track hand movements in a video. The movements that we are currently tracking includes:
- Moving to the right
- Moving to the left
- Moving upward
- Moving downward
Hand movement tracking has many potential, especially in the fields of Internet of Things and Virtual Reality.

## Method
We analysed two different approaches: the segmentation method and the dense optical flow method. Both of the methods compare two consecutive frames to detect and track the movements. The segmentation method uses `cv.absdiff` to find the absolute difference between two frames and apply `cv.findContours` to detect the movement. Meanwhile, the dense optical flow method uses `cv.calcOpticalFlowFarneback` function to calculate the flow vectors of the movement. It then calculate the direction of movement and produce a result. Overall, the dense optical flow method are more effective than the segmentation method in tracking hand movements

## Data & Test Result
The data we use for this project is live video feed from a webcam. We divided the data into 3 test cases based the interference of other objects with the hand:
- Test case 1: Video with only a hand and no other objects.

![only-hand test case](https://media.giphy.com/media/9dG8rZcrGNrAfGNepz/giphy.gif)

- Test case 2: Video with a hand and a face, to test if skin color will affect the detection

![hand with face test case](https://media.giphy.com/media/UNkJqe4RJXdKAZV0Ue/giphy.gif)

- Test case 3: Video with a hand and another moving object in the frame.

![hand with moving pen test case](https://media.giphy.com/media/BrUybPbXthIh9g0cy1/giphy.gif)

### Evaluation
After running each test case 20 times, we got the following results:

| Test Case # | Success Rate | Fail Rate |
| ----------- | ------------ | --------- |
| 1           | 95%          | 5%        |
| 2           | 75%          | 25%       |
| 3           | 25%          | 75%       |

From the results above, we can see that the biggest limitation of the program is the present of other moving objects can heavily impact the result. This is because the programs detect the predominant movement in the video, and when another object has a bigger movement than the hand, the movement of that object gets picked up instead.

## Future Plans
- Use a machine learning object recognition AI to detect a hand in the frame before applying the tracking algorithm. We have actually trained an Azure Custom Vision AI to detect hands using the data in the [Training Images folder](Training%20Images). However, we have not been successful at plugging it into our Python code yet.
- Use convex hull algorithm to detect movement direction in segmentation method. The convex hull algorithm can help detect the center of the hand in each frame, which we can use to calculate the direction.
- We can also use convex hull to check if the hand is in an opened or closed position, as suggested in [this article](https://gogul.dev/software/hand-gesture-recognition-p2)