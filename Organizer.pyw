from os import listdir, rename, mkdir, path as Path
from time import sleep
from windows_toasts import InteractableWindowsToaster, Toast, ToastActivatedEventArgs, ToastButton, ToastInputSelectionBox, ToastSelection
from subprocess import Popen

path = "E:/Downloads/"

types = {
    "Image/": [
        ".png", ".jpg", ".jpeg", ".webp", ".gif",
        ".bmp", ".tif", ".tiff", ".ico", ".svg", ".heic", ".heif", ".avif", ".psd", ".tga",
        ".cr2", ".nef", ".arw"
    ],
    "Executables/": [
        ".exe", ".appimage", ".AppImage", ".deb", ".appinstaller", ".msi",
        ".bat", ".cmd", ".com", ".ps1", ".msix", ".msixbundle", ".appx", ".appxbundle"
    ],
    "Documents/": [
        ".doc", ".docx", ".pdf", ".xlsx", ".xls",
        ".ppt", ".pptx", ".txt", ".rtf", ".odt", ".ods", ".odp", ".csv", ".md"
    ],
    "Compacted/": [
        ".zip", ".rar", ".7z", 
        ".gz", ".bz2", ".xz", ".tar", ".tgz", ".zipx", ".zst"
    ],
    "ISO/": [
        ".iso", ".img", ".vhd", ".vhdx"
    ],
    "Torrent/": [
        ".torrent"
    ],
    "Video/": [
        ".mkv", ".mp4", ".avi", ".mov", ".webm", ".flv", ".wmv", ".m4v"
    ],
    "Audio/": [
        ".wav", ".mp3", ".flac", ".aac", ".ogg", ".m4a", ".wma", ".opus"
    ],
    "Script/": [
        ".java", ".py", ".pyw", ".js", ".c", ".cpp", ".json",
        ".ts", ".tsx", ".html", ".css", ".scss", ".vue", ".rs", ".go", ".php", ".rb", ".sh", ".bat", ".ps1", ".yml", ".yaml", ".toml", ".ini"
    ],
}

exception = [
    None,
    ".fdmdownload",
    ".tmp",
    ".!qB",
    ".!qb",
    ".!ut",
    ".opdownload",
    ".crdownload",
    ".aria2",
    ".part",
    ".download",
    ".partial",
    ".downloading",
    ".filepart",
    ".tmpfile",
    ".!sync",
]

folderShortCurts = {
    "Desktop": "E:/Desktop/",
    "Share": "E:/Share/"
}

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
        rename(f"{oldPath}", f"{toFolder}{file}")
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
        inputDropDown = activatedEventArgs.inputs['newPath'] 

        # Compare if moved the file or clicked to open/show in dir
        for folderShortCurtName, folderShortCurtPath in folderShortCurts.items(): 
            if(folderShortCurtPath == inputDropDown):
                newLocationFile = move(inputDropDown, newPath, file).replace("/", "\\") 
                if(newPath in activatedEventArgs.arguments): 
                    if('/open' in activatedEventArgs.arguments): 
                        Popen(f'explorer /open,"{newLocationFile}"')
                        return
                    elif('/select' in activatedEventArgs.arguments): 
                        Popen(f'explorer /select,"{newLocationFile}"')
                        return
            if(activatedEventArgs.arguments == "confirm"): # Confirm button
                return   
            # If not change the default moved folder
            elif 'explorer /select' in activatedEventArgs.arguments or 'explorer /open' in activatedEventArgs.arguments: 
                Popen(activatedEventArgs.arguments) 
                return

    newToast = Toast([f'File {file} moved to {folderName.replace("/", "")}.'])

    pathReplaced = path.replace("/", "\\")
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
        newFile = organize("Others/", otherFile)
        if newFile != None:
            notification(otherFile, "Others/", newFile)

if __name__ == '__main__':
    while(1):
        verify()
        sleep(2)
