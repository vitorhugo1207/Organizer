path = "D:/Downloads/"

types = {
    "Image/": [".png", ".jpg", ".jpeg", ".webp", ".gif"],
    "Executables/": [".exe", ".AppImage", ".deb", ".appinstaller", ".msi"],
    "Documents/": [".doc", ".docx", ".pdf", ".xlsx", ".xls"],
    "Compacted/": [".zip", ".rar", ".7zip"],
    "ISO/": [".iso", ".img"],
    "Torrent/": [".torrent"],
    "Video/": [".mkv", ".mp4"],
    "Audio/": [".wav", ".mp3"],
    "Script/": [".java", ".py", ".pyw", ".js", ".c", ".cpp", ".json"],
}

exception = [None, ".fdmdownload", ".tmp", ".!qB", ".opdownload", ".crdownload", ".part"]

folderShortCurts = {
    "Desktop": "C:/Users/vitor/Desktop/"
}

from os import listdir, rename, mkdir, path as Path
from time import sleep
from windows_toasts import InteractableWindowsToaster, Toast, ToastActivatedEventArgs, ToastButton, ToastInputSelectionBox, ToastSelection
from subprocess import Popen

def organize(folderName, file):
    countDup = 2
    try:
        rename(f"{path}{file}", f"{path}{folderName}{file}")
        return file

    except FileNotFoundError: # Create folder
        mkdir(f"{path}{folderName}")
        rename(f"{path}{file}", f"{path}{folderName}{file}")
        return file

    except FileExistsError: # If file is Duplicate
        folderFiles = sorted(listdir(f"{path}{folderName}"))

        supposedFile = f"{Path.splitext(file)[0]} ({countDup}){Path.splitext(file)[1]}"

        for folderFile in folderFiles:
            if supposedFile == folderFile and Path.isfile(f"{path}{folderName}{folderFile}"):
                countDup += 1
                supposedFile = f"{Path.splitext(file)[0]} ({countDup}){Path.splitext(file)[1]}"
        
        rename(f"{path}{file}", f"{path}{folderName}{supposedFile}")
        return supposedFile

    except PermissionError: # When another program is using the file
        return

def move(toFolder, oldPath, file):
    countDup = 2
    try:
        rename(f"{oldPath}", f"{toFolder}")

    except FileExistsError: # If file is Duplicate
        folderFiles = sorted(listdir(f"{toFolder}"))

        supposedFile = f"{Path.splitext(file)[0]} ({countDup}){Path.splitext(file)[1]}"

        for folderFile in folderFiles:
            if supposedFile == folderFile and Path.isfile(f"{toFolder}{folderFile}"):
                countDup += 1
                supposedFile = f"{Path.splitext(file)[0]} ({countDup}){Path.splitext(file)[1]}"
        
        rename(f"{oldPath}", f"{toFolder}{supposedFile}")

    except PermissionError: # When another program is using the file
        return

def notification(file, folderName, newFile):
    selections = []
    wintoaster = InteractableWindowsToaster('Organizer')

    def activated_callback(activatedEventArgs: ToastActivatedEventArgs):
        inputDropDown = activatedEventArgs.inputs['newPath']
        if(inputDropDown == 1):
            Popen(activatedEventArgs.arguments) # type: ignore
        else:
            move(inputDropDown, newPath, file)

    newToast = Toast([f'File {file} moved to {folderName.replace("/", "")}.'])

    pathReplaced = path.replace("/", "\\");
    folderNameReplaced = folderName.replace("/", "\\")
    newPath = f'{pathReplaced}{folderNameReplaced}{newFile}'
    newToast.AddAction(ToastButton('Open Location', f'explorer /select,"{newPath}"'))
    newToast.AddAction(ToastButton('Open File', f'explorer /open,"{newPath}"'))

    folderNameToast = folderName.replace("/", "")
    selections = [ToastSelection(f"{pathReplaced}{folderNameReplaced}", f"{folderNameToast}")]
    for folderShortCurtName, folderShortCurtPath in folderShortCurts.items():
        selections.append(ToastSelection(folderShortCurtPath, folderShortCurtName))
    newToast.AddInput(ToastInputSelectionBox('newPath', 'Move file to', selections, selections[0]))

    newToast.on_activated = activated_callback
    
    wintoaster.show_toast(newToast)

def verify():
    otherFiles = []
    newFile = None
    for file in listdir(path):
        for folderName, type in types.items():
            if Path.splitext(file)[1].lower() in type: # File Known
                newFile = organize(folderName, file)
                if newFile != None:
                    notification(file, folderName, newFile)
        if Path.isfile(f"{path}/{file}") and not Path.splitext(file)[1] in exception: # Append Unknown files
            otherFiles.append(file)
    for otherFile in otherFiles: # File Unknown
        if newFile != None:
            newFile = organize("Others/", otherFile)
        notification(otherFile, "Others/", newFile)

if __name__ == '__main__':
    while(1):
        verify()
        sleep(2)
