# Styring av RPi3
## Navigation in terminal
```bash
ls #list all files and folders in current directory
```
```bash
cd folderDirectory #enter a folder
```


## Connect to RPi3 over ssh
### Terminal
```bash
ssh evenlisa@evenlisa.local
```
### CyberDuck
File protocol -  SFTP (SSH)
Server -         evenlisa.local
Username -       evenlisa
Password -       123


## Create folder
```bash
mkdir nameOfFile
```

## Edit file
```bash
nano nameOfFile
```

## Run a file
```bash
python3 nameOfFile.py
```

## Compiling and running C-file
### Compiling the C-file
```bash
gcc adc_sampler.c - lpigpio - lpthread - lm -o adc_sampler
```
### Running the C-file
```bash
sudo ./adc_sampler sampleAmount outputFile #Ex: sampleAmount = 31250
```
