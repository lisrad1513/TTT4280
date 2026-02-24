# Commands

## Testing video and photo
### Photo
```bash
rpicam-still -v -o foo.jpg
```

### Video
```bash
rpicam-vid -v -o foo.h264
```

### Convert video
We will use FFMPEG to convert the files. Install this to the current computer.

```bash
brew install ffmpeg
```

Then, navigate to the correct folder

```bash
ffmpeg -i video.h264 -c copy video.mp4
```

## Record propper video

### Recording video and converting directly on the RPi3
Navigate to the proper folder, and run both of the following commands in the terminal on the RPi3.

```bash
python3 record_video_upgrade.py videoer/testopptak
ffmpeg -framerate 60 -i videoer/testopptak.h264 -c copy videoer/testopptak.mp4
```
The resolution and framerate of the camera was originally 1640 x 922 at 40fps, but we changed it to 1920 x 1080 at 60 fps. We did this in order to get more data out of our camera.

