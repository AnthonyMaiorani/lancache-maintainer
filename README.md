# Lancache-Maintaner

> A small python script to purge corrupted lancache entries for Steam and Epic Games.

[![License](https://img.shields.io/github/license/Caboose700/lancache-maintainer)](http://badges.mit-license.org) 
![Platform](https://img.shields.io/badge/python-v3.8.1-blue) 
![Platform](https://img.shields.io/badge/platform-Linux-brightgreen)

## Description
This script reads the "access.log" created by 
"[Monolithic Game Download Cache Docker Container](https://github.com/lancachenet/monolithic)" to identify files 
which are corrupted. Corrupted files will be requested multiple times. If the script detects a file being requested five
times in a row, it will purge the file from the cache. 

## Requirements
* [Tailer Python Module](https://pypi.org/project/tailer/)
* Must be executed on machine running 
"[Monolithic Game Download Cache Docker Container](https://github.com/lancachenet/monolithic)".

```
sudo apt update && sudo apt install python3 python3-pip -y && pip3 install tailer
```

## Limitations
* Only watches "access.log" for "Steam" and "Epic Games" cache files.

## Configuration
File paths for the cache folder need to be changed in "main.py" if they differ from the default install 
of the "[Monolithic Game Download Cache Docker Container](https://github.com/lancachenet/monolithic)".

## Lancache Maintainer Service Setup
Follow these instructions to set up the Lancache Maintainer as a systemd service on your Linux system. 

### Step 1: Modify the Service File
Before setting up the service, you need to modify the lancache-maintainer.service file to match your system's configuration, specifically the username and the path to the script.

Open the lancache-maintainer.service file in a text editor.
Locate the line that starts with 'User=' and replace 'anthony' with your actual username.
Make sure the 'ExecStart' and 'WorkingDirectory' paths are correct for your setup.
Save and close the file after making these changes.
### Step 2: Copy the Service File to System Directory
Copy the modified service file to the /etc/systemd/system/ directory. This requires superuser privileges.


```
sudo cp lancache-maintainer.service /etc/systemd/system/lancache-maintainer.service
```
### Step 3: Reload Systemd Manager Configuration
After copying the service file, reload the systemd manager configuration to recognize the new service.

```
sudo systemctl daemon-reload
```
### Step 4: Enable the Service
To have the Lancache Maintainer service start automatically at boot, enable it using the following command:

```
sudo systemctl enable lancache-maintainer.service
```
### Step 5: Start the Service
Start the Lancache Maintainer service with:
```
sudo systemctl start lancache-maintainer.service
```
### Step 6: Check the Service Status
Verify that the service is running properly:

```
sudo systemctl status lancache-maintainer.service
```
If the service is active and running, you have successfully set up the Lancache Maintainer service. If you encounter any errors, check the service's logs for more details:

```
sudo journalctl -u lancache-maintainer.service
```

### Troubleshooting
If the service fails to start, ensure that your Python script is executable and working correctly when run manually.

Verify that all paths in the lancache-maintainer.service file are correct and accessible by the user specified in the service file.

For issues related to Python dependencies, ensure that all required packages are installed in the environment that the script is running in.