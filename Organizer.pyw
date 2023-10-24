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
    "Desktop": "D:/Desktop/",
    "Share": "D:/Share/"
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
        folderFiles = listdir(f"{path}{folderName}")

        supposedFile = f"{Path.splitext(file)[0]} ({countDup}){Path.splitext(file)[1]}"

        for folderFile in folderFiles:
            if folderFile in folderFiles and supposedFile in folderFiles:
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
        return f"{toFolder}{file}"

    except FileExistsError: # If file is Duplicate
        folderFiles = listdir(f"{toFolder}")

        supposedFile = f"{Path.splitext(file)[0]} ({countDup}){Path.splitext(file)[1]}"

        for folderFile in folderFiles:
            if folderFile in folderFiles and supposedFile in folderFiles:
                countDup += 1
                supposedFile = f"{Path.splitext(file)[0]} ({countDup}){Path.splitext(file)[1]}"
        
        rename(f"{oldPath}", f"{toFolder}{supposedFile}")
        return f"{toFolder}{supposedFile}"

    except PermissionError: # When another program is using the file
        return

def notification(file, folderName, newFile):
    selections = [] # Select itens for menu dropdown
    wintoaster = InteractableWindowsToaster('Organizer')

    def activated_callback(activatedEventArgs: ToastActivatedEventArgs):
        inputDropDown = activatedEventArgs.inputs['newPath'] # type: ignore
        print(activatedEventArgs)

        # Compare if moved the file or clicked to open/show in dir
        for folderShortCurtName, folderShortCurtPath in folderShortCurts.items(): 
            if(folderShortCurtPath == inputDropDown):
                newLocationFile = move(inputDropDown, newPath, file).replace("/", "\\") # type: ignore
                if(newPath in activatedEventArgs.arguments): # type: ignore
                    if('/open' in activatedEventArgs.arguments): # type: ignore
                        Popen(f'explorer /open,"{newLocationFile}"')
                        return
                    elif('/select' in activatedEventArgs.arguments): # type: ignore
                        Popen(f'explorer /select,"{newLocationFile}"')
                        return
            if(activatedEventArgs.arguments == "confirm"): # Confirm button
                return   
            # If not change the default moved folder
            elif 'explorer /select' in activatedEventArgs.arguments or 'explorer /open' in activatedEventArgs.arguments: # type: ignore
                Popen(activatedEventArgs.arguments) # type: ignore
                return

    newToast = Toast([f'File {file} moved to {folderName.replace("/", "")}.'])

    pathReplaced = path.replace("/", "\\");
    folderNameReplaced = folderName.replace("/", "\\")
    newPath = f'{pathReplaced}{folderNameReplaced}{newFile}'

    newToast.AddAction(ToastButton('Open Location', f'explorer /select,"{newPath}"'))
    newToast.AddAction(ToastButton('Open File', f'explorer /open,"{newPath}"'))
    newToast.AddAction(ToastButton('Confirm', 'confirm'))

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
