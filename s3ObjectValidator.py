import re, urllib.parse, random
from pathlib import Path

def makeFullStructureSanitize(rootdir,history,filesBool=False,dirsBool=False, DesructiveBool = True, verboseBool = False):

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
    history = {"before": {"files" : [] , "dirs" : [] }, "after": {"files" : [] , "dirs" : [] }}

    makeFullStructureSanitize(rootdir,history,filesBool,dirsBool,DesructiveBool,verboseBool)

    if filesBool:
        return { "before" : history['before']['files'], "after" : history['after']['files']}
    if dirsBool:
        return { "before" : history['before']['dirs'], "after" : history['after']['dirs']}
    else:
        return history

def pathExists(pathString):
    path = Path(pathString)
    if path.exists():
        return True
    else:
        return False

def specialCharacters(string):
    # specialChars = ["&","$","@","=",";","/",":","+"," ",",","?"]
    reg = r'[&$@=;/:+ ,?]'

    if re.findall(reg, string):
        return urllib.parse.quote(string)
    else:
        return string

def avoidCharacters(string):
    # avoidChars = ["{","\^","<","}","%","`","]",">","\[","~","<","#","\\","|"]
    reg = r'[\\{\^<}%`\]>\[~<#\|]'

    if re.findall(reg, string):
        # string = re.sub(reg, "", string)
        return urllib.parse.quote(string)
    else:
        return string

def hasSpecialCharacters(string):
    reg = r'[&$@=;/:+ ,?]'

    if re.findall(reg, string):
        return True
    else:
        return False

def hasAvoidCharacters(string):
    reg = r'[\\{\^<}%`\]>\[~<#\|]'

    if re.findall(reg, string):
        string = re.sub(reg, "", string)
        return True
    else:
        return False

def needsSanitizing(path):
    actualPath = extractActualPath(path)
    if hasAvoidCharacters(actualPath) or hasSpecialCharacters(actualPath):
        return True
    else:
        return False

def extractActualPath(path):
    pathString = str(path).split('/')
    return pathString[-1]
    # actualPath = pathString[-1]
    # return actualPath

def sanitize(path):
    
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