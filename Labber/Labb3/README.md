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
Install this to the computer

```bash
brew install ffmpeg
```

Then, navigate to the correct folder

```bash

ffmpeg -i video.h264 -c copy video.mp4
```

##Take propper video

### Take video and convert directly on the Pi
```bash
python3 record_video_upgrade.py videoer/testopptak
```
```bash
ffmpeg -framerate 60 -i videoer/testopptak.h264 -c copy videoer/testopptak.mp4
```


