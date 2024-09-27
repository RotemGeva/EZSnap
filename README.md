# EZSnap

EZSnap is a handy tool designed for Software Quality Assurance (SQA) testers, allowing them to easily take screenshots during tests and save them in a designated folder. 

## Features

- **Screenshot Capture**: Capture screenshots using the key combination `Ctrl + Alt + Z`.
- **Notifications**: Receive notifications every time a screenshot is taken.
- **Shutdown**: Close EZSnap by pressing `Ctrl + Alt + S`.
- **Status Check**: Verify if EZSnap is still running by pressing `Ctrl + Alt + X`.
- **Customizable Settings**: Modify image names, target folder names and locations, timeout settings, and numbering order via `configuration.ini`.

## Configuration

The `configuration.ini` file allows you to customize the following settings:

[Location]

; Set to ON to save images in a folder next to the script executable.

; Set to OFF to save images in a specific folder defined by the INI key: Path.

UseDefaultFolder = ON

Path = null

[Names]

; Set to ON to use "EZSnap_Images" as the target folder name.

; Set to OFF to specify a different name under "FolderName."

UseDefaultFolderName = ON

FolderName = null

; Set to ON to use "Img" as the default naming convention for images.

; Set to OFF to use a custom naming convention defined in "ImageName."

UseDefaultImageName = OFF

ImageName = image

[Numbering]

; Set to ON to restart the image number when creating a new target folder.

RestartImgNumber = OFF

[Timeout]

; Set the timeout duration for self-termination (in minutes).

TimeToSelfTerminate = 60


## Usage

1. Launch EZSnap.
2. Use the key combination `Ctrl + Alt + Z` to take a screenshot.
3. Customize your settings in `configuration.ini` as needed.
4. Use `Ctrl + Alt + S` to shut down the application or `Ctrl + Alt + X` to check its status.

## Installation

1. Download or clone the EZSnap repository.
2. Double-click EZSnap.exe to get started.



