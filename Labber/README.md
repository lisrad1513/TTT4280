# Controlling RPi3
Remember to connect both the PC and the RPi3 to the same wifi!
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
ssh evenlisa@evenlisa.local #password: 123
```
### CyberDuck
File protocol -  SFTP (SSH) <br>
Server -         evenlisa.local <br>
Username -       evenlisa <br>
Password -       123 <br>


## Create folder
```bash
mkdir nameOfFile
```

## Edit file
```bash
nano nameOfFile
```
Press `Ctrl+X` to confirm changes, and then `Y` to save the changes to the file

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
