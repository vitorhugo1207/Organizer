from os import listdir, rename, mkdir, path as Path
from time import sleep
from windows_toasts import WindowsToaster, ToastText1
from subprocess import Popen

path = "C:/Users/vitor/Downloads/"

types = {
    "Image/": [".png", ".jpg", ".jpeg", ".webp", ".gif"],
    "Executables/": [".exe", ".AppImage", ".deb", ".appinstaller", ".msi"],
    "Documents/": [".doc", ".docx", ".pdf", ".xlsx", ".xls"],
    "Compacted/": [".zip", ".rar", ".7zip"],
    "ISO/": [".iso", ".img"],
    "Torrent/": [".torrent"],
    "Video/": [".mkv", ".mp4"],
    "Audio/": [".wav", ".mp3"],
    "Script/": [".java", ".py", ".pyw", ".js", ".c", ".cpp", ".json"]
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
            if supposedFile == folderFile and Path.isfile(f"{path}{folderName}{folderFile}"):
                countDup += 1
                supposedFile = f"{Path.splitext(file)[0]} ({countDup}){Path.splitext(file)[1]}"
        
        rename(f"{path}{file}", f"{path}{folderName}{supposedFile}")
        return supposedFile

    except PermissionError: # When another program is using the file
        return

def notification(file, folderName, newFile):
    newToast = ToastText1()
    newToast.SetBody(f'File {file} moved to {folderName.replace("/", "")}. \nClick to open folder.')
    pathReplaced = path.replace("/", "\\")
    folderNameReplaced = folderName.replace("/", "\\")
    newToast.on_activated = lambda _: Popen(f'explorer /select,"{pathReplaced}{folderNameReplaced}{newFile}"')
    wintoaster.show_toast(newToast)

def verify():
    otherFiles = []
    for file in files:
        # Make a exeption is all is files is a dir
        for folderName, type in types.items():
            if Path.splitext(file)[1] in type: # File Known
                newFile = organize(folderName, file)
                notification(file, folderName, newFile)
        if Path.isfile(f"{path}/{file}") and Path.splitext(file)[1] != None and not Path.splitext(file)[1] == ".tmp": # Append Unknown files
            otherFiles.append(file)
    for otherFile in otherFiles: # File Unknown
        newFile = organize("Others/", otherFile)
        notification(otherFile, "Others/", newFile)

if __name__ == '__main__':
    wintoaster = WindowsToaster('Organizer Folder')
    while(1):
        files = listdir(path)
        verify()
        sleep(2)
