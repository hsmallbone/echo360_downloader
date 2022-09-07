# Echo Downloader
A python script to download Echo360 lectures.

## Usage
Copy and run link_extractor.js in the developer console on the Echo360 page. Make sure you are in the right script context.
Run the python command it outputs.

## Details
The python script requires wget, scikit-video and opencv2. It takes a list of content URLs and lecture names as its inputs and downloads and joins the flipbook images from Echo360.
The FPS and video backend can be customised in the code.