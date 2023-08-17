<h2 align="center">Organizer</h2>

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

<!-- [![CodeVersion](https://img.shields.io/badge/Code_Version-2023.07.25.0-pink.svg)]()
</div> -->

<p align="center"> 
    Organizer is a Simple Python Folder Organizer with Windows 10 and 11 notification when organize some files with click event to open the folder that file was moved with file selected. Feel free to do any pull request or issue to incluid some file extension or make improvements.
</p>

## Bugs Known

-   When downloading something with qBitTorrent Organizer move the file infinit, yet searching for a solution.
-   When repeat name only can count untill 10.

## Change folder or Added Files
Open the Organizer file `1st line` will be your path to your folder and `2nd line` file extension settings. 

## Instalation
**1st** For instalation you'll need install ``Python``: 
https://www.python.org/downloads/

**2nd** After you will need to added ``pip`` command as global varable on Windows.

**3rd** Install windows_toasts libray running: 
``` 
pip install windows_toasts
``` 

**Note**: Here Organizer will be ready to work, but if you want to automatize it when you startup your PC, then:

**4th** Move `Organizer.pyw` to `C:\Users\%username%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup`

Now when you start your PC, Organizer will oranizer your files on Download folder.

## Future Plans

-   Add a UI interface.
-   Make more controlable to use `.exe` files.
-   Added support to Linux Systems.

## 💻 Technologies Used <a name="Technologies_Used" ></a>

-   Python
-   windows_toasts
