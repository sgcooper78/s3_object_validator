import re, urllib.parse, random, argparse
from pathlib import Path

def makeFullStructureSanitize(rootdir,history,filesBool=False,dirsBool=False, DesructiveBool = True, verboseBool = False):
    """
    makeFullStructureSanitize creates structure and loops through it

    Parameters:
    rootdir (str): directory root to scan
    history (bool): dict to make history
    filesBool (bool): bool if scanning files
    dirsBool (bool): bool if scanning dirs
    DesructiveBool (bool): bool if scanning without changing names
    verboseBool (bool): bool for more printouts
  
    Returns:
    None: nothing returned
    """ 

    for path in Path(rootdir).iterdir():
        if path.is_symlink():
            if verboseBool:
                print(f"{path} is a symlink, symlinks will be removed as they are not supported in S3")
            print("unlinking symlink")
            print(path)
            if DesructiveBool:
                path.unlink()
        if path.is_file() and filesBool:
            # history['before']['files'].append(path)
            if needsSanitizing(path):
                if verboseBool:
                    print(f"{path} is a file")
                print(f"{path} needs to be sanitized")
                print(path)
                if DesructiveBool:
                    path = sanitize(path)
                # history['after']['files'].append(path)
        elif path.is_dir() and not path.is_symlink():
            if dirsBool:
                # history['before']['dirs'].append(path)
                if needsSanitizing(path):
                    if verboseBool:
                        print(f"{path} is a directory")
                    print(f"{path} needs to be sanitized")
                    print(path)
                    if DesructiveBool:
                        path = sanitize(path)
                    # history['after']['dirs'].append(path)
            print(f"Changing directory to {path}")
            makeFullStructureSanitize(path,history,filesBool,dirsBool,DesructiveBool,verboseBool)


def sanitizeStructure(rootdir,filesBool=False,dirsBool=False, DesructiveBool = True,verboseBool = False):
    """
    sanitizeStructure sets up history, scans and changes files/dirs and returns history.

    Parameters:
    rootdir (str): directory root to scan
    filesBool (bool): bool if scanning files
    dirsBool (bool): bool if scanning dirs
    DesructiveBool (bool): bool if scanning without changing names
    verboseBool (bool): bool for more printouts
  
    Returns:
    dict: history of what was changed
    """ 
    history = {"before": {"files" : [] , "dirs" : [] }, "after": {"files" : [] , "dirs" : [] }}

    makeFullStructureSanitize(rootdir,history,filesBool,dirsBool,DesructiveBool,verboseBool)

    if filesBool:
        return { "before" : history['before']['files'], "after" : history['after']['files']}
    if dirsBool:
        return { "before" : history['before']['dirs'], "after" : history['after']['dirs']}
    else:
        return history

def pathExists(pathString):
    """
    Checks if path exists and returns True or False

    Parameters:
    pathString (str): path to test
  
    Returns:
    bool: bool wether path exists or not
    """ 
    path = Path(pathString)
    if path.exists():
        return True
    else:
        return False

def specialCharacters(string):
    """
    replaces special characters by encoding them

    Parameters:
    string (str): string to test
  
    Returns:
    str: url encoded string
    """ 
    # specialChars = ["&","$","@","=",";","/",":","+"," ",",","?"]
    reg = r'[&$@=;/:+ ,?]'

    if re.findall(reg, string):
        return urllib.parse.quote(string)
    else:
        return string

def avoidCharacters(string):
    """
    replaces avoid characters by encoding them

    Parameters:
    string (str): string to test
  
    Returns:
    str: url encoded string
    """ 
    # avoidChars = ["{","\^","<","}","%","`","]",">","\[","~","<","#","\\","|"]
    reg = r'[\\{\^<}%`\]>\[~<#\|]'

    if re.findall(reg, string):
        # string = re.sub(reg, "", string)
        return urllib.parse.quote(string)
    else:
        return string

def hasSpecialCharacters(string):
    """
    tests if string has special characters

    Parameters:
    string (str): string to test
  
    Returns:
    bool: retuns True or False depending on if it contains special characters
    """ 
    reg = r'[&$@=;/:+ ,?]'

    if re.findall(reg, string):
        return True
    else:
        return False

def hasAvoidCharacters(string):
    """
    tests if string has avoid characters

    Parameters:
    string (str): string to test
  
    Returns:
    bool: retuns True or False depending on if it contains avoid characters
    """ 
    reg = r'[\\{\^<}%`\]>\[~<#\|]'

    if re.findall(reg, string):
        return True
    else:
        return False

def needsSanitizing(path):
    """
    tests if string needs to be sanitized at all

    Parameters:
    path (str): string to test
  
    Returns:
    bool: retuns True or False if path needs to be sanitized
    """ 
    actualPath = extractActualPath(path)
    if hasAvoidCharacters(actualPath) or hasSpecialCharacters(actualPath):
        return True
    else:
        return False

def extractActualPath(path):
    """
    extracts end out of a path
    for example /var/log/example.log would return example.log

    Parameters:
    path (str): path to extract end out of
  
    Returns:
    str: returns file name or directory name
    """ 
    pathString = str(path).split('/')
    return pathString[-1]
    # actualPath = pathString[-1]
    # return actualPath

def sanitize(path):
    """
    Sanitizes a Path

    Parameters:
    path (str): path to sanitize
  
    Returns:
    Path: returns sanitized Path
    """ 
    
    pathString = str(path).split('/')
    newActualPath = actualPath = pathString[-1]
    if hasSpecialCharacters(newActualPath):
        newActualPath = specialCharacters(newActualPath)
    if hasAvoidCharacters(newActualPath):
        newActualPath = avoidCharacters(newActualPath)

    if newActualPath == actualPath:
        return path
    pathString[-1] = newActualPath
    newPath = "/".join(pathString)
    if pathExists(newPath):
        randomNumber = str(random.randrange(1, 10000000))
        path.replace(newPath + randomNumber)
        newPathObject = Path(newPath + randomNumber)
    else:
        path.replace(newPath)
        newPathObject = Path(newPath)

    return newPathObject

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("Path", type=str ,help="Path to scan directories/files")
    parser.add_argument("-d", "--directory", default=False, action="store_true" ,help="Makes scan only include directories")
    parser.add_argument("-s", "--scan", default=True, action="store_true" ,help="Makes scan non-destructive")
    parser.add_argument("-f", "--files", default=False, action="store_true" ,help="Makes scan only include files")
    parser.add_argument("-v", "--verbose", default=False, action="store_true" ,help="Increase verbosity of program" )

    args = parser.parse_args()

    if not Path(args.Path).exists():
        print("File or directory path does not exist")
        exit()

    cleaned = sanitizeStructure(args.Path,args.files,args.directory,args.scan,args.verbose)
    print("Done sanitizing")


if __name__ == "__main__":
    main()