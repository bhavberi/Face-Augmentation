# Mid-Project Report

#### Team: _Computer Vision_

#### Team Members:
- [Anirudh Kaushik](https://github.com/anirudhkaushik2003)
- [Ankith Varun]()
- [Bhav Beri](https://github.com/bhavberi)
- [Sanyam Shah](https://github.com/maynaS)

----- 

### Problem Statement

_Face and Photograph Augmentation based on a Custom Theme_

### 📝 Introduction

Face and photograph augmentation are a form of  expression, communication and entertainment. Applying a mask on one’s face is surprising and fun and may also be considered artistic. We present a technique to make any photographed or animated face into a mask and an automated algorithm to apply masks on top of faces. To complete the resulting image, it is possible to apply gradual blur and vignetting and change the color temperature of the photograph.

### 🚀 Progress so far! 

- Face Detection: 
    - [x] Using the `Haar Cascade Classifier` with OpenCV to automatically detect faces in an image.
    - [x] Segmenting the face, and smoothening it for further use.
    - [x] Getting the facial landmarks.

- Special Instagram-like Effects:
    - [x] Gradient blurring
    - [x] Vignetting
    - [x] Changing the Color Temperature

### 🔜 Future Work

- For Mask Images
    - Creating a blending map for the face.
    - Creating a blending map for hat/ears (if any).
    - Marking facial landmarks on the mask image.
    - Defining mask specific effect parameters (if needed).
- For Photographs
    - Getting Transformation for the mask (based on landmarks).
    - Put the mask over the image, using the blending map.
    - (Optional) Add/Subtract the eye region from the mask over the face (to make it look more realistic).
    - (Optional) Add the hat/ears (if any).
    - Apply the special effects.