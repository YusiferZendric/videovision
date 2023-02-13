# Video Remastering Tool

This is a Python script that uses the Replicate GFG-GAN API to remaster a video frame by frame. The script accepts the file name of a video as input and outputs a remastered version of the video. 

## Dependencies

To use this script, you will need to install the following dependencies: 
- OpenCV (`cv2`)
- Replicate (`replicate`)
- Base64 (`base64`)
- Requests (`requests`)
- Glob (`glob`)
- FFmpeg (`ffmpeg`)

You can install these dependencies using `pip` by running the following command:

```bash
pip install opencv-python replicate base64 requests glob ffmpeg
```


## How to Use

To use this script, follow these steps: 
1. Clone or download this repository. 
2. Open a terminal window and navigate to the directory containing the script. 
3. Set your Replicate API token as an environment variable by running the following command:

```bash
export REPLICATE_API_TOKEN=your_api_token
```
4. Run the script using the following command:

```bash

python videovision.py
```
5. When prompted, enter the file name of the video you want to remaster. 

The script will then convert the video into individual frames, send each frame to the Replicate GFG-GAN model for prediction, and output a remastered version of the video. The remastered video will be saved in the same directory as the script under the file name `output.mp4`. 

## Notes

- The Replicate GFG-GAN model used in this script is the `tencentarc/gfpgan` model with the `9283608cc6b7be6b65a8e44983db012355fde4132009bf99d976b2f0896856a3` version.
- This script assumes that the input video is in the same directory as the script. 
- The output video will be in MP4 format and will have the same frame rate as the input video.

# Disclaimer
With this free API, you can edit a limited number of images. If you have a large number of files, you can purchase the paid version of the API
